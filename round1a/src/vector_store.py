import fitz  # PyMuPDF
import os
import json
import re
from collections import defaultdict
from PIL import Image
import io
import pytesseract

def is_table_or_graphics_heavy(blocks):
    if not blocks:
        return False
    num_blocks = len(blocks)
    num_text = sum(1 for b in blocks if b.get("type") == 0)
    num_image = sum(1 for b in blocks if b.get("type") == 1)
    num_vector = sum(1 for b in blocks if b.get("type") == 2)
    text_ratio = num_text / num_blocks if num_blocks else 0
    graphics_ratio = (num_image + num_vector) / num_blocks if num_blocks else 0
    if text_ratio < 0.3 or graphics_ratio > 0.3:
        return True
    return False

def is_meaningful_heading(text):
    if len(text) < 4:
        return False
    if re.fullmatch(r"[\-\u2022\*\s]+", text):
        return False
    if re.match(r"^\d+(\.\d+)*\s", text):
        return True
    if text[0].isupper():
        return True
    if text.islower():
        return False
    return True

def is_possible_table_line(text, level):
    short_problematic_texts = {
        "name", "date", "signature", "address", "age", "s.no", "s.no.", "service",
        "pay", "designation", "relationship", "persons", "single", "whether", "rs."
    }
    normalized = text.strip().lower()
    if normalized in short_problematic_texts:
        return True
    if len(text) < 5:
        return True
    if re.fullmatch(r"[0-9\.\-]+", normalized):
        return True
    return False

def clean_heading_text(text):
    text = re.sub(r"[\t\r\n]+", " ", text)  # Replace tabs and newlines with space
    text = re.sub(r" +", " ", text)  # Collapse multiple spaces
    text = text.strip()
    if not text.endswith(" "):
        text += " "
    return text

def extract_text_with_ocr(page):
    ocr_texts = []
    for img_index, img in enumerate(page.get_images(full=True)):
        xref = img[0]
        base_image = page.extract_image(xref)
        image_bytes = base_image['image']
        image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
        try:
            text = pytesseract.image_to_string(image)
            if text.strip():
                ocr_texts.append(text.strip())
        except Exception as e:
            print(f"Warning: OCR failed on image {img_index} of page {page.number+1}: {e}")
    return "\n".join(ocr_texts)

def extract_title(doc, pdf_path):
    page = doc[0]
    blocks = page.get_text("dict")["blocks"]
    lines = []
    font_sizes = defaultdict(int)
    for block in blocks:
        if "lines" not in block:
            continue
        for line in block["lines"]:
            text = ""
            size = None
            for span in line["spans"]:
                span_text = span.get("text", "").strip()
                if not span_text:
                    continue
                if size is None:
                    size = round(span["size"], 1)
                text += " " + span_text
            text = text.strip()
            if text:
                lines.append({
                    "text": text,
                    "size": size,
                    "y0": line.get("bbox", [0, 0, 0, 0])[1]
                })
                font_sizes[size] += 1

    if not lines:
        ocr_text = extract_text_with_ocr(page)
        if ocr_text:
            first_line = ocr_text.split('\n')[0]
            if len(first_line) > 0:
                return first_line

    if not lines:
        return os.path.splitext(os.path.basename(pdf_path))[0]

    max_size = max(line["size"] for line in lines)
    max_lines = [line for line in lines if line["size"] == max_size]
    max_lines.sort(key=lambda x: x.get("y0", 0))
    for line in max_lines:
        if len(line["text"]) > 3:
            return line["text"]

    return os.path.splitext(os.path.basename(pdf_path))[0]

def extract_outline_and_title(pdf_path):
    doc = fitz.open(pdf_path)
    first_page_blocks = doc[0].get_text("dict")["blocks"]
    
    # Detect if document is table/image heavy -> only extract title, no outline
    if is_table_or_graphics_heavy(first_page_blocks):
        title = extract_title(doc, pdf_path)
        # Check for headline text to be put in outline if title is empty or very short
        headline = None
        # Get largest font text on first page for headline
        all_lines = []
        for line in doc[0].get_text("dict")["blocks"]:
            if "lines" not in line:
                continue
            for ln in line["lines"]:
                txt = "".join([span["text"] for span in ln["spans"]]).strip()
                size = round(ln["lines"][0]["spans"][0]["size"], 1) if ln["lines"][0]["spans"] else 0
                if txt:
                    all_lines.append({"text": txt, "size": size})
        if all_lines:
            max_size = max(l["size"] for l in all_lines)
            max_lines = [l["text"] for l in all_lines if abs(l["size"] - max_size) < 0.5]
            if max_lines and (not title or len(title.strip()) < 5):
                headline = max_lines[0]
        if headline:
            return {
                "title": "",
                "outline": [{
                    "level": "H1",
                    "text": headline + " ",
                    "page": 0
                }]
            }
        else:
            return {"title": title, "outline": []}

    lines = []
    font_sizes = defaultdict(int)
    for page_idx, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        if not blocks:
            # OCR fallback for image-only pages
            ocr_text = extract_text_with_ocr(page)
            if ocr_text:
                lines.append({
                    "text": ocr_text,
                    "size": 10,
                    "page": page_idx + 1,
                    "y0": 0
                })
            continue
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = ""
                size = None
                for span in line["spans"]:
                    span_text = span.get("text", "").strip()
                    if not span_text:
                        continue
                    if size is None:
                        size = round(span["size"], 1)
                    text += " " + span_text
                text = text.strip()
                if text:
                    lines.append({
                        "text": text,
                        "size": size,
                        "page": page_idx + 1,
                        "y0": line.get("bbox", [0, 0, 0, 0])[1]
                    })
                    font_sizes[size] += 1

    title = extract_title(doc, pdf_path)
    sorted_fonts = sorted(font_sizes.items(), key=lambda x: -x[0])
    font_to_level = {}
    levels = ["H1", "H2", "H3"]
    sizes_assigned = []
    for size, _ in sorted_fonts:
        if len(sizes_assigned) >= len(levels):
            break
        if all(abs(size - assigned) > 0.5 for assigned in sizes_assigned):
            font_to_level[size] = levels[len(sizes_assigned)]
            sizes_assigned.append(size)

    outline = []
    added_texts = set()
    for line in lines:
        text = clean_heading_text(line["text"])
        page = line["page"]
        size = line["size"]
        level = font_to_level.get(size)
        if not level:
            continue
        if not is_meaningful_heading(text):
            continue
        if is_possible_table_line(text, level):
            continue
        if text in added_texts:
            continue
        added_texts.add(text)
        outline.append({
            "level": level,
            "text": text,
            "page": page
        })

    return {"title": title.strip(), "outline": outline}

def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = sorted([f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')])
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file}")
        pdf_path = os.path.join(input_dir, pdf_file)
        result = extract_outline_and_title(pdf_path)
        output_filename = os.path.splitext(pdf_file)[0] + ".json"
        output_path = os.path.join(output_dir, output_filename)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)
        print(f"Saved {output_filename}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 3:
        process_all_pdfs(sys.argv[1], sys.argv[2])
    else:
        # Assume docker run mode
        process_all_pdfs("input", "output")

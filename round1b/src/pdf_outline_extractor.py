import fitz  # PyMuPDF
import os
import json
import re
import sys
from collections import defaultdict


def extract_outline_and_title(pdf_path):
    doc = fitz.open(pdf_path)
    lines = []
    font_sizes = defaultdict(int)

    for page_index, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if "lines" not in block:
                continue
            for line in block["lines"]:
                text = ""
                size = None
                for span in line["spans"]:
                    span_text = span["text"].strip()
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
                        "page": page_index
                    })
                    font_sizes[size] += 1

    # Step 1: Get title from first page (max font size)
    title_candidates = [line for line in lines if line["page"] == 0]
    if title_candidates:
        max_size = max(line["size"] for line in title_candidates)
        title = " ".join(line["text"] for line in title_candidates if line["size"] == max_size)
    else:
        title = ""

    # Step 2: Assign font sizes to H1, H2, H3, H4...
    sorted_fonts = sorted(font_sizes.items(), key=lambda x: -x[0])
    levels = ["H1", "H2", "H3", "H4", "H5", "H6"]
    font_to_level = {}
    for i, (size, _) in enumerate(sorted_fonts[:len(levels)]):
        font_to_level[size] = levels[i]

    # Step 3: Extract outline from pages 1 onward
    outline = []
    for line in lines:
        page = line["page"]
        if page == 0:
            continue  # skip first page

        text = line["text"].strip()
        size = line["size"]
        level = font_to_level.get(size)
        if not level:
            continue

        # Accept if ends with colon or has numbering pattern or sentence-like case
        if re.match(r"^\d+(\.\d+)*\s", text) or text.endswith(":") or text.istitle():
            outline.append({
                "level": level,
                "text": text + " ",
                "page": page
            })

    return {
        "title": title.strip(),
        "outline": outline
    }


def process_all_pdfs(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    pdf_files = sorted(f for f in os.listdir(input_dir) if f.lower().endswith(".pdf"))

    for idx, pdf_file in enumerate(pdf_files, 1):
        pdf_path = os.path.join(input_dir, pdf_file)
        print(f"Processing {pdf_file}...")
        result = extract_outline_and_title(pdf_path)

        output_path = os.path.join(output_dir, f"file{idx:02}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4, ensure_ascii=False)

        print(f"Saved to {output_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python pdf_outline_extractor.py <input_pdf_folder> <output_json_folder>")
        sys.exit(1)

    input_folder = sys.argv[1]
    output_folder = sys.argv[2]
    process_all_pdfs(input_folder, output_folder)

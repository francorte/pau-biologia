from pathlib import Path
import json
import fitz  # PyMuPDF

YEAR = 2025

PDF_DIR = Path("pdfs")
OUTPUT_DIR = Path("extracted_exams")
OUTPUT_FILE = OUTPUT_DIR / f"examen_{YEAR}.json"

pdfs = list(PDF_DIR.glob("*.pdf"))
print("PDFs encontrados:", pdfs)

if not pdfs:
    print("❌ No hay PDFs en la carpeta 'pdfs/'")
    exit()

results = []
qid = 1

for pdf_path in pdfs:
    doc = fitz.open(pdf_path)

    for page_index, page in enumerate(doc, start=1):
        text = page.get_text().strip()

        if not text:
            continue

        results.append({
            "id": f"BIO_{YEAR}_{qid:03}",
            "year": YEAR,
            "pdf": pdf_path.name,
            "page": page_index,
            "texto": text
        })

        qid += 1

OUTPUT_DIR.mkdir(exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print(f"✅ OK → {len(results)} páginas procesadas")
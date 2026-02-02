import pdfplumber
import json
import sys
from pathlib import Path

# =======================
# USO:
# python extract_pdf.py <ruta_pdf> <año> <salida.json>
# =======================

if len(sys.argv) != 4:
    print("Uso: python extract_pdf.py <ruta_pdf> <año> <salida.json>")
    sys.exit(1)

pdf_path = Path(sys.argv[1])
year = int(sys.argv[2])
output_path = Path(sys.argv[3])

if not pdf_path.exists():
    print(f"Error: no existe el archivo {pdf_path}")
    sys.exit(1)

pages_text = []

with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text()
        if text:
            pages_text.append({
                "page": i,
                "text": text.strip()
            })

result = {
    "source_year": year,
    "pdf_path": str(pdf_path),
    "pages": pages_text
}

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print("Extracción completada correctamente.")
print(f"Páginas extraídas: {len(pages_text)}")
print(f"Archivo generado: {output_path}")
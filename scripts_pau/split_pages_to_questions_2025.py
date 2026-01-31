from pathlib import Path
import json
import re

YEAR = 2025

INPUT_FILE = Path("extracted_exams") / f"examen_{YEAR}.json"
OUTPUT_FILE = Path("extracted_exams") / f"preguntas_{YEAR}.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    pages = json.load(f)

questions = []
qid = 1

# patrón típico de enunciado PAU (ajustable)
QUESTION_PATTERN = re.compile(
    r"(?:^|\n)(\d+\.\s+.*?)(?=\n\d+\.|\Z)",
    re.DOTALL
)

for page in pages:
    text = page["texto"]

    matches = QUESTION_PATTERN.findall(text)

    for m in matches:
        questions.append({
            "id": f"BIO_{YEAR}_Q{qid:03}",
            "year": YEAR,
            "pdf": page["pdf"],
            "page": page["page"],
            "texto": m.strip()
        })
        qid += 1

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(questions)} preguntas extraídas")
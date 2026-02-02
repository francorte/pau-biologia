from pathlib import Path
import json
import re

YEAR = 2025

INPUT_FILE = Path("extracted_exams") / f"preguntas_{YEAR}.json"
OUTPUT_FILE = Path("extracted_exams") / f"preguntas_{YEAR}_figuras.json"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    questions = json.load(f)

# Patrones típicos PAU
FIGURE_PATTERNS = {
    "figura": re.compile(r"\bfigura\b", re.IGNORECASE),
    "gráfico": re.compile(r"\bgr[aá]fico\b", re.IGNORECASE),
    "tabla": re.compile(r"\btabla\b", re.IGNORECASE),
    "esquema": re.compile(r"\besquema\b", re.IGNORECASE),
    "imagen": re.compile(r"\bimagen\b", re.IGNORECASE)
}

for q in questions:
    texto = q["texto"]

    referencias = []

    for tipo, pattern in FIGURE_PATTERNS.items():
        if pattern.search(texto):
            referencias.append(tipo)

    q["requiere_imagen"] = len(referencias) > 0
    q["referencias_visual"] = referencias

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(questions, f, ensure_ascii=False, indent=2)

print(f"✅ {len(questions)} preguntas analizadas (referencias visuales detectadas)")
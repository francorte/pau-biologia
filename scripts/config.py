from pathlib import Path
import logging

PROJECT_ROOT = Path(__file__).parent.absolute()
INPUT_DIR = Path("/Users/franciscodelacorte/Desktop/Biología/2025")
DB_DIR = PROJECT_ROOT / "db"
DB_PATH = DB_DIR / "pau_biologia.db"
EXTRACTED_EXAMS_DIR = PROJECT_ROOT / "extracted_exams"
PUBLIC_IMAGES_DIR = PROJECT_ROOT / "public" / "exam_images"
LOGS_DIR = PROJECT_ROOT / "logs"

for directory in [DB_DIR, EXTRACTED_EXAMS_DIR, PUBLIC_IMAGES_DIR, LOGS_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

YEAR = 2025
EXAM_CONFIG = {
    'A': {'name': 'Examen A', 'file': 'Examen_A_2025.pdf'},
    'B': {'name': 'Examen B', 'file': 'Examen_B_2025.pdf'},
    'C': {'name': 'Examen C', 'file': 'Examen_C_2025.pdf'},
    'D': {'name': 'Examen D', 'file': 'Examen_D_2025.pdf'},
}

BLOQUE_KEYWORDS = {
    'A': ['biomolécula', 'proteína', 'lípido', 'glúcido', 'ácido nucleico'],
    'B': ['replicación', 'transcripción', 'traducción', 'mutación', 'expresión'],
    'C': ['membrana', 'célula', 'mitosis', 'meiosis', 'orgánulo'],
    'D': ['metabolismo', 'respiración', 'fotosíntesis', 'glucólisis'],
    'E': ['biotecnología', 'PCR', 'CRISPR', 'ADN recombinante'],
    'F': ['inmunidad', 'anticuerpo', 'linfocito', 'antígeno'],
}

LABEL_TO_QUESTION_NUMBER = {
    '1': 1, '2.1': 2, '2.2': 3, '3.1': 4, '3.2': 5,
    '4.1': 6, '4.2': 7, '5.1': 8, '5.2': 9,
}

LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_FILE = LOGS_DIR / f"exam_processor_{YEAR}.log"

def validate_paths():
    if not INPUT_DIR.exists():
        raise FileNotFoundError(f"❌ Carpeta no existe: {INPUT_DIR}")

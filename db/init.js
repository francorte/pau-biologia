import Database from "better-sqlite3";

// Crear o abrir la base de datos
const db = new Database("db/pau_biologia.db");

// =======================
// TABLA DE EXÁMENES (origen)
// =======================
db.prepare(`
  CREATE TABLE IF NOT EXISTS exams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    year INTEGER NOT NULL,
    pdf_path TEXT NOT NULL
  )
`).run();

// =======================
// TABLA DE BLOQUES PAU 2026
// =======================
db.prepare(`
  CREATE TABLE IF NOT EXISTS blocks (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL
  )
`).run();

// =======================
// TABLA DE PREGUNTAS NORMALIZADAS
// =======================
db.prepare(`
  CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    exam_id INTEGER NOT NULL,
    question_code TEXT NOT NULL,
    original_text TEXT NOT NULL,
    normalized_text TEXT,
    block_code TEXT NOT NULL,
    source_year INTEGER NOT NULL,
    requires_image INTEGER DEFAULT 0,
    image_hint TEXT,
    FOREIGN KEY (exam_id) REFERENCES exams(id),
    FOREIGN KEY (block_code) REFERENCES blocks(code)
  )
`).run();

// =======================
// INSERTAR BLOQUES OFICIALES PAU 2026
// =======================
const blocks = [
  ["A", "Biomoléculas"],
  ["B", "Genética molecular"],
  ["C", "Biología celular"],
  ["D", "Metabolismo"],
  ["E", "Biotecnología"],
  ["F", "Inmunología"]
];

const insertBlock = db.prepare(`
  INSERT OR IGNORE INTO blocks (code, name)
  VALUES (?, ?)
`);

for (const block of blocks) {
  insertBlock.run(block);
}

console.log("Base de datos PAU Biología (modelo 2026) creada correctamente.");
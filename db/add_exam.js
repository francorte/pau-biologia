import Database from "better-sqlite3";
import path from "path";

// Abrir la base de datos
const db = new Database("db/pau_biologia.db");

// =======================
// ARGUMENTOS DE ENTRADA
// =======================
// Uso desde terminal:
// node db/add_exam.js 2025 /ruta/al/examen.pdf

const year = process.argv[2];
const pdfPath = process.argv[3];

if (!year || !pdfPath) {
  console.error("Uso correcto:");
  console.error("node db/add_exam.js <año> <ruta_pdf>");
  process.exit(1);
}

// Convertir la ruta a absoluta
const absolutePath = path.resolve(pdfPath);

// =======================
// INSERTAR EXAMEN
// =======================
const insertExam = db.prepare(`
  INSERT INTO exams (year, pdf_path)
  VALUES (?, ?)
`);

const result = insertExam.run(year, absolutePath);

console.log("Examen registrado correctamente.");
console.log("ID del examen:", result.lastInsertRowid);
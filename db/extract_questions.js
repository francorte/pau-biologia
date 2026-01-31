import fs from "fs";
import Database from "better-sqlite3";
import * as pdfjsLib from "pdfjs-dist/legacy/build/pdf.mjs";

// =======================
// CONFIGURACIÓN NODE
// =======================

// En entorno Node NO hay worker
pdfjsLib.GlobalWorkerOptions.workerSrc = null;

// =======================
// USO:
// npm run extract -- <exam_id>
// =======================

const examId = process.argv[2];

if (!examId) {
  console.error("Uso: npm run extract -- <exam_id>");
  process.exit(1);
}

// Abrir base de datos
const db = new Database("db/pau_biologia.db");

// Obtener ruta del PDF y año
const exam = db
  .prepare("SELECT pdf_path, year FROM exams WHERE id = ?")
  .get(examId);

if (!exam) {
  console.error("Examen no encontrado.");
  process.exit(1);
}

// =======================
// LEER PDF (NODE SAFE)
// =======================

const data = new Uint8Array(fs.readFileSync(exam.pdf_path));
const pdf = await pdfjsLib.getDocument({ data }).promise;

let fullText = "";

for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
  const page = await pdf.getPage(pageNum);
  const content = await page.getTextContent();

  const pageText = content.items
    .map(item => item.str)
    .join(" ");

  fullText += pageText + "\n";
}

// =======================
// EXTRACCIÓN BÁSICA
// =======================

const rawQuestions = fullText
  .split(/Pregunta\s+/i)
  .slice(1);

console.log(`Preguntas detectadas: ${rawQuestions.length}`);

// Insertar en BD
const insertQuestion = db.prepare(`
  INSERT INTO questions (
    exam_id,
    question_code,
    original_text,
    normalized_text,
    block_code,
    source_year,
    requires_image
  )
  VALUES (?, ?, ?, NULL, ?, ?, 0)
`);

let counter = 1;

for (const q of rawQuestions) {
  const questionText = q.trim();

  if (questionText.length < 50) continue;

  insertQuestion.run(
    examId,
    `RAW-${counter}`,
    questionText,
    "A",          // bloque provisional
    exam.year
  );

  counter++;
}

console.log("Extracción básica completada.");
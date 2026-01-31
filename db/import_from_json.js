import fs from "fs";
import Database from "better-sqlite3";

// =======================
// USO:
// node db/import_from_json.js <ruta_json>
// =======================

const jsonPath = process.argv[2];

if (!jsonPath) {
  console.error("Uso: node db/import_from_json.js <ruta_json>");
  process.exit(1);
}

if (!fs.existsSync(jsonPath)) {
  console.error("No existe el archivo JSON:", jsonPath);
  process.exit(1);
}

// Abrir BD
const db = new Database("db/pau_biologia.db");

// Leer JSON
const raw = fs.readFileSync(jsonPath, "utf-8");
const data = JSON.parse(raw);

const { source_year, pages } = data;

// Unir todo el texto
const fullText = pages.map(p => p.text).join("\n");

// =======================
// EXTRACCIÓN DE PREGUNTAS
// =======================

const rawQuestions = fullText
  .split(/Pregunta\s+/i)
  .slice(1);

console.log(`Preguntas detectadas: ${rawQuestions.length}`);

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
  VALUES (?, ?, ?, NULL, ?, ?, ?)
`);

// Crear examen lógico (solo una vez)
const exam = db.prepare(
  "SELECT id FROM exams WHERE year = ?"
).get(source_year);

if (!exam) {
  console.error("No existe examen registrado para ese año.");
  process.exit(1);
}

let counter = 1;

for (const q of rawQuestions) {
  const text = q.trim();
  if (text.length < 50) continue;

  // Heurística simple: ¿requiere imagen?
  const requiresImage = /(figura|esquema|gráfico|tabla|imagen)/i.test(text)
    ? 1
    : 0;

  insertQuestion.run(
    exam.id,
    `RAW-${counter}`,
    text,
    "A",              // bloque provisional
    source_year,
    requiresImage
  );

  counter++;
}

console.log("Importación desde JSON completada.");
import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbPath = path.join(__dirname, 'pau_biologia.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error abriendo BD:', err);
    process.exit(1);
  }
  console.log('✓ Conectado a pau_biologia.db');
});

db.serialize(() => {
  // Tabla: Exámenes
  db.run(`
    CREATE TABLE IF NOT EXISTS exams (
      id TEXT PRIMARY KEY,
      year INTEGER NOT NULL,
      exam_letter TEXT NOT NULL,
      pdf_path TEXT,
      extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
  `, (err) => {
    if (err) console.error('Error creando tabla exams:', err);
    else console.log('✓ Tabla exams creada');
  });

  // Tabla: Preguntas
  db.run(`
    CREATE TABLE IF NOT EXISTS questions (
      id TEXT PRIMARY KEY,
      exam_id TEXT NOT NULL,
      question_number INTEGER NOT NULL,
      bloque TEXT,
      text TEXT,
      FOREIGN KEY (exam_id) REFERENCES exams(id)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla questions:', err);
    else console.log('✓ Tabla questions creada');
  });

  // Tabla: Apartados
  db.run(`
    CREATE TABLE IF NOT EXISTS apartados (
      id TEXT PRIMARY KEY,
      question_id TEXT NOT NULL,
      label TEXT NOT NULL,
      text TEXT,
      points REAL,
      FOREIGN KEY (question_id) REFERENCES questions(id)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla apartados:', err);
    else console.log('✓ Tabla apartados creada');
  });

  // Tabla: Imágenes
  db.run(`
    CREATE TABLE IF NOT EXISTS images (
      id TEXT PRIMARY KEY,
      exam_id TEXT NOT NULL,
      page_number INTEGER,
      image_data BLOB,
      FOREIGN KEY (exam_id) REFERENCES exams(id)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla images:', err);
    else console.log('✓ Tabla images creada');
  });

  // Tabla: Corrección
  db.run(`
    CREATE TABLE IF NOT EXISTS correction_criteria (
      id TEXT PRIMARY KEY,
      apartado_id TEXT NOT NULL,
      criteria_text TEXT,
      FOREIGN KEY (apartado_id) REFERENCES apartados(id)
    )
  `, (err) => {
    if (err) console.error('Error creando tabla correction_criteria:', err);
    else console.log('✓ Tabla correction_criteria creada');
  });
});

db.close((err) => {
  if (err) {
    console.error('Error cerrando BD:', err);
  } else {
    console.log('\n✅ ESQUEMA CREADO EXITOSAMENTE');
  }
});
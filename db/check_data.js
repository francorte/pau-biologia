import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbPath = path.join(__dirname, 'pau_biologia.db');

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error:', err);
    process.exit(1);
  }
  console.log('✓ Conectado a pau_biologia.db\n');
});

db.serialize(() => {
  // Ver estructura de exámenes
  console.log('=== EXÁMENES ===');
  db.all(`SELECT * FROM exams LIMIT 3`, [], (err, rows) => {
    if (rows) {
      rows.forEach(row => console.log(row));
    }
    
    console.log('\n=== PREGUNTAS (Ejemplo) ===');
    db.all(`SELECT id, exam_id, question_number, bloque, text FROM questions LIMIT 2`, [], (err, rows) => {
      if (rows) {
        rows.forEach(row => {
          console.log(`\nID: ${row.id}`);
          console.log(`Exam: ${row.exam_id}`);
          console.log(`Bloque: ${row.bloque}`);
          console.log(`Texto: ${row.text.substring(0, 80)}...`);
        });
      }
      
      console.log('\n=== APARTADOS (Ejemplo) ===');
      db.all(`SELECT id, question_id, label, points FROM apartados LIMIT 5`, [], (err, rows) => {
        if (rows) {
          rows.forEach(row => console.log(row));
        }
        
        console.log('\n=== RESUMEN ===');
        db.all(`
          SELECT 
            (SELECT COUNT(*) FROM exams) as exams,
            (SELECT COUNT(*) FROM questions) as questions,
            (SELECT COUNT(*) FROM apartados) as apartados,
            (SELECT COUNT(*) FROM images) as images
        `, [], (err, rows) => {
          if (rows) {
            console.log(rows[0]);
          }
          db.close();
        });
      });
    });
  });
});
import sqlite3 from 'sqlite3';
import path from 'path';
import fs from 'fs';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const dbPath = path.join(__dirname, 'pau_biologia.db');
const jsonPath = path.join(__dirname, '..', 'extracted_exams', 'all_exams.json');

if (!fs.existsSync(jsonPath)) {
  console.error(`✗ Error: No se encuentra ${jsonPath}`);
  console.error('  Ejecuta primero: python3 extract_exams_complete.py');
  process.exit(1);
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('✗ Error conectando a BD:', err);
    process.exit(1);
  }
  console.log('✓ Conectado a pau_biologia.db\n');
});

function importExams() {
  console.log('📥 IMPORTANDO EXÁMENES A BD\n');
  
  const rawData = fs.readFileSync(jsonPath, 'utf-8');
  const allExams = JSON.parse(rawData);
  
  let examCount = 0;
  let questionCount = 0;
  let apartadoCount = 0;
  
  db.serialize(() => {
    Object.entries(allExams).forEach(([year, yearExams]) => {
      Object.entries(yearExams).forEach(([letter, examData]) => {
        const examId = `${year}_EXM_${letter}`;
        const pdfPath = examData.pdf_path;
        
        console.log(`📅 ${year} - Examen ${letter}`);
        
        db.run(
          `INSERT OR REPLACE INTO exams (id, year, exam_letter, pdf_path) 
           VALUES (?, ?, ?, ?)`,
          [examId, parseInt(year), letter, pdfPath],
          function(err) {
            if (err) {
              console.error(`  ✗ Error insertando examen: ${err}`);
            } else {
              examCount++;
              console.log(`  ✓ Examen ${examId} insertado`);
              
              examData.questions.forEach((question) => {
                const questionId = `${year}_EXM_${letter}_Q${question.number}`;
                
                db.run(
                  `INSERT OR REPLACE INTO questions 
                   (id, exam_id, question_number, bloque, text) 
                   VALUES (?, ?, ?, ?, ?)`,
                  [questionId, examId, question.number, question.bloque, question.text],
                  function(err) {
                    if (err) {
                      console.error(`    ✗ Error en pregunta ${question.number}: ${err}`);
                    } else {
                      questionCount++;
                      
                      if (question.apartados && question.apartados.length > 0) {
                        question.apartados.forEach((apartado) => {
                          const apartadoId = `${questionId}_${apartado.label}`;
                          
                          db.run(
                            `INSERT OR REPLACE INTO apartados 
                             (id, question_id, label, text, points) 
                             VALUES (?, ?, ?, ?, ?)`,
                            [apartadoId, questionId, apartado.label, apartado.text, apartado.points],
                            function(err) {
                              if (err) {
                                console.error(`      ✗ Error apartado ${apartado.label}: ${err}`);
                              } else {
                                apartadoCount++;
                              }
                            }
                          );
                        });
                      }
                    }
                  }
                );
              });
              
              if (examData.images && examData.images.length > 0) {
                examData.images.forEach((img) => {
                  const imgId = `${examId}_${img.id}`;
                  
                  db.run(
                    `INSERT OR REPLACE INTO images (id, exam_id, page_number) 
                     VALUES (?, ?, ?)`,
                    [imgId, examId, img.page],
                    function(err) {
                      if (err) {
                        console.error(`    ✗ Error imagen: ${err}`);
                      }
                    }
                  );
                });
              }
            }
          }
        );
      });
    });
  });
  
  setTimeout(() => {
    db.all(`SELECT COUNT(*) as count FROM exams`, [], (err, rows) => {
      const examsCount = rows[0].count;
      
      db.all(`SELECT COUNT(*) as count FROM questions`, [], (err, rows) => {
        const questionsCount = rows[0].count;
        
        db.all(`SELECT COUNT(*) as count FROM apartados`, [], (err, rows) => {
          const apartadosCount = rows[0].count;
          
          db.all(`SELECT COUNT(*) as count FROM images`, [], (err, rows) => {
            const imagesCount = rows[0].count;
            
            console.log(`\n${'='*60}`);
            console.log(`✅ IMPORTACIÓN COMPLETADA`);
            console.log(`${'='*60}`);
            console.log(`  • Exámenes: ${examsCount}`);
            console.log(`  • Preguntas: ${questionsCount}`);
            console.log(`  • Apartados: ${apartadosCount}`);
            console.log(`  • Imágenes: ${imagesCount}`);
            console.log(`${'='*60}\n`);
            
            db.close();
          });
        });
      });
    });
  }, 2000);
}

importExams();
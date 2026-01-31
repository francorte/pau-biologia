import sqlite3 from 'sqlite3';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const DB_PATH = path.join(__dirname, 'db', 'pau_biologia.db');
const IMAGES_BASE_DIR = path.join(__dirname, 'manual_images', '2025');
const PUBLIC_BASE_DIR = path.join(__dirname, 'public', 'exam_images', '2025');

const EXAM_CONFIGS = [
  {
    letter: 'A',
    year: 2025,
    images: [
      { filename: 'A_1.png', question_number: 1, new_name: 'P1_expresion_genica.png', description: 'Expresión génica', elements: 'ADN, ARN, Ribosoma' },
      { filename: 'A_2.1.png', question_number: 2, new_name: 'P2_1_estructuras_proteicas.png', description: 'Estructuras proteicas', elements: 'Primaria, secundaria' },
      { filename: 'A_2.2.png', question_number: 3, new_name: 'P2_2_molecula_adn.png', description: 'Molécula de ADN', elements: 'Nucleótidos' },
      { filename: 'A_4.1.png', question_number: 6, new_name: 'P4_1_respuesta_alergica.png', description: 'Respuesta alérgica', elements: 'Inmunoglobulinas' },
      { filename: 'A_4.2.png', question_number: 7, new_name: 'P4_2_respuesta_inmune.png', description: 'Tipos de inmunidad', elements: 'Innata, adaptativa' }
    ]
  },
  {
    letter: 'B',
    year: 2025,
    images: [
      { filename: 'B_1.png', question_number: 1, new_name: 'P1_imagen_B.png', description: 'Pregunta 1 B', elements: 'Elementos' },
      { filename: 'B_3.1.png', question_number: 4, new_name: 'P3_1_imagen_B.png', description: 'Pregunta 3.1 B', elements: 'Elementos' },
      { filename: 'B_3.2.png', question_number: 5, new_name: 'P3_2_imagen_B.png', description: 'Pregunta 3.2 B', elements: 'Elementos' }
    ]
  },
  {
    letter: 'C',
    year: 2025,
    images: [
      { filename: 'C_1.png', question_number: 1, new_name: 'P1_imagen_C.png', description: 'Pregunta 1 C', elements: 'Elementos' },
      { filename: 'C_3.1.png', question_number: 4, new_name: 'P3_1_imagen_C.png', description: 'Pregunta 3.1 C', elements: 'Elementos' },
      { filename: 'C_3.2.png', question_number: 5, new_name: 'P3_2_imagen_C.png', description: 'Pregunta 3.2 C', elements: 'Elementos' }
    ]
  },
  {
    letter: 'D',
    year: 2025,
    images: [
      { filename: 'D_1.png', question_number: 1, new_name: 'P1_imagen_D.png', description: 'Pregunta 1 D', elements: 'Elementos' },
      { filename: 'D_3.1.png', question_number: 4, new_name: 'P3_1_imagen_D.png', description: 'Pregunta 3.1 D', elements: 'Elementos' },
      { filename: 'D_3.2.png', question_number: 5, new_name: 'P3_2_imagen_D.png', description: 'Pregunta 3.2 D', elements: 'Elementos' },
      { filename: 'D_5.1.png', question_number: 8, new_name: 'P5_1_imagen_D.png', description: 'Pregunta 5.1 D', elements: 'Elementos' },
      { filename: 'D_5.2.png', question_number: 9, new_name: 'P5_2_imagen_D.png', description: 'Pregunta 5.2 D', elements: 'Elementos' }
    ]
  }
];

console.log('🚀 IMPORTADOR DE IMÁGENES\n');

const db = new sqlite3.Database(DB_PATH, (err) => {
  if (err) {
    console.error('❌ Error BD:', err.message);
    process.exit(1);
  }
  console.log('✅ Conectado\n');
});

db.run(`
  CREATE TABLE IF NOT EXISTS question_images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id INTEGER NOT NULL,
    image_filename TEXT NOT NULL,
    image_path TEXT NOT NULL,
    description TEXT,
    elements TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE(question_id)
  )
`, (err) => {
  if (err) {
    console.error('❌ Tabla:', err.message);
    db.close();
    process.exit(1);
  }
  console.log('✅ Tabla OK\n');
  processAllExams();
});

async function processAllExams() {
  let totalProcessed = 0;
  let totalErrors = 0;
  
  for (const examConfig of EXAM_CONFIGS) {
    console.log(`\n${'='.repeat(50)}`);
    console.log(`📝 EXAMEN ${examConfig.letter}`);
    console.log('='.repeat(50));
    
    const examId = await getExamId(examConfig.letter, examConfig.year);
    
    if (!examId) {
      console.log(`⚠️  No encontrado en BD\n`);
      totalErrors++;
      continue;
    }
    
    console.log(`✅ ID: ${examId}`);
    
    const sourceDir = path.join(IMAGES_BASE_DIR, `Examen${examConfig.letter}`);
    const targetDir = path.join(PUBLIC_BASE_DIR, `Examen${examConfig.letter}`);
    
    if (!fs.existsSync(targetDir)) {
      fs.mkdirSync(targetDir, { recursive: true });
    }
    
    for (let i = 0; i < examConfig.images.length; i++) {
      const img = examConfig.images[i];
      const sourcePath = path.join(sourceDir, img.filename);
      const targetPath = path.join(targetDir, img.new_name);
      const webPath = `/exam_images/2025/Examen${examConfig.letter}/${img.new_name}`;
      
      console.log(`[${i + 1}/${examConfig.images.length}] ${img.filename}`);
      
      if (!fs.existsSync(sourcePath)) {
        console.log(`   ⚠️  No encontrado`);
        totalErrors++;
        continue;
      }
      
      try {
        fs.copyFileSync(sourcePath, targetPath);
        console.log(`   ✅ Copiada`);
      } catch (err) {
        console.error(`   ❌ Error:`, err.message);
        totalErrors++;
        continue;
      }
      
      const inserted = await insertImage(examId, img.question_number, img.new_name, webPath, img.description, img.elements);
      
      if (inserted) {
        console.log(`   💾 BD OK (P${img.question_number})`);
        totalProcessed++;
      } else {
        console.log(`   ⚠️  BD Error`);
        totalErrors++;
      }
    }
  }
  
  console.log('\n' + '='.repeat(50));
  console.log('✅ COMPLETADO');
  console.log('='.repeat(50));
  console.log(`  • Procesadas: ${totalProcessed}`);
  console.log(`  • Errores: ${totalErrors}`);
  console.log('='.repeat(50) + '\n');
  
  db.close();
}

function getExamId(letter, year) {
  return new Promise((resolve) => {
    db.get(`SELECT id FROM exams WHERE year = ? AND exam_letter = ?`, [year, letter], (err, row) => {
      resolve(row ? row.id : null);
    });
  });
}

function insertImage(examId, questionNumber, filename, webPath, description, elements) {
  return new Promise((resolve) => {
    db.run(`
      INSERT OR REPLACE INTO question_images 
      (question_id, image_filename, image_path, description, elements)
      SELECT q.id, ?, ?, ?, ?
      FROM questions q
      WHERE q.exam_id = ? AND q.question_number = ?
    `, [filename, webPath, description, elements, examId, questionNumber], function(err) {
      resolve(err ? false : this.changes > 0);
    });
  });
}
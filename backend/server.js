import express from 'express';
import cors from 'cors';
import sqlite3 from 'sqlite3';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json());
app.use(express.static('public'));

const dbPath = path.join(__dirname, 'db', 'pau_biologia.db');
let db = null;

function initDB() {
  return new Promise((resolve, reject) => {
    db = new sqlite3.Database(dbPath, (err) => {
      if (err) reject(err);
      else { console.log('✓ BD conectada'); resolve(); }
    });
  });
}

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

app.get('/api/health', (req, res) => {
  res.json({ status: 'OK' });
});

app.get('/api/bloques', (req, res) => {
  const bloques = [
    { id: 'A', nombre: 'Bloque A: Las biomoléculas' },
    { id: 'B', nombre: 'Bloque B: Genética molecular' },
    { id: 'C', nombre: 'Bloque C: Biología celular' },
    { id: 'D', nombre: 'Bloque D: Metabolismo' },
    { id: 'E', nombre: 'Bloque E: Biotecnología' },
    { id: 'F', nombre: 'Bloque F: Inmunología' }
  ];
  res.json(bloques);
});

app.get('/api/questions/by-bloque/:bloque', (req, res) => {
  db.all('SELECT id, question_number, question_label, bloque, total_points FROM questions WHERE bloque = ? ORDER BY question_number', [req.params.bloque], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.get('/api/questions/:question_id', (req, res) => {
  db.get('SELECT id, question_number, question_label, question_text, bloque, total_points FROM questions WHERE id = ?', [req.params.question_id], (err, question) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!question) return res.status(404).json({ message: 'Not found' });
    
    db.all('SELECT apartado_letter, apartado_text, points FROM apartados WHERE question_id = ? ORDER BY apartado_letter', [req.params.question_id], (err, apartados) => {
      if (err) return res.status(500).json({ error: err.message });
      
      db.get('SELECT image_filename, image_path FROM question_images WHERE question_id = ?', [req.params.question_id], (err, image) => {
        if (err) return res.status(500).json({ error: err.message });
        
        res.json({
          ...question,
          apartados: apartados || [],
          image: image || null
        });
      });
    });
  });
});

async function start() {
  try {
    await initDB();
    app.listen(PORT, () => {
      console.log('\n✓ BD conectada');
      console.log('\n🚀 Servidor PAU Biología en http://localhost:3000\n');
    });
  } catch (err) {
    console.error('❌ Error:', err.message);
    process.exit(1);
  }
}

start();

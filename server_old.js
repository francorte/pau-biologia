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
      else { console.log('✓ BD OK'); resolve(); }
    });
  });
}

app.get('/api/health', (req, res) => res.json({ status: 'OK' }));
app.get('/api/stats', (req, res) => {
  if (!db) return res.status(500).json({ error: 'BD no inicializada' });
  db.all('SELECT (SELECT COUNT(*) FROM exams) as total_exams', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows[0]);
  });
});

app.get('/api/exams', (req, res) => {
  if (!db) return res.status(500).json({ error: 'BD no inicializada' });
  db.all('SELECT * FROM exams ORDER BY year DESC', [], (err, rows) => {
    if (err) return res.status(500).json({ error: err.message });
    res.json(rows);
  });
});

app.get('/api/question/:id/image', (req, res) => {
  if (!db) return res.status(500).json({ error: 'BD no inicializada' });
  db.get('SELECT * FROM question_images WHERE question_id = ?', [req.params.id], (err, row) => {
    if (err) return res.status(500).json({ error: err.message });
    if (!row) return res.status(404).json({ message: 'Sin imagen' });
    res.json(row);
  });
});

async function start() {
  try {
    await initDB();
    app.listen(PORT, () => console.log('🚀 http://localhost:3000\n📁 Static: public/*'));
  } catch (err) {
    console.error('❌', err.message);
    process.exit(1);
  }
}

start();

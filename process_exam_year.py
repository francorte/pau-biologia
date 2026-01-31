#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script simplificado para vincular imágenes con preguntas existentes en la BD
"""

import sqlite3
import shutil
import argparse
from pathlib import Path

class ImageLinker:
    def __init__(self, year, input_dir, db_path='db/pau_biologia.db', output_images='public/exam_images'):
        self.year = year
        self.input_dir = Path(input_dir)
        self.db_path = Path(db_path)
        self.output_images = Path(output_images) / str(year)
        
        # Crear carpeta de salida
        self.output_images.mkdir(parents=True, exist_ok=True)
        
        print(f"\n🔗 VINCULADOR DE IMÁGENES - AÑO {year}")
        print(f"📂 Carpeta imágenes: {self.input_dir}")
        print(f"💾 Base de datos: {self.db_path}")
        print(f"📤 Salida: {self.output_images}\n")
    
    def parse_image_filename(self, filename):
        """
        Parsea nombres como: A_1_2025.png, B_3.1_2025.png
        Retorna: (letra_examen, numero_pregunta)
        """
        parts = filename.stem.split('_')
        if len(parts) >= 2:
            exam_letter = parts[0]  # A, B, C, D
            question_label = parts[1]  # 1, 2.1, 3.2, etc.
            return exam_letter, question_label
        return None, None
    
    def get_question_id(self, cursor, exam_letter, question_label):
        """Obtiene el ID de la pregunta desde la BD"""
        exam_id = f"{self.year}_EXM_{exam_letter}"
        
        # Buscar por question_number directamente
        cursor.execute("""
            SELECT id, question_number 
            FROM questions 
            WHERE exam_id = ?
            ORDER BY question_number
        """, (exam_id,))
        
        questions = cursor.fetchall()
        
        # Mapear el label a question_number
        # Ejemplo: A_1 → pregunta 1, A_2.1 → pregunta 2, A_2.2 → pregunta 3
        label_to_qnum = {
            '1': 1,
            '2.1': 2, '2.2': 3,
            '3.1': 4, '3.2': 5,
            '4.1': 6, '4.2': 7,
            '5.1': 8, '5.2': 9,
        }
        
        target_qnum = label_to_qnum.get(question_label)
        
        if target_qnum:
            for qid, qnum in questions:
                if qnum == target_qnum:
                    return qid
        
        return None
    
    def process_images(self):
        """Procesa todas las imágenes PNG en la carpeta"""
        
        # Conectar a BD
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Crear tabla si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question_id TEXT NOT NULL,
                image_filename TEXT NOT NULL,
                image_path TEXT NOT NULL,
                description TEXT,
                elements TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(question_id)
            )
        """)
        conn.commit()
        
        # Buscar imágenes
        images = list(self.input_dir.glob(f"*_{self.year}.png"))
        
        if not images:
            print(f"⚠️  No se encontraron imágenes con patrón *_{self.year}.png")
            print(f"Archivos en carpeta:")
            for f in self.input_dir.iterdir():
                print(f"  - {f.name}")
            return
        
        print(f"📸 Encontradas {len(images)} imágenes\n")
        
        stats = {'vinculadas': 0, 'sin_pregunta': 0, 'errores': 0}
        
        for image_path in sorted(images):
            exam_letter, question_label = self.parse_image_filename(image_path)
            
            if not exam_letter or not question_label:
                print(f"⚠️  {image_path.name}: Formato incorrecto")
                stats['errores'] += 1
                continue
            
            # Buscar pregunta en BD
            question_id = self.get_question_id(cursor, exam_letter, question_label)
            
            if not question_id:
                print(f"⚠️  {image_path.name}: No se encontró pregunta (Examen {exam_letter}, P{question_label})")
                stats['sin_pregunta'] += 1
                continue
            
            # Copiar imagen
            new_filename = f"{exam_letter}_{question_label}.png"
            output_path = self.output_images / new_filename
            shutil.copy2(image_path, output_path)
            
            web_path = f"/exam_images/{self.year}/{new_filename}"
            
            # Insertar en BD
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO question_images 
                    (question_id, image_filename, image_path, description, elements)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    question_id,
                    new_filename,
                    web_path,
                    f"Examen {exam_letter} - Pregunta {question_label}",
                    ""
                ))
                
                print(f"✅ {image_path.name} → Pregunta {question_id}")
                stats['vinculadas'] += 1
                
            except sqlite3.Error as e:
                print(f"❌ {image_path.name}: Error BD - {e}")
                stats['errores'] += 1
        
        conn.commit()
        conn.close()
        
        # Resumen
        print("\n" + "=" * 50)
        print("✅ PROCESO COMPLETADO")
        print("=" * 50)
        print(f"  • Imágenes vinculadas: {stats['vinculadas']}")
        print(f"  • Sin pregunta asociada: {stats['sin_pregunta']}")
        print(f"  • Errores: {stats['errores']}")
        print("=" * 50 + "\n")

def main():
    parser = argparse.ArgumentParser(description='Vincula imágenes con preguntas en la BD')
    parser.add_argument('--year', type=int, required=True, help='Año (ej: 2025)')
    parser.add_argument('--input', type=str, required=True, help='Carpeta con imágenes')
    parser.add_argument('--db', type=str, default='db/pau_biologia.db', help='Ruta BD')
    parser.add_argument('--output', type=str, default='public/exam_images', help='Salida')
    
    args = parser.parse_args()
    
    linker = ImageLinker(
        year=args.year,
        input_dir=args.input,
        db_path=args.db,
        output_images=args.output
    )
    
    linker.process_images()

if __name__ == "__main__":
    main()
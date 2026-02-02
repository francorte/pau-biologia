#!/usr/bin/env python3
import sqlite3
from pathlib import Path
from config import PUBLIC_IMAGES_DIR, DB_PATH, YEAR, LABEL_TO_QUESTION_NUMBER

class ImageLinker:
    def __init__(self):
        self.db_path = DB_PATH
        self.images_dir = PUBLIC_IMAGES_DIR / str(YEAR)
    
    def link_images(self):
        print(f"\n🔗 VINCULANDO IMÁGENES A PREGUNTAS\n")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Buscar imágenes
        images = list(self.images_dir.glob("*.png"))
        
        if not images:
            print(f"⚠️  No hay imágenes en {self.images_dir}")
            return
        
        print(f"Encontradas {len(images)} imágenes\n")
        
        linked = 0
        errors = 0
        
        for image_path in sorted(images):
            # Parsear nombre: B_3.2_2025.png
            parts = image_path.stem.split('_')
            
            if len(parts) < 2:
                print(f"⚠️  {image_path.name}: Formato inválido")
                errors += 1
                continue
            
            exam_letter = parts[0]  # A, B, C, D
            question_label = parts[1]  # 1, 2.1, 3.2, etc.
            
            # Convertir label a question_number
            question_number = LABEL_TO_QUESTION_NUMBER.get(question_label)
            
            if not question_number:
                print(f"⚠️  {image_path.name}: Label no reconocido ({question_label})")
                errors += 1
                continue
            
            # Buscar pregunta en BD
            exam_id = f"{YEAR}_EXM_{exam_letter}"
            question_id = f"{exam_id}_Q{question_number}"
            
            cursor.execute("SELECT id FROM questions WHERE id = ?", (question_id,))
            result = cursor.fetchone()
            
            if not result:
                print(f"⚠️  {image_path.name}: Pregunta no encontrada ({question_id})")
                errors += 1
                continue
            
            # Insertar en BD
            web_path = f"/exam_images/{YEAR}/{image_path.name}"
            
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO question_images 
                    (question_id, image_filename, image_path, description)
                    VALUES (?, ?, ?, ?)
                """, (
                    question_id,
                    image_path.name,
                    web_path,
                    f"Pregunta {question_label}"
                ))
                
                print(f"✓ {exam_letter}_{question_label} → {question_id}")
                linked += 1
            
            except Exception as e:
                print(f"✗ {image_path.name}: {e}")
                errors += 1
        
        conn.commit()
        conn.close()
        
        print(f"\n{'='*60}")
        print(f"✅ IMÁGENES VINCULADAS")
        print(f"{'='*60}")
        print(f"  • Vinculadas: {linked}")
        print(f"  • Errores: {errors}")
        print(f"  • Total: {linked + errors}\n")

if __name__ == "__main__":
    linker = ImageLinker()
    linker.link_images()

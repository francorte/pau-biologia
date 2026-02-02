#!/usr/bin/env python3
import csv
import sqlite3
from config import DB_PATH

def load_images_from_csv(csv_file):
    print(f"\n📸 CARGANDO IMÁGENES DESDE {csv_file}\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        for i, row in enumerate(reader, 1):
            ruta_imagen = row.get('Ruta Imagen', '').strip()
            
            if not ruta_imagen:
                print(f"⊘ Fila {i}: Sin ruta de imagen")
                continue
            
            exam_letter = row['Examen'].strip()
            q_number = int(row['Pregunta #'].strip())
            nombre_imagen = row.get('Nombre Imagen (ej: A_1_2025.png)', '').strip()
            
            exam_id = f"2025_EXM_{exam_letter}"
            question_id = f"{exam_id}_Q{q_number}"
            
            # Insertar en BD
            try:
                cursor.execute("""
                    INSERT OR REPLACE INTO question_images 
                    (question_id, image_filename, image_path, description)
                    VALUES (?, ?, ?, ?)
                """, (
                    question_id,
                    nombre_imagen,
                    ruta_imagen,
                    f"Pregunta {row['Label'].strip()}"
                ))
                
                print(f"✓ {exam_letter}Q{q_number}: {ruta_imagen}")
            
            except Exception as e:
                print(f"✗ Fila {i}: {e}")
    
    conn.commit()
    conn.close()
    
    print(f"\n✅ IMÁGENES CARGADAS A BD\n")

if __name__ == "__main__":
    import sys
    csv_file = sys.argv[1] if len(sys.argv) > 1 else "preguntas_pau_2025_COMPLETADO.csv"
    load_images_from_csv(csv_file)

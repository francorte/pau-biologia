import sqlite3
import pdfplumber
import base64
import os
from pathlib import Path

DB_PATH = 'db/pau_biologia.db'
PDF_DIR = Path(os.path.expanduser('~/Desktop/Biología'))

def encode_image_to_base64(image_bytes):
    """Convierte bytes de imagen a base64"""
    return base64.b64encode(image_bytes).decode('utf-8')

def extract_images_from_pdf(pdf_path, exam_id):
    """Extrae imágenes de un PDF y las guarda en BD"""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            images_count = 0
            
            for page_num, page in enumerate(pdf.pages, 1):
                # Obtener todas las imágenes de la página
                for img in page.images:
                    try:
                        # Extraer imagen como bytes
                        img_stream = img['stream'].get_data()
                        
                        # Convertir a base64
                        img_base64 = encode_image_to_base64(img_stream)
                        
                        # Guardar en BD
                        cursor = db.cursor()
                        cursor.execute('''
                            INSERT INTO images (exam_id, page_number, image_data)
                            VALUES (?, ?, ?)
                        ''', (exam_id, page_num, img_base64))
                        db.commit()
                        
                        images_count += 1
                        print(f"  ✓ Imagen {images_count} guardada (página {page_num})")
                        
                    except Exception as e:
                        print(f"  ⚠ Error procesando imagen en página {page_num}: {e}")
                        continue
            
            return images_count
            
    except Exception as e:
        print(f"❌ Error abriendo PDF {pdf_path}: {e}")
        return 0

# Conectar a BD
db = sqlite3.connect(DB_PATH)
db.row_factory = sqlite3.Row

print("🖼️ EXTRACCIÓN DE IMÁGENES A BASE64")
print("=" * 60)

try:
    # Obtener exámenes de BD
    cursor = db.cursor()
    cursor.execute('SELECT id, year, exam_letter, pdf_path FROM exams ORDER BY year DESC')
    exams = cursor.fetchall()
    
    if not exams:
        print("❌ No hay exámenes en la BD")
        exit(1)
    
    total_images = 0
    
    for exam in exams:
        exam_id = exam['id']
        year = exam['year']
        exam_letter = exam['exam_letter']
        pdf_path = exam['pdf_path']
        
        # Buscar el PDF
        if os.path.exists(pdf_path):
            print(f"\n📅 {year} - Examen {exam_letter}")
            print(f"   📄 {pdf_path}")
            
            images_count = extract_images_from_pdf(pdf_path, exam_id)
            total_images += images_count
            
            print(f"   ✅ Total: {images_count} imágenes")
        else:
            print(f"\n⚠️ {year} - Examen {exam_letter}: PDF no encontrado")
    
    print("\n" + "=" * 60)
    print(f"✅ EXTRACCIÓN COMPLETADA")
    print(f"   Total imágenes guardadas: {total_images}")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    db.close()
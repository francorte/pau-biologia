#!/usr/bin/env python3
import shutil
from pathlib import Path
from config import INPUT_DIR, PUBLIC_IMAGES_DIR, YEAR, LABEL_TO_QUESTION_NUMBER

class ImageHandler:
    def __init__(self):
        self.stats = {'found': 0, 'copied': 0, 'errors': 0}
    
    def parse_image_filename(self, filename):
        parts = filename.stem.split('_')
        if len(parts) >= 3:
            exam_letter = parts[0]
            question_label = parts[1]
            year = int(parts[2]) if len(parts) > 2 else YEAR
            
            if exam_letter not in ['A', 'B', 'C', 'D']:
                return None, None, None
            
            return exam_letter, question_label, year
        
        return None, None, None
    
    def copy_and_organize(self):
        print(f"\n📸 ORGANIZANDO IMÁGENES {YEAR}\n")
        
        images = sorted(INPUT_DIR.glob(f"*_{YEAR}.png"))
        
        if not images:
            print(f"⚠ No hay imágenes con patrón *_{YEAR}.png")
            return
        
        print(f"Encontradas {len(images)} imágenes\n")
        self.stats['found'] = len(images)
        
        year_dir = PUBLIC_IMAGES_DIR / str(YEAR)
        year_dir.mkdir(parents=True, exist_ok=True)
        
        for image_path in images:
            exam_letter, question_label, year = self.parse_image_filename(image_path)
            
            if not exam_letter:
                print(f"⚠ {image_path.name}: Formato incorrecto")
                self.stats['errors'] += 1
                continue
            
            if question_label not in LABEL_TO_QUESTION_NUMBER:
                print(f"⚠ {image_path.name}: Label no reconocido")
                self.stats['errors'] += 1
                continue
            
            new_filename = f"{exam_letter}_{question_label}_{YEAR}.png"
            output_path = year_dir / new_filename
            
            try:
                shutil.copy2(image_path, output_path)
                print(f"✓ {image_path.name}")
                self.stats['copied'] += 1
            except Exception as e:
                print(f"✗ {image_path.name}: {e}")
                self.stats['errors'] += 1
        
        print(f"\n{'='*60}")
        print(f"✅ IMÁGENES PROCESADAS")
        print(f"{'='*60}")
        print(f"  • Encontradas: {self.stats['found']}")
        print(f"  • Copiadas: {self.stats['copied']}")
        print(f"  • Errores: {self.stats['errors']}")
        print(f"  • Destino: {year_dir}\n")

if __name__ == "__main__":
    handler = ImageHandler()
    handler.copy_and_organize()

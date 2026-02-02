#!/usr/bin/env python3
import pdfplumber
import json
import re
from pathlib import Path
from config import INPUT_DIR, EXTRACTED_EXAMS_DIR, YEAR, EXAM_CONFIG, BLOQUE_KEYWORDS, LABEL_TO_QUESTION_NUMBER

class PDFExtractor:
    def __init__(self):
        self.stats = {'pdfs_processed': 0, 'total_questions': 0, 'total_images': 0}
    
    def classify_by_bloque(self, text):
        text_lower = text.lower()
        for bloque, keywords in BLOQUE_KEYWORDS.items():
            if any(kw in text_lower for kw in keywords):
                return bloque
        return None
    
    def extract_questions_from_text(self, text):
        questions = []
        pregunta_pattern = r'Pregunta\s+([\d\.]+)\s*\((\d+)\s*puntos?\)'
        ejercicio_splits = re.split(r'EJERCICIO\s+\d+', text)
        question_counter = 0
        
        for ejercicio_idx, ejercicio_section in enumerate(ejercicio_splits[1:], 1):
            pregunta_matches = re.finditer(pregunta_pattern, ejercicio_section)
            
            for pregunta_match in pregunta_matches:
                question_counter += 1
                pregunta_label = pregunta_match.group(1)
                total_points = float(pregunta_match.group(2)) if pregunta_match.group(2) else 2.0
                
                start_pos = pregunta_match.end()
                siguiente_pregunta = re.search(pregunta_pattern, ejercicio_section[start_pos:])
                end_pos = start_pos + siguiente_pregunta.start() if siguiente_pregunta else len(ejercicio_section)
                
                pregunta_texto_section = ejercicio_section[start_pos:end_pos]
                lines = pregunta_texto_section.split('\n')
                pregunta_text_lines = []
                apartados_start_idx = 0
                
                for i, line in enumerate(lines):
                    if re.match(r'^\s*a\)', line):
                        apartados_start_idx = i
                        break
                    pregunta_text_lines.append(line)
                
                pregunta_text = ' '.join(pregunta_text_lines).strip()
                apartados = []
                apartados_section = '\n'.join(lines[apartados_start_idx:])
                apartado_pattern = r'([a-f])\)\s*([^[]*)?\s*\[(\d+[.,]\d+)\]'
                
                for apt_match in re.finditer(apartado_pattern, apartados_section):
                    label = apt_match.group(1)
                    apt_text = apt_match.group(2).strip() if apt_match.group(2) else ""
                    apt_points = float(apt_match.group(3).replace(',', '.'))
                    
                    apartados.append({
                        'label': label,
                        'text': apt_text,
                        'points': apt_points
                    })
                
                if apartados or pregunta_text:
                    questions.append({
                        'number': question_counter,
                        'label': pregunta_label,
                        'text': pregunta_text,
                        'total_points': total_points,
                        'apartados': apartados
                    })
        
        return questions
    
    def extract_from_pdf(self, pdf_path, exam_letter):
        result = {
            'exam_id': f"{YEAR}_EXM_{exam_letter}",
            'exam_letter': exam_letter,
            'year': YEAR,
            'questions': [],
            'images_detected': 0,
        }
        
        try:
            print(f"  → Procesando {pdf_path.name}...", end=" ")
            
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page in pdf.pages:
                    text = page.extract_text() or ""
                    full_text += text + "\n"
                    result['images_detected'] += len(page.images)
                
                questions = self.extract_questions_from_text(full_text)
                
                for q in questions:
                    q['bloque'] = self.classify_by_bloque(q['text'])
                
                result['questions'] = questions
                self.stats['total_questions'] += len(questions)
                self.stats['total_images'] += result['images_detected']
            
            print(f"✓ ({len(questions)} preguntas)")
            return result
        
        except Exception as e:
            print(f"✗ Error: {e}")
            return None
    
    def process_all_exams(self):
        print(f"\n📊 EXTRAYENDO EXÁMENES {YEAR}\n")
        
        all_exams = {}
        
        for exam_letter, config in sorted(EXAM_CONFIG.items()):
            pdf_path = INPUT_DIR / config['file']
            
            if not pdf_path.exists():
                print(f"⚠ No encontrado: {config['file']}")
                continue
            
            exam_data = self.extract_from_pdf(pdf_path, exam_letter)
            
            if exam_data:
                all_exams[exam_letter] = exam_data
                self.stats['pdfs_processed'] += 1
        
        output_file = EXTRACTED_EXAMS_DIR / f"exams_{YEAR}.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_exams, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✅ EXTRACCIÓN COMPLETADA")
        print(f"{'='*60}")
        print(f"  • PDFs: {self.stats['pdfs_processed']}")
        print(f"  • Preguntas: {self.stats['total_questions']}")
        print(f"  • Imágenes: {self.stats['total_images']}")
        print(f"  • Salida: {output_file}\n")
        
        return all_exams, self.stats

if __name__ == "__main__":
    extractor = PDFExtractor()
    exams, stats = extractor.process_all_exams()

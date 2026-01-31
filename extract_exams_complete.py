#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pdfplumber
import json
import re
from pathlib import Path
from datetime import datetime
import sys

class PAUExamExtractor:
    def __init__(self, base_dir="/Users/franciscodelacorte/Desktop/Biología"):
        self.base_dir = Path(base_dir)
        self.output_dir = Path("extracted_exams")
        self.output_dir.mkdir(exist_ok=True)
        
        self.bloque_keywords = {
            'A': ['biomolécula', 'proteína', 'lípido', 'glúcido', 'ácido nucleico', 'agua', 'enlace', 'enzima', 'aminoácido', 'fosfolípido', 'gen', 'expresión genética'],
            'B': ['replicación', 'transcripción', 'traducción', 'gen', 'mutación', 'expresión génica', 'promotor', 'operón', 'insulina', 'transcriptasa'],
            'C': ['membrana', 'célula', 'mitosis', 'meiosis', 'orgánulo', 'ciclo celular', 'núcleo', 'ribosoma', 'glóbulos rojos', 'cromosomas'],
            'D': ['metabolismo', 'respiración', 'fotosíntesis', 'glucólisis', 'energía', 'ATP', 'fermentación', 'ciclo de krebs', 'beta-oxidación', 'ácidos grasos'],
            'E': ['biotecnología', 'PCR', 'CRISPR', 'ADN recombinante', 'OMG', 'clonación', 'ingeniería genética'],
            'F': ['inmunidad', 'anticuerpo', 'inmunoglobulina', 'linfocito', 'antígeno', 'trasplante', 'inmune', 'alérgica', 'abejas', 'respuesta alérgica']
        }
    
    def classify_by_bloque(self, text):
        text_lower = text.lower()
        for bloque, keywords in self.bloque_keywords.items():
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
                total_points_str = pregunta_match.group(2)
                total_points = float(total_points_str) if total_points_str else 2.0
                
                start_pos = pregunta_match.end()
                
                siguiente_pregunta = re.search(pregunta_pattern, ejercicio_section[start_pos:])
                if siguiente_pregunta:
                    end_pos = start_pos + siguiente_pregunta.start()
                else:
                    end_pos = len(ejercicio_section)
                
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
                    apt_points_str = apt_match.group(3).replace(',', '.')
                    apt_points = float(apt_points_str)
                    
                    apartados.append({
                        'label': label,
                        'text': apt_text,
                        'points': apt_points
                    })
                
                if apartados or pregunta_text:
                    questions.append({
                        'number': question_counter,
                        'label': pregunta_label,
                        'ejercicio': ejercicio_idx,
                        'text': pregunta_text,
                        'total_points': total_points,
                        'apartados': apartados
                    })
        
        return questions
    
    def extract_exam_pdf(self, pdf_path):
        result = {
            'pdf_path': str(pdf_path),
            'pages': [],
            'questions': [],
            'images': []
        }
        
        try:
            with pdfplumber.open(pdf_path) as pdf:
                full_text = ""
                for page_idx, page in enumerate(pdf.pages):
                    text = page.extract_text() or ""
                    full_text += text + "\n"
                    
                    result['pages'].append({
                        'number': page_idx + 1,
                        'text': text
                    })
                    
                    for img_idx, img in enumerate(page.images):
                        image_id = f"IMG_P{page_idx + 1}_{img_idx}"
                        result['images'].append({
                            'id': image_id,
                            'page': page_idx + 1,
                            'bbox': img.get('bbox', None)
                        })
                
                questions = self.extract_questions_from_text(full_text)
                
                for q in questions:
                    q['bloque'] = self.classify_by_bloque(q['text'])
                
                result['questions'] = questions
        
        except Exception as e:
            print(f"  ✗ Error procesando {pdf_path}: {e}")
            return None
        
        return result
    
    def process_all_exams(self):
        print(f"\n📊 INGESTIÓN DE EXÁMENES PAU\n")
        print(f"Buscando exámenes en: {self.base_dir}")
        
        all_exams = {}
        stats = {
            'total_files': 0,
            'processed': 0,
            'errors': 0,
            'total_questions': 0,
            'total_images': 0
        }
        
        year_dirs = sorted([d for d in self.base_dir.iterdir() if d.is_dir()])
        
        for year_dir in year_dirs:
            year = year_dir.name
            print(f"\n📅 Año {year}")
            
            pdf_files = sorted(year_dir.glob("Examen_*.pdf"))
            
            if not pdf_files:
                print(f"  ⚠ No se encontraron PDFs")
                continue
            
            year_exams = {}
            
            for pdf_file in pdf_files:
                stats['total_files'] += 1
                
                letter_match = re.search(r'Examen_([A-D])_', pdf_file.name)
                exam_letter = letter_match.group(1) if letter_match else "?"
                
                print(f"  → Procesando Examen_{exam_letter}_{year}.pdf...", end=" ")
                
                exam_data = self.extract_exam_pdf(pdf_file)
                
                if exam_data:
                    exam_data['year'] = int(year)
                    exam_data['exam_letter'] = exam_letter
                    exam_data['exam_id'] = f"{year}_EXM_{exam_letter}"
                    
                    year_exams[exam_letter] = exam_data
                    stats['processed'] += 1
                    stats['total_questions'] += len(exam_data['questions'])
                    stats['total_images'] += len(exam_data['images'])
                    
                    print(f"✓ ({len(exam_data['questions'])} preguntas, {len(exam_data['images'])} imágenes)")
                else:
                    stats['errors'] += 1
                    print("✗")
            
            if year_exams:
                all_exams[year] = year_exams
        
        output_file = self.output_dir / "all_exams.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(all_exams, f, ensure_ascii=False, indent=2)
        
        print(f"\n{'='*60}")
        print(f"✅ EXTRACCIÓN COMPLETADA")
        print(f"{'='*60}")
        print(f"  • Total archivos: {stats['total_files']}")
        print(f"  • Procesados: {stats['processed']}")
        print(f"  • Errores: {stats['errors']}")
        print(f"  • Preguntas extraídas: {stats['total_questions']}")
        print(f"  • Imágenes detectadas: {stats['total_images']}")
        print(f"  • Salida: {output_file}")
        print(f"{'='*60}\n")
        
        return all_exams, stats

if __name__ == "__main__":
    extractor = PAUExamExtractor()
    exams, stats = extractor.process_all_exams()
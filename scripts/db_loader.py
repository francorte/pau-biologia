#!/usr/bin/env python3
import json
import sqlite3
from pathlib import Path
from config import EXTRACTED_EXAMS_DIR, DB_PATH, YEAR

class DBLoader:
    def __init__(self):
        self.db_path = DB_PATH
        self.json_file = EXTRACTED_EXAMS_DIR / f"exams_{YEAR}.json"
        self.stats = {'exams': 0, 'questions': 0, 'apartados': 0}
    
    def load_exams(self):
        print(f"\n📥 CARGANDO DATOS A BD\n")
        
        if not self.json_file.exists():
            print(f"❌ No encontrado: {self.json_file}")
            return False
        
        with open(self.json_file, 'r', encoding='utf-8') as f:
            exams = json.load(f)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            for exam_letter, exam_data in exams.items():
                exam_id = exam_data['exam_id']
                
                cursor.execute("""
                    INSERT OR REPLACE INTO exams (id, year, exam_letter, total_questions)
                    VALUES (?, ?, ?, ?)
                """, (exam_id, YEAR, exam_letter, len(exam_data['questions'])))
                
                self.stats['exams'] += 1
                print(f"  Examen {exam_letter}...", end=" ")
                
                for q in exam_data['questions']:
                    question_id = f"{exam_id}_Q{q['number']}"
                    
                    cursor.execute("""
                        INSERT OR REPLACE INTO questions 
                        (id, exam_id, question_number, question_label, question_text, bloque, total_points)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                    """, (
                        question_id, exam_id, q['number'], q['label'],
                        q['text'], q.get('bloque'), q['total_points']
                    ))
                    
                    self.stats['questions'] += 1
                    
                    for apt in q.get('apartados', []):
                        cursor.execute("""
                            INSERT INTO apartados (question_id, apartado_letter, apartado_text, points)
                            VALUES (?, ?, ?, ?)
                        """, (question_id, apt['label'], apt['text'], apt['points']))
                        
                        self.stats['apartados'] += 1
                
                print(f"✓ ({len(exam_data['questions'])} preguntas)")
            
            conn.commit()
            
            print(f"\n{'='*60}")
            print(f"✅ DATOS CARGADOS A BD")
            print(f"{'='*60}")
            print(f"  • Exámenes: {self.stats['exams']}")
            print(f"  • Preguntas: {self.stats['questions']}")
            print(f"  • Apartados: {self.stats['apartados']}")
            print(f"  • BD: {self.db_path}\n")
            
            return True
        
        except Exception as e:
            print(f"\n❌ Error: {e}")
            conn.rollback()
            return False
        
        finally:
            conn.close()
    
    def verify(self):
        print(f"\n📋 VERIFICANDO BD...\n")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM exams")
        exams_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM questions")
        questions_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM apartados")
        apartados_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT bloque, COUNT(*) FROM questions GROUP BY bloque")
        by_bloque = cursor.fetchall()
        
        conn.close()
        
        print(f"  Exámenes: {exams_count}")
        print(f"  Preguntas: {questions_count}")
        print(f"  Apartados: {apartados_count}")
        print(f"\n  Por bloque:")
        for bloque, count in by_bloque:
            print(f"    {bloque}: {count}")
        
        print()

if __name__ == "__main__":
    loader = DBLoader()
    if loader.load_exams():
        loader.verify()

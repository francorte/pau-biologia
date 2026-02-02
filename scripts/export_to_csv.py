#!/usr/bin/env python3
import sqlite3
import csv
from config import DB_PATH, YEAR

def export_questions_to_csv():
    print("\n📊 EXPORTANDO PREGUNTAS A CSV\n")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Obtener todas las preguntas con apartados
    cursor.execute("""
        SELECT 
            q.exam_id,
            SUBSTR(q.exam_id, -1) as exam_letter,
            q.question_number,
            q.question_label,
            q.question_text,
            q.bloque,
            q.total_points,
            GROUP_CONCAT(a.apartado_letter || '(' || a.points || 'pts): ' || a.apartado_text, ' | ') as apartados
        FROM questions q
        LEFT JOIN apartados a ON q.id = a.question_id
        GROUP BY q.id
        ORDER BY exam_letter, q.question_number
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Escribir CSV
    filename = f"preguntas_pau_{YEAR}.csv"
    
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        
        # Encabezados
        writer.writerow([
            'Examen',
            'Pregunta #',
            'Label',
            'Bloque',
            'Puntos',
            'Enunciado',
            'Apartados',
            'Nombre Imagen (ej: A_1_2025.png)',
            'Ruta Imagen',
            'Notas'
        ])
        
        # Datos
        for row in rows:
            exam_id, exam_letter, q_number, label, text, bloque, points, apartados = row
            writer.writerow([
                exam_letter,
                q_number,
                label,
                bloque or '',
                points,
                text,
                apartados or '',
                f"{exam_letter}_{label}_{YEAR}.png",  # Sugiere nombre
                '',  # Vacío para que Francisco lo llene
                ''
            ])
    
    print(f"✅ Exportado: {filename}")
    print(f"  • Preguntas: {len(rows)}")
    print(f"  • Puedes abrirlo en Google Sheets\n")

if __name__ == "__main__":
    export_questions_to_csv()

import sqlite3

db = sqlite3.connect('db/pau_biologia.db')
cursor = db.cursor()

# Clasificación final validada
bloques = {
    # Examen A
    ('A', 1): 'B',
    ('A', 2): 'A',
    ('A', 3): 'B',
    ('A', 4): 'C',
    ('A', 5): 'C',
    ('A', 6): 'F',
    ('A', 7): 'F',
    ('A', 8): 'D',
    ('A', 9): 'D',
    # Examen B
    ('B', 1): 'D',
    ('B', 2): 'D',
    ('B', 3): 'C',
    ('B', 4): 'F',
    ('B', 5): 'C',
    ('B', 6): 'B',
    ('B', 7): 'E',
    ('B', 8): 'E',
    ('B', 9): 'E',
    # Examen C
    ('C', 1): 'B',
    ('C', 2): 'B',
    ('C', 3): 'C',
    ('C', 4): 'C',
    ('C', 5): 'D',
    ('C', 6): 'D',
    ('C', 7): 'B',
    ('C', 8): 'B',
    ('C', 9): 'B',
    # Examen D
    ('D', 1): 'C',
    ('D', 2): 'A',
    ('D', 3): 'E',
    ('D', 4): 'F',
    ('D', 5): 'F',
    ('D', 6): 'C',
    ('D', 7): 'C',
    ('D', 8): 'D',
    ('D', 9): 'D',
}

updated = 0
for (exam_letter, num), bloque in bloques.items():
    cursor.execute(
        'UPDATE questions SET bloque = ? WHERE exam_id = (SELECT id FROM exams WHERE exam_letter = ?) AND question_number = ?',
        (bloque, exam_letter, num)
    )
    updated += cursor.rowcount

db.commit()
db.close()

print(f'✅ {updated} preguntas actualizadas con bloques')

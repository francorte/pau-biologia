#!/usr/bin/env python3
import sqlite3

DB_PATH = "pau_biologia.sqlite"

def cargar_examen_a_2025():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("INSERT OR IGNORE INTO examenes (año, tipo) VALUES (2025, 'A')")
    cursor.execute("SELECT id FROM examenes WHERE año = 2025 AND tipo = 'A'")
    examen_id = cursor.fetchone()[0]
    
    preguntas = [
        {
            "numero": "1",
            "bloque": "B",
            "puntos": 2.0,
            "enunciado": "En relación con la figura adjunta, responda a las siguientes cuestiones:",
            "apartados": [
                ("a", "Cite y defina los dos procesos que tienen lugar en la expresión de la información genética", 0.5),
                ("b", "¿Cómo se denomina la enzima marcada como E?", 0.1),
                ("c", "Identifique los elementos de la figura señalados con los números del 1 al 5", 0.5),
                ("d", "Indique el nombre de los extremos del elemento 2 (señalados con a y b), y el de los extremos del elemento 5 (señalados con c y d)", 0.4),
                ("e", "La insulina humana se produce a gran escala mediante ingeniería genética en bacterias. Sin embargo, el ADN humano contiene intrones que no pueden ser eliminados por las bacterias. ¿Por qué el uso de la transcriptasa inversa, una enzima que sintetiza ADN utilizando como molde una molécula de ARN, permite que una bacteria exprese correctamente el gen de la insulina humana y sintetice la proteína funcional?", 0.5),
            ],
        },
        {
            "numero": "2.1",
            "bloque": "A",
            "puntos": 2.0,
            "enunciado": "En relación con la imagen adjunta:",
            "apartados": [
                ("a", "Indique qué biomolécula está representada", 0.1),
                ("b", "¿Qué tipo de estructuras, de dicha biomolécula, representan los números del 1 al 5?", 0.5),
                ("c", "Indiqué qué tipo de enlace representa el número 6 y entre qué grupos funcionales se establece", 0.3),
                ("d", "Indique tres tipos de enlaces que intervengan en la estabilización de la estructura representada con el número 4", 0.3),
                ("e", "Si esta biomolécula se somete a una temperatura superior a 100 ºC, ¿qué ocurrirá y qué consecuencia tendrá?", 0.3),
                ("f", "Indique cinco localizaciones en una célula eucariota en las que se puedan encontrar las estructuras implicadas en la síntesis de esta biomolécula", 0.5),
            ],
        },
        {
            "numero": "2.2",
            "bloque": "A",
            "puntos": 2.0,
            "enunciado": "En relación con la figura adjunta:",
            "apartados": [
                ("a", "¿Qué molécula está representada en la imagen?", 0.2),
                ("b", "¿Qué representan los números 1, 2, 3, 4 y el recuadro 5?", 0.5),
                ("c", "Indique tres características que presente dicha molécula", 0.6),
                ("d", "Indique el nombre del proceso de síntesis de esta molécula y el nombre de la enzima principal de dicho proceso", 0.3),
                ("e", "Razone cómo afectaría a dicha enzima y a dicho proceso un incremento considerable de pH", 0.4),
            ],
        },
        {
            "numero": "3.1",
            "bloque": "D",
            "puntos": 2.0,
            "enunciado": "Los glóbulos rojos mantienen un contenido salino interno del 0,9 %",
            "apartados": [
                ("a", "¿Qué ocurriría con estas células si se inyectara a un individuo una solución salina que hiciera que la concentración final de sales en sangre fuese del 2,2 %?", 0.5),
                ("b", "¿Y si la concentración final de sales en sangre fuese del 0,01%?", 0.5),
                ("c", "Indique la composición de los fosfolípidos y explique por qué su estructura los hace idóneos para formar membranas biológicas", 1.0),
            ],
        },
        {
            "numero": "3.2",
            "bloque": "C",
            "puntos": 2.0,
            "enunciado": "En una clase de biología aplicada, en la que se está estudiando la mitosis",
            "apartados": [
                ("a", "¿A qué fases de la mitosis corresponden A, B y C?", 0.3),
                ("b", "¿Qué fase de la mitosis no se ha observado? Indique tres acontecimientos que ocurren en esta fase", 0.7),
                ("c", "Indique la importancia biológica que tiene la mitosis para este organismo", 0.5),
                ("d", "Sabiendo que la colchicina inhibe la polimerización de la tubulina, ¿qué efectos tendría en la mitosis de estas células?", 0.5),
            ],
        },
        {
            "numero": "4.1",
            "bloque": "F",
            "puntos": 2.0,
            "enunciado": "Ulani se mudó a España desde una isla remota sin saber que era alérgica a las abejas",
            "apartados": [
                ("a", "¿Qué tipo de inmunoglobulinas son específicas de la respuesta alérgica?", 0.6),
                ("b", "¿Cómo se denominan las diferentes sustancias que desencadenan una respuesta alérgica?", 0.2),
                ("c", "Indique el nombre de la célula de la imagen y el nombre de una sustancia liberada", 0.4),
                ("d", "¿Qué tipo de células producen las inmunoglobulinas?", 0.8),
            ],
        },
        {
            "numero": "4.2",
            "bloque": "F",
            "puntos": 2.0,
            "enunciado": "En relación con la imagen adjunta sobre inmunología:",
            "apartados": [
                ("a", "¿Qué tipos de inmunidad se representan?", 0.3),
                ("b", "¿Qué tipos de respuestas inmunitarias se representan?", 0.2),
                ("c", "Nombre las moléculas o células señaladas", 0.5),
                ("d", "Cite dos orgánulos implicados en la producción", 0.5),
                ("e", "Explique cómo se relacionan transcripción y traducción", 0.5),
            ],
        },
        {
            "numero": "5.1",
            "bloque": "D",
            "puntos": 2.0,
            "enunciado": "La industria alimentaria aprovecha diversos procesos de fermentación",
            "apartados": [
                ("a", "¿Qué tipo de fermentación se utiliza en yogur?", 0.4),
                ("b", "¿Qué tipo de fermentación se utiliza en pan?", 1.0),
                ("c", "Indique tres características diferenciadoras", 0.3),
                ("d", "¿Cómo afecta la temperatura a las enzimas?", 0.3),
            ],
        },
        {
            "numero": "5.2",
            "bloque": "A",
            "puntos": 2.0,
            "enunciado": "Con relación a la beta-oxidación de los ácidos grasos:",
            "apartados": [
                ("a", "Indique la localización intracelular", 0.2),
                ("b", "¿De qué tipo de molécula se parte y qué se obtiene?", 0.8),
                ("c", "Indique rutas para obtener energía", 0.6),
                ("d", "Nombre cuatro componentes de la misma localización", 0.4),
            ],
        },
    ]
    
    for preg in preguntas:
        cursor.execute("SELECT id FROM bloques WHERE codigo = ?", (preg["bloque"],))
        bloque_id = cursor.fetchone()[0]
        
        desc_completa = f"{preg['enunciado']}\n\n"
        for apt_letra, apt_texto, _ in preg["apartados"]:
            desc_completa += f"{apt_letra}) {apt_texto}\n"
        
        cursor.execute("""
            INSERT INTO preguntas 
            (examen_id, numero_pregunta, bloque_id, puntos, descripcion)
            VALUES (?, ?, ?, ?, ?)
        """, (examen_id, preg["numero"], bloque_id, preg["puntos"], desc_completa))
        
        pregunta_id = cursor.lastrowid
        
        for apt_letra, apt_texto, pts in preg["apartados"]:
            cursor.execute("""
                INSERT INTO respuestas 
                (pregunta_id, apartado, descripcion)
                VALUES (?, ?, ?)
            """, (pregunta_id, apt_letra, ""))
        
        print(f"✓ Pregunta {preg['numero']} (Bloque {preg['bloque']})")
    
    conn.commit()
    conn.close()
    print("\n✅ Examen A 2025 cargado")

if __name__ == "__main__":
    cargar_examen_a_2025()


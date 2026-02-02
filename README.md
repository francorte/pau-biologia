# 🧬 PAU Biología Trainer - Andalucía

Aplicación profesional para entrenamiento de exámenes PAU de Biología según las **Directrices y Orientaciones oficiales de Andalucía 2025-26**.

[![React](https://img.shields.io/badge/React-18.2-61DAFB?logo=react)](https://react.dev)
[![Express](https://img.shields.io/badge/Express-4.18-90C53F?logo=express)](https://expressjs.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite)](https://www.sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

## 🎯 Características principales

* ✅ **Banco de preguntas PAU 2025** - 36 preguntas clasificadas por bloques
* ✅ **6 Bloques temáticos oficiales** - A, B, C, D, E, F
* ✅ **Interfaz web profesional** - 3 paneles: bloques, preguntas, detalle
* ✅ **16 imágenes vinculadas** - Asociadas automáticamente a preguntas
* ✅ **API REST completa** - Para futuras integraciones
* ✅ **Base de datos SQLite** - 36 preguntas + 157 apartados

## 📊 Distribución de bloques

| Bloque | Contenido | Preguntas |
|--------|-----------|-----------|
| **A** | Biomoléculas | 2 |
| **B** | Genética molecular | 9 |
| **C** | Biología celular | 8 |
| **D** | Metabolismo | 10 |
| **E** | Biotecnología | 3 |
| **F** | Inmunología | 4 |

## 📂 Estructura del proyecto
```
pau-biologia/
├── README.md                    # Este archivo
├── CONTRIBUTING.md              # Guía de contribución
├── requirements.txt             # Dependencias Python
│
├── 📁 backend/
│   ├── server.js               # Express API (puerto 3000)
│   ├── package.json
│   └── package-lock.json
│
├── 📁 frontend/
│   ├── index.html              # React 18 + Tailwind CSS
│   ├── public/
│   │   └── exam_images/2025/   # 16 imágenes PAU
│   └── src/
│
├── 📁 db/
│   └── pau_biologia.db         # SQLite3 (36 preguntas)
│
├── 📁 docs/
│   ├── ARQUITECTURA.md         # Descripción técnica
│   └── ORIENTACIONES.md        # Directrices PAU oficiales
│
├── 📁 scripts/
│   ├── upload_exam.py          # Script maestro
│   ├── extract_pdf.py
│   ├── classify_bloques.py
│   ├── db_loader.py
│   └── 11 scripts más
│
└── 📁 data/
    └── exams/                  # PDFs entrada
```

## 🚀 Instalación rápida

### Requisitos
- Node.js 16+
- Python 3.8+
- npm o yarn

### Pasos
```bash
git clone https://github.com/francorte/pau-biologia.git
cd pau-biologia

npm install
pip install -r requirements.txt --break-system-packages

node backend/server.js
```

Abre navegador en `http://localhost:3000`

## 🔌 API REST Endpoints
```
GET  /api/bloques                           # Obtener 6 bloques
GET  /api/questions/by-bloque/:bloque       # Preguntas por bloque
GET  /api/questions/:id                     # Detalle pregunta con imagen
POST /api/upload                            # Cargar nuevo examen
```

## 🛠️ Stack tecnológico

* **Backend:** Express.js + Node.js
* **Frontend:** React 18 + Tailwind CSS
* **BD:** SQLite3
* **Scripts:** Python 3.8+
* **Hosting:** Vercel ready

## 📖 Basado en documentación oficial

Sigue las **Directrices y Orientaciones Generales para las Pruebas de Acceso** a la Universidad - Biología (2025-26) de las Universidades Públicas de Andalucía.

## 🤝 Contribuir

Ver `CONTRIBUTING.md`

## 📄 Licencia

MIT License - Ver LICENSE para detalles

## 👤 Autor

**Francisco de la Corte** - [@francorte](https://github.com/francorte)

---

*Preparando estudiantes andaluces para el éxito en PAU Biología* 🎓


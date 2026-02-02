# 🏗️ Arquitectura PAU Biología

## Componentes principales

### Backend (Express.js)
- **server.js** - API REST con 6 endpoints
- **Puerto:** 3000
- **BD:** SQLite3

### Frontend (React)
- **3 paneles:** Bloques | Preguntas | Detalle
- **Imágenes:** Base64 o rutas `/exam_images/`
- **Estilos:** Tailwind CSS

### Base de datos (SQLite)
- **exams** - Años disponibles
- **questions** - 36+ preguntas
- **apartados** - Subapartados con puntuación
- **question_images** - Imágenes asociadas

## Flujo de datos
```
PDF → Python extract → JSON → BD SQLite
                              ↓
                         Express API
                              ↓
                          React UI
                         (3 paneles)
```

## Clasificación de bloques

- **A:** Biomoléculas (2)
- **B:** Genética molecular (9)
- **C:** Biología celular (8)
- **D:** Metabolismo (10)
- **E:** Biotecnología (3)
- **F:** Inmunología (4)


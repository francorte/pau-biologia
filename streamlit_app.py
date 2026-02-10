import streamlit as st

st.set_page_config(page_title="PAU Biología Trainer", layout="wide")

st.title("🧬 PAU Biología Trainer")
st.write("Preparación para la PAU - Evaluación de Andalucía 2024-2025")

st.info("🚀 Versión Beta - Trainer en desarrollo")

# Quiz básico de prueba
st.subheader("📝 Quiz de ejemplo")
tema = st.radio("Selecciona tema:", ["Celula", "Genética", "Ecología"])

if tema == "Celula":
    st.write("**¿Cuál es la función principal de las mitocondrias?**")
    respuesta = st.radio("", ["A) Síntesis de proteínas", "B) Producción de ATP", "C) Almacenamiento de ADN"])
    if respuesta == "B) Producción de ATP":
        st.success("✅ ¡Correcto!")
    else:
        st.error("❌ Intenta de nuevo")

st.divider()
st.caption("Desarrollado por Francisco de la Corte | Aljaraque, Andalucía")

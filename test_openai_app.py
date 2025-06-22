# test_openai_app.py

import streamlit as st
from openai import OpenAI

# Crear cliente OpenAI (nuevo SDK v1.0+)
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Test API OpenAI", page_icon="🧪", layout="centered")
st.title("🧪 Prueba de conexión con OpenAI API")

texto = st.text_area("✍️ Ingresa un texto de prueba para análisis cualitativo",
                     "La universidad busca mejorar la calidad académica mediante nuevas estrategias de evaluación.",
                     height=200)

if st.button("🔍 Analizar con ChatGPT"):
    with st.spinner("Analizando con ChatGPT..."):

        prompt = f"""Analiza el siguiente texto con un enfoque cualitativo:

{texto}

Devuelve:
1. Análisis temático.
2. Análisis del discurso.
3. Conclusión cualitativa."""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=700
            )
            resultado = response.choices[0].message.content
            st.success("✅ Análisis generado correctamente:")
            st.text_area("📋 Resultado", resultado, height=300)
        except Exception as e:
            st.error(f"❌ Error al comunicarse con la API: {str(e)}")

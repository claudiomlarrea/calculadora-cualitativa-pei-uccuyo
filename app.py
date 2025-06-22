import streamlit as st
import pandas as pd
import openai
import os

# Cargar clave API desde los secretos
openai.api_key = st.secrets["openai"]["api_key"]

# Configuración inicial de la interfaz
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")
st.markdown("Sube tu archivo Excel con actividades del PEI")

# Subida del archivo
uploaded_file = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("Archivo cargado correctamente ✅")

    st.subheader("📊 Vista previa de los datos")
    st.dataframe(df.head())

    columnas_objetivo = [
        "Actividades Objetivo 1",
        "Actividades Objetivo 2",
        "Actividades Objetivo 3",
        "Actividades Objetivo 4",
        "Actividades Objetivo 5",
        "Actividades Objetivo 6",
    ]

    # Extraer los textos no vacíos de las columnas objetivo
    textos = []
    for col in columnas_objetivo:
        if col in df.columns:
            textos += df[col].dropna().astype(str).tolist()

    textos_filtrados = [t.strip() for t in textos if t.strip() and t.strip() != "-"]

    if textos_filtrados:
        if st.button("🔍 Realizar análisis cualitativo global de las actividades"):
            with st.spinner("Analizando con ChatGPT..."):
                prompt = (
                    "Realiza un análisis temático y del discurso de los siguientes textos "
                    "extraídos del Plan Estratégico Institucional de una universidad. "
                    "Identifica temas emergentes, patrones discursivos, preocupaciones y objetivos institucionales relevantes. "
                    "Los textos son:\n\n" + "\n- ".join(textos_filtrados)
                )

                try:
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ],
                        temperature=0.3
                    )
                    resultado = response.choices[0].message.content
                    st.success("✅ Análisis generado correctamente.")
                    st.subheader("📄 Resultado")
                    st.write(resultado)
                except Exception as e:
                    st.error(f"❌ Error al comunicarse con la API de OpenAI:\n\n{e}")
    else:
        st.warning("⚠️ No se encontraron textos válidos en las columnas seleccionadas.")
else:
    st.info("📥 Por favor, sube un archivo Excel para comenzar.")

import streamlit as st
import pandas as pd
import openai
import os
from io import BytesIO
from docx import Document

st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", page_icon="🧠", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")

openai.api_key = st.secrets["openai"]["api_key"] if "openai" in st.secrets else os.getenv("OPENAI_API_KEY")

uploaded_file = st.file_uploader("📤 Sube tu archivo Excel con actividades PEI", type=["xlsx"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    st.subheader("🧠 Selecciona columnas con texto libre para análisis cualitativo")
    texto_cols = st.multiselect("Selecciona una o más columnas", df.columns.tolist())

    if texto_cols:
        col_joined = df[texto_cols].astype(str).agg(" ".join, axis=1)

        st.subheader("🤖 Generando análisis temático y de discurso con ChatGPT")
        resultados = []
        for i, texto in enumerate(col_joined):
            prompt = f"Analiza el siguiente texto con un enfoque cualitativo:

{texto}

Devuelve:
1. Análisis temático.
2. Análisis del discurso.
3. Conclusión cualitativa."
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=700
                )
                resultado = response["choices"][0]["message"]["content"]
            except Exception as e:
                resultado = f"❌ Error: {str(e)}"
            resultados.append(resultado)

        df["Análisis Cualitativo"] = resultados
        st.dataframe(df[["Análisis Cualitativo"]])

        def export_to_word(resultados):
            doc = Document()
            doc.add_heading("Análisis Cualitativo PEI", 0)
            for i, r in enumerate(resultados, 1):
                doc.add_heading(f"Actividad {i}", level=2)
                doc.add_paragraph(r)
            export_path = "/mnt/data/analisis_cualitativo_pei.docx"
            doc.save(export_path)
            return export_path

        docx_file = export_to_word(resultados)
        with open(docx_file, "rb") as f:
            st.download_button("📥 Descargar Análisis en Word", f, file_name="analisis_cualitativo_pei.docx")

else:
    st.info("👆 Por favor sube un archivo Excel para comenzar.")

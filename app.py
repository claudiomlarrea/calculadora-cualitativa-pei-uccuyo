# app.py

import streamlit as st
import pandas as pd
from openai import OpenAI
from io import BytesIO
from docx import Document

# Crear cliente OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Configuración de página
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", page_icon="🎓", layout="wide")
st.title("🎓 Calculadora Cualitativa PEI UCCuyo")

# Subida de archivo Excel
uploaded_file = st.file_uploader("📤 Sube tu archivo Excel con actividades PEI", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    # 🔎 Detectar automáticamente columnas que contienen "Actividades Objetivo"
    texto_cols = [col for col in df.columns if "actividades objetivo" in col.lower()]
    st.subheader("🔎 Columnas detectadas automáticamente")
    st.write(texto_cols)

    if texto_cols:
        # Combinar textos por fila
        col_joined = df[texto_cols].astype(str).agg(" ".join, axis=1)

        st.subheader("🤖 Análisis temático y de discurso por actividad")
        resultados = []

        for i, texto in enumerate(col_joined):
            prompt = f"""Analiza el siguiente conjunto de actividades para una unidad del PEI con un enfoque cualitativo:

{texto}

Devuelve:
1. Análisis temático.
2. Análisis del discurso.
3. Conclusión cualitativa de esta unidad de actividades."""

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=700
                )
                resultado = response.choices[0].message.content
            except Exception as e:
                resultado = f"❌ Error: {str(e)}"
            resultados.append(resultado)

        df["Análisis Cualitativo"] = resultados
        st.dataframe(df[["Análisis Cualitativo"]])

        # Exportar a Word
        def export_to_word(resultados):
            doc = Document()
            doc.add_heading("Análisis Cualitativo PEI por Actividad", 0)
            for i, r in enumerate(resultados, 1):
                doc.add_heading(f"Actividad {i}", level=2)
                doc.add_paragraph(r)
            output_path = "/mnt/data/analisis_objetivos_pei.docx"
            doc.save(output_path)
            return output_path

        if any("❌ Error" not in r for r in resultados):
            docx_file = export_to_word(resultados)
            with open(docx_file, "rb") as f:
                st.download_button("📥 Descargar análisis en Word", f, file_name="analisis_objetivos_pei.docx")
        else:
            st.warning("⚠️ No se pudo generar análisis válido para exportar.")
    else:
        st.warning("⚠️ No se encontraron columnas de actividades objetivo.")
else:
    st.info("👆 Por favor sube un archivo Excel para comenzar.")

# app.py

import streamlit as st
import pandas as pd
from openai import OpenAI
from io import BytesIO
from docx import Document

# Crear cliente OpenAI con nueva API
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", page_icon="🧠", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")

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

        if any("❌ Error" not in r for r in resultados):
            docx_file = export_to_word(resultados)
            with open(docx_file, "rb") as f:
                st.download_button("📥 Descargar Análisis en Word", f, file_name="analisis_cualitativo_pei.docx")
        else:
            st.warning("⚠️ No se pudo generar ningún análisis válido para exportar.")

        # 🧠 Análisis global
        st.subheader("🧠 Análisis Global del Conjunto de Actividades")
        texto_global = "\n".join(col_joined)
        prompt_global = f"""Analiza el siguiente conjunto de textos con un enfoque cualitativo integral:

{texto_global}

Devuelve un único informe estructurado con:
1. Análisis temático general.
2. Análisis del discurso predominante.
3. Conclusión cualitativa integradora."""

        try:
            respuesta_global = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_global}],
                temperature=0.7,
                max_tokens=1000
            )
            analisis_global = respuesta_global.choices[0].message.content
            st.text_area("📋 Resultado del Análisis Global", analisis_global, height=400)

            st.download_button(
                label="📥 Descargar Análisis Global (.txt)",
                data=analisis_global,
                file_name="analisis_global_pei.txt",
                mime="text/plain"
            )
        except Exception as e:
            st.error(f"❌ Error al generar el análisis global: {str(e)}")

else:
    st.info("👆 Por favor sube un archivo Excel para comenzar.")

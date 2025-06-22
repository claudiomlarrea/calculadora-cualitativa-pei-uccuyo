# app.py

import streamlit as st
import pandas as pd
from openai import OpenAI
from io import BytesIO
from docx import Document

# Crear cliente OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Configuración general
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", page_icon="🎓", layout="wide")
st.title("🎓 Calculadora Cualitativa PEI UCCuyo")

# Subida de archivo
uploaded_file = st.file_uploader("📤 Sube tu archivo Excel con actividades PEI", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📑 Vista previa de los datos")
    st.dataframe(df)

    # Detectar columnas de actividades objetivo
    texto_cols = [col for col in df.columns if "actividades objetivo" in col.lower()]
    st.subheader("🔎 Columnas detectadas automáticamente")
    st.write(texto_cols)

    actividades = []

    for col in texto_cols:
        for idx, texto in enumerate(df[col]):
            if pd.notna(texto) and str(texto).strip() not in ["", "-", "None"]:
                actividades.append({
                    "Índice": idx + 2,  # para que coincida con la fila de Excel
                    "Columna": col,
                    "Texto": str(texto).strip()
                })

    if actividades:
        st.subheader("🤖 Análisis temático por actividad individual")
        resultados = []

        for act in actividades:
            prompt = (
                "Analiza esta actividad institucional desde un enfoque cualitativo:\n\n"
                f"{act['Texto']}\n\n"
                "Devuelve:\n"
                "1. Análisis temático.\n"
                "2. Análisis del discurso.\n"
                "3. Conclusión cualitativa."
            )

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

            resultados.append({
                "Fila Excel": act["Índice"],
                "Columna": act["Columna"],
                "Actividad": act["Texto"],
                "Análisis": resultado
            })

        df_resultado = pd.DataFrame(resultados)
        st.dataframe(df_resultado)

        # Exportar a Word
        def export_to_word(resultados):
            doc = Document()
            doc.add_heading("Análisis Cualitativo PEI por Actividad Individual", 0)
            for r in resultados:
                doc.add_heading(f"Fila {r['Fila Excel']} – {r['Columna']}", level=2)
                doc.add_paragraph(f"Actividad: {r['Actividad']}")
                doc.add_heading("Análisis", level=3)
                doc.add_paragraph(r["Análisis"])
            output_path = "/mnt/data/analisis_actividades_PEIs.docx"
            doc.save(output_path)
            return output_path

        docx_file = export_to_word(resultados)
        with open(docx_file, "rb") as f:
            st.download_button("📥 Descargar informe en Word", f, file_name="analisis_actividades_PEIs.docx")
    else:
        st.warning("⚠️ No se encontraron actividades válidas en las columnas objetivo.")
else:
    st.info("👆 Por favor sube un archivo Excel para comenzar.")

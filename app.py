import streamlit as st
import pandas as pd
from openai import OpenAI
from docx import Document
from io import BytesIO

# Configurar título
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")
st.caption("Sube tu archivo Excel con actividades PEI")

# Subida del archivo
uploaded_file = st.file_uploader("📂 Sube archivo .xlsx", type=["xlsx"])
if not uploaded_file:
    st.info("📌 Por favor sube un archivo Excel para comenzar.")
    st.stop()

# Cargar archivo
df = pd.read_excel(uploaded_file)

# Detectar columnas objetivo
target_columns = [col for col in df.columns if "Actividades Objetivo" in col]

# Vista previa
st.subheader("📊 Vista previa de los datos")
st.dataframe(df[target_columns].head(10))

# Botón para ejecutar análisis global
if st.button("🔍 Realizar análisis cualitativo global de las actividades"):
    with st.spinner("Generando análisis con GPT..."):

        # Reunir textos
        all_texts = []
        for col in target_columns:
            texts = df[col].dropna().astype(str).tolist()
            all_texts.extend(texts)

        concatenated_text = "\n\n".join(all_texts)

        # Enviar a OpenAI
        client = OpenAI()
        prompt = f"""Analiza cualitativamente las siguientes actividades institucionales del PEI. Realiza:
1. Un análisis temático general.
2. Un análisis del discurso relevante.
3. Conclusiones cualitativas principales.

Texto base:
{concatenated_text}
"""
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        analysis = response.choices[0].message.content

        # Mostrar en pantalla
        st.success("✅ Análisis generado correctamente:")
        st.markdown("### 🧾 Resultado del análisis global")
        st.markdown(analysis)

        # Guardar en Word
        doc = Document()
        doc.add_heading("Análisis Cualitativo Global de Actividades PEI", level=1)
        doc.add_paragraph(analysis)

        buffer = BytesIO()
        doc.save(buffer)
        buffer.seek(0)

        # Botón de descarga
        st.download_button(
            label="📥 Descargar análisis en Word",
            data=buffer,
            file_name="analisis_global_actividades_pei.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

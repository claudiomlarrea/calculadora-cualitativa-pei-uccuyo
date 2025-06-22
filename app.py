import pandas as pd
import streamlit as st
import openai
import io
from datetime import datetime

# Título institucional
st.title("🔍 Universidad Católica de Cuyo")
st.header("Secretaría de Investigación - Valorador Docente")
st.subheader("Análisis Cualitativo Temático y del Discurso por Objetivo")

# Carga del archivo
guardar_texto = None
uploaded_file = st.file_uploader("📂 Carga tu base de datos (CSV o Excel)", type=["csv", "xlsx"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.success("✅ Base de datos cargada correctamente")
    st.write("Vista previa de los primeros registros:")
    st.dataframe(df.head())

    # Selección de columna con textos
    columnas_texto = [col for col in df.columns if df[col].dtype == "object"]
    columna_seleccionada = st.selectbox("Selecciona una columna para analizar", columnas_texto)

    # Filtrar textos no vacíos
    textos_validos = df[columna_seleccionada].dropna().astype(str)

    if len(textos_validos) == 0:
        st.warning("⚠️ No hay textos no vacíos en la columna seleccionada")
    else:
        if st.button("📊 Realizar análisis cualitativo"):
            with st.spinner("Analizando temas y discursos..."):
                joined_text = "\n".join(textos_validos.tolist())
                prompt = f"""Realiza un análisis cualitativo temático y de discurso del siguiente conjunto de textos escritos por docentes. Extrae los temas recurrentes, ejemplos representativos y posibles patrones discursivos. Escribe el informe en español académico.\n\n{joined_text}"""

                # Llamada a OpenAI
                openai.api_key = st.secrets["openai_api_key"]
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=[
                        {"role": "system", "content": "Eres un experto en análisis cualitativo de textos en español."},
                        {"role": "user", "content": prompt}
                    ]
                )
                analisis = response["choices"][0]["message"]["content"]

                st.markdown("### 🧾 Resultados del análisis")
                st.write(analisis)
                guardar_texto = analisis

        # Opción para descarga
        if guardar_texto:
            buffer = io.StringIO()
            buffer.write(guardar_texto)
            st.download_button(
                label="📥 Descargar análisis como TXT",
                data=buffer.getvalue(),
                file_name=f"analisis_{columna_seleccionada}_{datetime.now().date()}.txt",
                mime="text/plain"
            )

import streamlit as st
import pandas as pd
import openai

# Configurar manualmente la clave API (NO RECOMENDADO para producción)
openai.api_key = ""

# Configuración general
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")
st.markdown("Sube tu archivo Excel con actividades del PEI realizadas por todas las unidades académicas y administrativas.")

# Cargar archivo
uploaded_file = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente")

    st.subheader("📊 Vista previa de los datos")
    st.dataframe(df)

    # Extraer columnas con actividades objetivo
    columnas_actividades = [col for col in df.columns if 'Actividades Objetivo' in col]

    # Extraer textos no vacíos de cada columna
    textos = []
    for col in columnas_actividades:
        textos_col = df[col].dropna().astype(str)
        textos += [t.strip() for t in textos_col if t.strip() != "" and t.strip() != "-" and t.strip().lower() != "none"]

    if textos:
        if st.button("🔍 Realizar análisis cualitativo global de las actividades"):
            with st.spinner("Generando análisis temático y de discurso con ChatGPT..."):
                prompt = (
                    "Realiza un análisis temático y del discurso de las siguientes actividades institucionales "
                    "del Plan Estratégico de una universidad. Identifica temas emergentes, patrones del discurso, "
                    "preocupaciones frecuentes y objetivos institucionales clave.\n\n" +
                    "\n- " + "\n- ".join(textos)
                )

                try:
                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.3,
                    )
                    resultado = response.choices[0].message.content
                    st.success("✅ Análisis generado correctamente")
                    st.subheader("📄 Resultado del análisis")
                    st.write(resultado)
                except Exception as e:
                    st.error(f"❌ Error al comunicarse con la API de OpenAI:\n{e}")
    else:
        st.warning("⚠️ No se encontraron textos válidos en las columnas de actividades objetivo.")
else:
    st.info("📥 Por favor, sube un archivo Excel para comenzar.")

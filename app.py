
import streamlit as st
import pandas as pd
from openai import OpenAI

# Autenticación con tu clave API de OpenAI
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Configuración general
st.set_page_config(page_title="Calculadora Cualitativa PEI UCCuyo", layout="wide")
st.title("🧠 Calculadora Cualitativa PEI UCCuyo")
st.markdown("Sube tu archivo Excel con actividades del PEI realizadas por todas las unidades académicas y administrativas.")

# Subida de archivo
uploaded_file = st.file_uploader("📂 Cargar archivo Excel", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("✅ Archivo cargado correctamente")

    st.subheader("📊 Vista previa de los datos")
    st.dataframe(df)

    # Extraer columnas con "Actividades Objetivo"
    columnas_actividades = [col for col in df.columns if 'Actividades Objetivo' in col]

    textos = []
    for col in columnas_actividades:
        textos_col = df[col].dropna().astype(str)
        textos += [t.strip() for t in textos_col if t.strip() and t.strip() != "-" and t.strip().lower() != "none"]

    if textos:
        # Análisis cualitativo global
        if st.button("🔍 Realizar análisis cualitativo global de las actividades"):
            with st.spinner("Generando análisis temático y de discurso con ChatGPT..."):
                prompt = (
                    "Realiza un análisis temático y del discurso de las siguientes actividades institucionales "
                    "del Plan Estratégico de una universidad. Identifica temas emergentes, patrones del discurso, "
                    "preocupaciones frecuentes y objetivos institucionales clave.\n\n"
                    + "\n- " + "\n- ".join(textos)
                )
                try:
                    response = client.chat.completions.create(
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

        # Análisis cualitativo por columna
        st.markdown("---")
        if st.button("🔍 Realizar análisis por objetivo (1 a 6)"):
            with st.spinner("Analizando columna por columna..."):
                for col in columnas_actividades:
                    textos_col = df[col].dropna().astype(str)
                    textos_filtrados = [t.strip() for t in textos_col if t.strip() and t.strip() != "-" and t.strip().lower() != "none"]
                    if textos_filtrados:
                        prompt_columna = f"""
Realiza un análisis temático y del discurso profundo de las expresiones en la columna '{col}'. 
Organiza el análisis en dos partes:

1. ANÁLISIS TEMÁTICO:
- Temas y subtemas emergentes.
- Códigos frecuentes y significativos.
- Patrones de sentido y preocupaciones comunes.

2. ANÁLISIS DEL DISCURSO:
- Actos de habla, relaciones de poder, tono e ideología.
- Posicionamientos institucionales.
- Modalidades del lenguaje y sentido implícito.

Texto:
- {'\n- '.join(textos_filtrados)}
"""
                        try:
                            response = client.chat.completions.create(
                                model="gpt-4",
                                messages=[{"role": "user", "content": prompt_columna}],
                                temperature=0.3,
                            )
                            resultado_columna = response.choices[0].message.content
                            st.success(f"✅ Análisis generado para {col}")
                            st.subheader(f"📄 Resultado: {col}")
                            st.write(resultado_columna)
                        except Exception as e:
                            st.error(f"❌ Error al analizar {col}:\n{e}")
    else:
        st.warning("⚠️ No se encontraron textos válidos en las columnas de actividades objetivo.")
else:
    st.info("📥 Por favor, sube un archivo Excel para comenzar.")

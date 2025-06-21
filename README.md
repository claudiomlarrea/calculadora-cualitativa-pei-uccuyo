# 🧠 Calculadora Cualitativa PEI - Universidad Católica de Cuyo

Esta aplicación permite realizar un análisis cualitativo automatizado (temático y de discurso) de las actividades cargadas en el PEI.

## 🚀 Cómo usar

1. **Clona o descarga este repositorio.**
2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Ejecuta la aplicación:**
   ```bash
   streamlit run app.py
   ```

## 🔐 Configuración de API

Agrega tu clave OpenAI en el archivo `.streamlit/secrets.toml`:

```toml
[openai]
api_key = "sk-..."
```

## 📁 Archivos

- `app.py` → Aplicación principal
- `requirements.txt` → Dependencias
- `README.md` → Instrucciones

Desarrollado por Dr. Claudio Larrea Arnau

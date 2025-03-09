import streamlit as st
import sqlite3
import os

# 📌 Ruta en Streamlit donde se almacena la base de datos
DB_DIR = "/mnt/data"
DB_PATH = os.path.join(DB_DIR, "datos.sqlite")

# 🔧 **Asegurar que el directorio de la base de datos existe**
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# 📂 **Interfaz para subir la base de datos manualmente**
st.title("📂 Subir Base de Datos SQLite")

uploaded_file = st.file_uploader("📂 Sube tu base de datos (.sqlite)", type="sqlite")

if uploaded_file:
    try:
        # Guardar la base de datos en la ruta correcta
        with open(DB_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success("✅ Base de datos subida correctamente.")
    except Exception as e:
        st.error(f"⚠️ Error al guardar la base de datos: {e}")

# 🔎 **Verificar si la base de datos está operativa**
if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH)
        st.success("✅ Conexión a la base de datos establecida correctamente.")
    except Exception as e:
        st.error(f"⚠️ Error al conectar con la base de datos: {e}")
else:
    st.warning("⚠️ No se encontró la base de datos en la ruta esperada. Sube un archivo primero.")

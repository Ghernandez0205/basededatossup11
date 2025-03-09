import streamlit as st
import sqlite3
import os

# 📌 Directorio donde se guardará la base de datos
DB_DIR = "/mnt/data"
DB_PATH = os.path.join(DB_DIR, "datos.sqlite")

# 🔹 Asegurar que el directorio de la base de datos existe
if not os.path.exists(DB_DIR):
    os.makedirs(DB_DIR)

# 📤 Permitir que el usuario suba su base de datos
uploaded_file = st.file_uploader("📂 Sube la base de datos SQLite", type=["sqlite"])

if uploaded_file:
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Guardar el archivo en /mnt/data/
    
    st.success(f"✅ Base de datos guardada correctamente.")

# 📡 Verificar si la base de datos existe antes de conectarse
if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        st.success("✅ Conectado exitosamente a la base de datos.")
    except sqlite3.OperationalError as e:
        st.error(f"❌ Error al conectar con la base de datos: {e}")
else:
    st.warning("⚠️ No se encontró ninguna base de datos. Sube un archivo para continuar.")

# 📂 Mostrar el contenido de la carpeta (para depuración)
if st.checkbox("📁 Ver archivos en /mnt/data/"):
    archivos = os.listdir(DB_DIR)
    st.write(archivos)

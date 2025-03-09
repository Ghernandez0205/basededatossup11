import streamlit as st
import sqlite3
import os

# 📌 Configurar la ruta donde se guardará la base de datos en Streamlit Cloud
DB_PATH = "/mnt/data/datos.sqlite"

# 🎯 Título de la aplicación
st.title("📂 Cargar Base de Datos")

# 📤 Permitir que el usuario suba su base de datos SQLite
uploaded_file = st.file_uploader("🔼 Sube tu base de datos SQLite (.sqlite)", type=["sqlite"])

if uploaded_file:
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())  # Guardar el archivo en /mnt/data/
    
    st.success(f"✅ Base de datos {uploaded_file.name} guardada correctamente.")

# 📡 Verificar si la base de datos existe antes de conectarse
if os.path.exists(DB_PATH):
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        st.success("✅ Conectado exitosamente a la base de datos.")
    except sqlite3.OperationalError as e:
        st.error(f"❌ Error al conectar con la base de datos: {e}")
else:
    st.warning("⚠️ No se encontró ninguna base de datos. Sube un archivo para continuar.")

# Mostrar el contenido de la carpeta donde se guarda la base de datos (para depuración)
if st.checkbox("📁 Ver archivos en /mnt/data/"):
    archivos = os.listdir("/mnt/data/")
    st.write(archivos)

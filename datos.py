import streamlit as st
import sqlite3
import os

# 📌 Ruta en Streamlit donde se almacenará la base de datos
DB_PATH = "/mnt/data/datos.sqlite"

# 📂 **Subida de la base de datos manualmente**
st.title("📂 Subir Base de Datos SQLite")

uploaded_file = st.file_uploader("📂 Sube tu base de datos (.sqlite)", type="sqlite")

if uploaded_file:
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Base de datos subida correctamente.")

# 🛠 **Verificar si la base de datos está disponible**
def check_db_exists():
    if os.path.exists(DB_PATH):
        return True
    return False

if check_db_exists():
    st.success("✅ La base de datos está operativa.")
else:
    st.error("⚠️ No se encontró la base de datos en la ruta esperada.")

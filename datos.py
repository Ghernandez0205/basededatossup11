import streamlit as st
import sqlite3
import os
import tempfile

# 📂 Subir base de datos sin escribir en disco
uploaded_file = st.file_uploader("📂 Sube la base de datos SQLite", type=["sqlite"])

if uploaded_file:
    try:
        # 🔹 Crear un archivo temporal en la RAM
        with tempfile.NamedTemporaryFile(delete=False) as temp_db:
            temp_db.write(uploaded_file.getbuffer())  # Guardar en la memoria
            temp_db_path = temp_db.name  # Obtener la ruta temporal

        # 📡 Conectar a la base de datos temporal
        conn = sqlite3.connect(temp_db_path, check_same_thread=False)
        st.success("✅ Base de datos cargada correctamente.")

        # 🔍 Opcional: Mostrar tablas existentes en la base de datos
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        if tables:
            st.write("📌 Tablas en la base de datos:", [t[0] for t in tables])
        else:
            st.warning("⚠️ La base de datos no contiene tablas.")

    except Exception as e:
        st.error(f"❌ Error al abrir la base de datos: {e}")
else:
    st.warning("⚠️ Sube una base de datos para continuar.")

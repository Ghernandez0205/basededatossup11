import streamlit as st
import pandas as pd
import sqlite3
import os

# 📌 Ruta local de la base de datos
DB_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

# 📂 Verificar si la base de datos existe
if not os.path.exists(DB_PATH):
    st.error("❌ No se encontró la base de datos en la ruta especificada.")
    st.stop()  # Detiene la ejecución si no hay base de datos

# 📊 Conectar a la base de datos
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

# 🔍 Función para obtener las tablas en la base de datos
def get_tables():
    query = "SELECT name FROM sqlite_master WHERE type='table';"
    tables = pd.read_sql(query, conn)
    return tables['name'].tolist()

# 📌 Obtener las tablas disponibles
tables = get_tables()

# 🎨 Interfaz Streamlit mejorada
st.title("📌 Gestión de la Base de Datos")
st.success("✅ Base de datos cargada correctamente.")

# 📂 Mostrar tablas disponibles en la base de datos
st.subheader("📑 Tablas disponibles:")
st.write(tables)

# 📊 Permitir seleccionar una tabla para ver los datos
selected_table = st.selectbox("Selecciona una tabla para visualizar:", tables)

# 📥 Cargar y mostrar datos de la tabla seleccionada
if selected_table:
    query = f"SELECT * FROM {selected_table} LIMIT 50;"  # Limita a 50 registros
    df = pd.read_sql(query, conn)
    
    if df.empty:
        st.warning(f"⚠️ La tabla '{selected_table}' está vacía.")
    else:
        st.dataframe(df)

# 📥 Agregar botón para descargar la base de datos
st.subheader("📥 Descargar Base de Datos")
with open(DB_PATH, "rb") as f:
    db_bytes = f.read()

st.download_button(label="Descargar Base de Datos", data=db_bytes, file_name="datos.sqlite", mime="application/octet-stream")

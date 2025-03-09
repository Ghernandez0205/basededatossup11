import streamlit as st
import pandas as pd
import sqlite3
import os
from io import BytesIO
from st_aggrid import AgGrid, GridOptionsBuilder

# Ruta de la base de datos en Streamlit Cloud
DB_PATH = "/mnt/data/datos.sqlite"

# Verificar si el usuario subió una base de datos
uploaded_file = st.file_uploader("📂 Sube la base de datos SQLite", type=["sqlite"])

if uploaded_file:
    DB_PATH = f"/mnt/data/{uploaded_file.name}"
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Base de datos guardada como {uploaded_file.name}")

# Si no hay base de datos, crear una nueva
if not os.path.exists(DB_PATH):
    st.warning("⚠️ No se encontró la base de datos. Se creará una nueva.")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Crear estructura de la base de datos si no existe
    cursor.executescript("""
    CREATE TABLE IF NOT EXISTS escuelas (
        id_escuela INTEGER PRIMARY KEY AUTOINCREMENT,
        Nombre_Escuela TEXT,
        Director TEXT,
        Direccion TEXT,
        Zona_Escolar TEXT,
        Sector TEXT
    );
    """)
    conn.commit()
    conn.close()
    st.success("✅ Base de datos creada exitosamente.")

# Conectar a la base de datos
@st.cache_resource
def get_connection():
    try:
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        return conn
    except sqlite3.OperationalError as e:
        st.error(f"❌ Error al conectar con la base de datos: {e}")
        return None

conn = get_connection()

# Verificar si la conexión es válida
if conn is None:
    st.stop()

# Función para verificar si una tabla existe
def check_table_exists(table_name):
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    result = pd.read_sql(query, conn)
    return not result.empty

# Cargar datos de escuelas
if check_table_exists("escuelas"):
    escuelas_df = pd.read_sql("SELECT * FROM escuelas", conn)
    if escuelas_df.empty:
        st.warning("⚠️ No hay registros en la tabla 'escuelas'.")
else:
    escuelas_df = pd.DataFrame()
    st.error("❌ La tabla 'escuelas' no existe en la base de datos.")

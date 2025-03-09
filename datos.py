import os
import sqlite3
import streamlit as st

# Definir la ruta de la base de datos dentro de Streamlit
DB_PATH = "/mnt/data/datos.sqlite"

# Verificar si la base de datos existe
if not os.path.exists(DB_PATH):
    st.warning("⚠️ No se encontró la base de datos. Creando una nueva...")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear las tablas necesarias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS escuelas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        director TEXT,
        direccion TEXT,
        zona TEXT,
        sector TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS personal_educativo (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        apellido TEXT,
        cargo TEXT,
        escuela_id INTEGER,
        FOREIGN KEY (escuela_id) REFERENCES escuelas(id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS auditoria_cambios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tabla TEXT,
        accion TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
    st.success("✅ Base de datos creada correctamente.")

# Conectar a la base de datos existente
conn = sqlite3.connect(DB_PATH)
st.success("✅ Conexión establecida con la base de datos.")

# Mostrar las tablas disponibles
st.subheader("📌 Tablas en la base de datos:")
tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
tables = [row[0] for row in conn.execute(tables_query)]
st.write(tables)

# Cargar y mostrar datos de la tabla 'escuelas'
st.subheader("🏫 Datos de la tabla 'escuelas':")
df_escuelas = pd.read_sql("SELECT * FROM escuelas", conn)
st.dataframe(df_escuelas)

conn.close()

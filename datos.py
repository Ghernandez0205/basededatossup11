import streamlit as st
import pandas as pd
import sqlite3
import os

# 📌 Ruta local para la base de datos en OneDrive
SQLITE_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.sqlite"

# 📌 Función para conectar a la base de datos
def get_connection():
    return sqlite3.connect(SQLITE_PATH, check_same_thread=False)

# 📌 Crear la base de datos si no existe
def create_database():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docentes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            RFC TEXT UNIQUE NOT NULL,
            Nombre TEXT NOT NULL,
            Apellido_Paterno TEXT,
            Apellido_Materno TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS escuelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Escuela TEXT NOT NULL,
            RFC_Docente TEXT NOT NULL,
            FOREIGN KEY (RFC_Docente) REFERENCES docentes(RFC) ON DELETE CASCADE
        )
    ''')
    
    conn.commit()
    conn.close()

# 📌 Cargar datos desde SQLite
def cargar_datos():
    conn = get_connection()
    df_docentes = pd.read_sql("SELECT * FROM docentes", conn)
    df_escuelas = pd.read_sql("SELECT * FROM escuelas", conn)
    conn.close()
    return df_docentes, df_escuelas

# 📌 Guardar datos en SQLite
def guardar_datos(df_docentes, df_escuelas):
    conn = get_connection()
    df_docentes.to_sql("docentes", conn, if_exists="replace", index=False)
    df_escuelas.to_sql("escuelas", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

# 📌 Crear base de datos si no existe
create_database()

# 📌 Título de la aplicación
st.title("📌 Gestión de Escuelas y Docentes")

# 📌 Cargar datos
df_docentes, df_escuelas = cargar_datos()

# 📌 Opciones de filtrado
st.sidebar.header("🔍 Filtros")
filtro_rfc = st.sidebar.text_input("🔎 Buscar por RFC:")
filtro_nombre = st.sidebar.text_input("🔎 Buscar por Nombre o Apellido:")
filtro_escuela = st.sidebar.text_input("🏫 Buscar por Escuela:")

# 📌 Aplicar filtros
if filtro_rfc:
    df_docentes = df_docentes[df_docentes["RFC"].str.contains(filtro_rfc, case=False, na=False)]

if filtro_nombre:
    df_docentes = df_docentes[
        df_docentes["Nombre"].str.contains(filtro_nombre, case=False, na=False) |
        df_docentes["Apellido_Paterno"].str.contains(filtro_nombre, case=False, na=False) |
        df_docentes["Apellido_Materno"].str.contains(filtro_nombre, case=False, na=False)
    ]

if filtro_escuela:
    df_escuelas = df_escuelas[df_escuelas["Escuela"].str.contains(filtro_escuela, case=False, na=False)]

# 📌 Mostrar tablas
st.subheader("📚 Lista de Docentes")
st.dataframe(df_docentes)

st.subheader("🏫 Lista de Escuelas")
st.dataframe(df_escuelas)

# 📌 Sección para agregar docentes
st.subheader("➕ Agregar Nuevo Docente")
col1, col2, col3, col4 = st.columns(4)

with col1:
    rfc = st.text_input("RFC:")
with col2:
    nombre = st.text_input("Nombre:")
with col3:
    apellido_paterno = st.text_input("Apellido Paterno:")
with col4:
    apellido_materno = st.text_input("Apellido Materno:")

if st.button("📌 Guardar Docente"):
    nuevo_docente = pd.DataFrame([[rfc, nombre, apellido_paterno, apellido_materno]],
                                 columns=["RFC", "Nombre", "Apellido_Paterno", "Apellido_Materno"])
    df_docentes = pd.concat([df_docentes, nuevo_docente], ignore_index=True)
    guardar_datos(df_docentes, df_escuelas)
    st.success(f"Docente '{nombre}' agregado correctamente.")

# 📌 Sección para agregar escuelas a un docente
st.subheader("🏫 Agregar Escuela a un Docente")
docente_seleccionado = st.selectbox("Selecciona un docente:", df_docentes["RFC"].astype(str) + " - " + df_docentes["Nombre"])

nombre_escuela = st.text_input("🏫 Nombre de la nueva escuela:")

if st.button("➕ Agregar Escuela"):
    rfc_seleccionado = docente_seleccionado.split(" - ")[0]
    nueva_escuela = pd.DataFrame([[nombre_escuela, rfc_seleccionado]],
                                 columns=["Escuela", "RFC_Docente"])
    df_escuelas = pd.concat([df_escuelas, nueva_escuela], ignore_index=True)
    guardar_datos(df_docentes, df_escuelas)
    st.success(f"Escuela '{nombre_escuela}' agregada al docente {docente_seleccionado}.")

# 📌 Descargas
st.subheader("📥 Descargar Base de Datos")

col1, col2, col3 = st.columns(3)

with col1:
    st.download_button("📥 Descargar Excel", df_docentes.to_csv(index=False).encode("utf-8"), "docentes.xlsx")
with col2:
    st.download_button("📥 Descargar CSV", df_docentes.to_csv(index=False).encode("utf-8"), "docentes.csv")
with col3:
    with open(SQLITE_PATH, "rb") as f:
        st.download_button("📥 Descargar SQLite", f, "datos.sqlite")

# 📌 Mensaje final
st.markdown("📌 **Desarrollado con Streamlit | Optimizado para gestión de docentes**")

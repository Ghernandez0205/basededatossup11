import streamlit as st
import pandas as pd
import sqlite3
import os

# Definir la ruta de la base de datos
SQLITE_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"

def create_database():
    """Crea la base de datos SQLite si no existe."""
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS docentes_escuelas (
            RFC TEXT PRIMARY KEY,
            CURP TEXT,
            Nombre TEXT,
            Apellido_Paterno TEXT,
            Apellido_Materno TEXT,
            Escuela TEXT
        )
    ''')
    conn.commit()
    conn.close()

def load_data():
    """Carga los datos desde Excel a SQLite si la base está vacía."""
    if not os.path.exists(SQLITE_PATH):
        df = pd.read_excel(EXCEL_PATH)
        save_to_sqlite(df)
    return fetch_from_sqlite()

def save_to_sqlite(df):
    """Guarda los datos en SQLite."""
    conn = sqlite3.connect(SQLITE_PATH)
    df.to_sql("docentes_escuelas", conn, if_exists="replace", index=False)
    conn.close()

def fetch_from_sqlite():
    """Obtiene los datos desde SQLite."""
    conn = sqlite3.connect(SQLITE_PATH)
    df = pd.read_sql("SELECT * FROM docentes_escuelas", conn)
    conn.close()
    return df

def add_school(rfc, new_school):
    """Agrega una nueva escuela a un docente."""
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE docentes_escuelas SET Escuela = ? WHERE RFC = ?", (new_school, rfc))
    conn.commit()
    conn.close()

def delete_record(rfc):
    """Elimina un docente de la base de datos."""
    conn = sqlite3.connect(SQLITE_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM docentes_escuelas WHERE RFC = ?", (rfc,))
    conn.commit()
    conn.close()

def download_data(df, format):
    """Descarga los datos en el formato seleccionado."""
    if format == "Excel":
        df.to_excel("docentes_escuelas.xlsx", index=False)
        return "docentes_escuelas.xlsx"
    elif format == "CSV":
        df.to_csv("docentes_escuelas.csv", index=False)
        return "docentes_escuelas.csv"

# Streamlit UI
st.title("📌 Gestión de Escuelas y Docentes")
st.write("**Desarrollado con Streamlit | Optimizado para SQLite**")

# Cargar datos desde SQLite
create_database()
df = load_data()

# Filtros avanzados
st.sidebar.header("🔍 Filtrar Docentes")
rfc_filter = st.sidebar.text_input("Buscar por RFC")
nombre_filter = st.sidebar.text_input("Buscar por Nombre")
escuela_filter = st.sidebar.text_input("Buscar por Escuela")

if rfc_filter:
    df = df[df["RFC"].str.contains(rfc_filter, case=False, na=False)]
if nombre_filter:
    df = df[df["Nombre"].str.contains(nombre_filter, case=False, na=False)]
if escuela_filter:
    df = df[df["Escuela"].str.contains(escuela_filter, case=False, na=False)]

st.dataframe(df)

# Agregar nueva escuela
st.subheader("🏫 Agregar Nueva Escuela a un Docente")
docente_seleccionado = st.selectbox("Selecciona un docente:", df["Nombre"].unique())
nueva_escuela = st.text_input("Nombre de la nueva escuela:")
if st.button("Agregar Escuela"):
    rfc_docente = df[df["Nombre"] == docente_seleccionado]["RFC"].values[0]
    add_school(rfc_docente, nueva_escuela)
    st.success(f"✅ Escuela '{nueva_escuela}' agregada al docente {docente_seleccionado}")
    df = fetch_from_sqlite()

# Eliminar docente
st.subheader("🗑️ Eliminar Docente")
docente_eliminar = st.selectbox("Selecciona un docente para eliminar:", df["Nombre"].unique())
if st.button("Eliminar Docente"):
    rfc_docente = df[df["Nombre"] == docente_eliminar]["RFC"].values[0]
    delete_record(rfc_docente)
    st.warning(f"⚠️ Docente {docente_eliminar} eliminado")
    df = fetch_from_sqlite()

# Descargar datos
st.subheader("📥 Descargar Datos")
formato = st.radio("Selecciona formato:", ["Excel", "CSV"])
if st.button("Descargar Datos"):
    file_path = download_data(df, formato)
    with open(file_path, "rb") as file:
        st.download_button(label=f"⬇️ Descargar {formato}", data=file, file_name=file_path)

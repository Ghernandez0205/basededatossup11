import streamlit as st
import pandas as pd
import sqlite3
import os

# Ruta del archivo Excel
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
DB_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.db"

# Crear base de datos si no existe
def create_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS docentes (
                      RFC TEXT PRIMARY KEY,
                      CURP TEXT,
                      Nombre TEXT,
                      Apellido_Paterno TEXT,
                      Apellido_Materno TEXT,
                      Nivel_Educativo TEXT,
                      Fecha_Ingreso_SEP TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS escuelas (
                      ID INTEGER PRIMARY KEY AUTOINCREMENT,
                      RFC TEXT,
                      Escuela TEXT,
                      FOREIGN KEY (RFC) REFERENCES docentes(RFC))''')
    conn.commit()
    conn.close()

# Cargar datos del Excel
def load_data():
    if os.path.exists(EXCEL_PATH):
        df = pd.read_excel(EXCEL_PATH)
        return df
    else:
        return pd.DataFrame()

def save_to_sqlite(df_docentes, df_escuelas):
    conn = sqlite3.connect(DB_PATH)
    df_docentes.to_sql("docentes", conn, if_exists="replace", index=False)
    df_escuelas.to_sql("escuelas", conn, if_exists="replace", index=False)
    conn.close()

def filter_data(df, search_term):
    if search_term:
        df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False, na=False).any(), axis=1)]
    return df

# Crear base de datos si no existe
create_database()

df_docentes = load_data()
df_escuelas = pd.DataFrame(columns=["RFC", "Escuela"])

st.title("📌 Gestión de Escuelas y Docentes")

# Menú lateral
menu = st.sidebar.radio("Selecciona una opción", ["📂 Ver Datos", "➕ Agregar Escuela", "🔍 Filtrar Información", "📤 Exportar Datos"])

if menu == "📂 Ver Datos":
    st.subheader("📋 Lista de Docentes")
    if not df_docentes.empty:
        st.dataframe(df_docentes)
    else:
        st.warning("No se encontró el archivo Excel en la ruta especificada.")

elif menu == "➕ Agregar Escuela":
    st.subheader("🏫 Agregar Escuelas a un Docente")
    rfc = st.text_input("Ingresa el RFC del docente")
    escuela = st.text_input("Nombre de la escuela")
    if st.button("Agregar"):
        if rfc and escuela:
            df_escuelas = df_escuelas.append({"RFC": rfc, "Escuela": escuela}, ignore_index=True)
            st.success(f"Escuela '{escuela}' agregada al docente con RFC {rfc}.")
        else:
            st.error("Por favor ingresa todos los datos.")
    st.dataframe(df_escuelas)

elif menu == "🔍 Filtrar Información":
    st.subheader("🔎 Filtrar Docentes y Escuelas")
    search = st.text_input("Buscar por RFC, CURP, Nombre o Escuela")
    filtered_df = filter_data(df_docentes, search)
    st.dataframe(filtered_df)

elif menu == "📤 Exportar Datos":
    st.subheader("📥 Exportar Datos en Diferentes Formatos")
    if st.button("📂 Guardar en SQLite"):
        save_to_sqlite(df_docentes, df_escuelas)
        st.success("Datos guardados en SQLite correctamente.")
    
    st.download_button("📥 Descargar en Excel", df_docentes.to_csv(index=False), "docentes.xlsx")
    st.download_button("📥 Descargar en CSV", df_docentes.to_csv(index=False), "docentes.csv")

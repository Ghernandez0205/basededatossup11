import streamlit as st
import pandas as pd
import sqlite3
import os

# Ruta del archivo Excel y SQLite
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
SQLITE_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

# Cargar datos desde Excel o SQLite
def cargar_datos():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
        st.error("No se encontró el archivo Excel en la ruta especificada.")
        return pd.DataFrame()

def guardar_datos(df):
    df.to_excel(EXCEL_PATH, index=False)
    with sqlite3.connect(SQLITE_PATH) as conn:
        df.to_sql("docentes", conn, if_exists="replace", index=False)
    st.success("Datos guardados correctamente.")

# Cargar datos
st.sidebar.title("Gestión de Docentes y Escuelas")
opcion = st.sidebar.radio("Selecciona una opción", ["Lista de Docentes", "Gestión de Escuelas", "Seguimiento de Documentación", "Generación de Reportes"])

df = cargar_datos()

if opcion == "Lista de Docentes":
    st.title("📚 Lista de Docentes")
    st.dataframe(df)

elif opcion == "Gestión de Escuelas":
    st.title("🏫 Gestión de Escuelas")
    docente = st.selectbox("Selecciona un docente:", df["Nombre"].dropna().unique())
    escuela_nueva = st.text_input("Nombre de la nueva escuela:")
    if st.button("Agregar Escuela"):
        df.loc[df["Nombre"] == docente, "Escuela"] = df.loc[df["Nombre"] == docente, "Escuela"].astype(str) + ", " + escuela_nueva
        guardar_datos(df)
        st.success(f"Escuela '{escuela_nueva}' agregada al docente {docente}")

elif opcion == "Seguimiento de Documentación":
    st.title("📌 Seguimiento de Documentación")
    docente = st.selectbox("Selecciona un docente:", df["Nombre"].dropna().unique())
    documentos = ["Hoja de Datos", "Reanudación", "Horarios", "FUP", "Talón de Pago", "Solicitud Día Económico"]
    entregados = st.multiselect("Selecciona documentos entregados:", documentos)
    if st.button("Guardar Documentación"):
        df.loc[df["Nombre"] == docente, "Documentación"] = ", ".join(entregados)
        guardar_datos(df)
        st.success("Documentación guardada correctamente.")

elif opcion == "Generación de Reportes":
    st.title("📊 Generación de Reportes")
    columnas = st.multiselect("Selecciona qué columnas exportar", df.columns)
    if st.button("Exportar a Excel"):
        df[columnas].to_excel("reporte.xlsx", index=False)
        st.success("Reporte exportado a Excel.")
    if st.button("Exportar a SQLite"):
        with sqlite3.connect(SQLITE_PATH) as conn:
            df[columnas].to_sql("reportes", conn, if_exists="replace", index=False)
        st.success("Reporte guardado en SQLite.")

import streamlit as st
import pandas as pd
import sqlite3
import os

# Ruta del archivo Excel en OneDrive
EXCEL_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.xlsx"
SQLITE_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.sqlite"

# Verificar si el archivo Excel existe
if os.path.exists(EXCEL_PATH):
    # Cargar el archivo Excel
    df = pd.read_excel(EXCEL_PATH)

    # Mostrar datos en Streamlit
    st.title("📚 Gestión de Escuelas y Docentes")
    st.dataframe(df)

    # Opción para filtrar por docente
    docente_seleccionado = st.selectbox("🔎 Filtrar por docente:", df["Nombre"].dropna().unique())
    df_filtrado = df[df["Nombre"] == docente_seleccionado]
    st.dataframe(df_filtrado)

    # Opción para agregar nuevas escuelas a un docente
    nueva_escuela = st.text_input("🏫 Agregar escuela para el docente seleccionado:")
    if st.button("Agregar Escuela"):
        df.loc[df["Nombre"] == docente_seleccionado, "Escuela"] = nueva_escuela
        df.to_excel(EXCEL_PATH, index=False)
        st.success(f"Escuela '{nueva_escuela}' agregada al docente {docente_seleccionado}.")

    # Función para convertir a SQLite
    def save_to_sqlite(df, db_path):
        conn = sqlite3.connect(db_path)
        df.to_sql("docentes", conn, if_exists="replace", index=False)
        conn.close()

    # Botón para descargar datos en SQLite
    if st.button("💾 Guardar en SQLite"):
        save_to_sqlite(df, SQLITE_PATH)
        st.success(f"📂 Datos guardados en SQLite en: {SQLITE_PATH}")

    # Opción para descargar en Excel
    st.download_button(
        label="📥 Descargar en Excel",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="datos.csv",
        mime="text/csv",
    )

else:
    st.error(f"❌ No se encontró el archivo Excel en la ruta: {EXCEL_PATH}")

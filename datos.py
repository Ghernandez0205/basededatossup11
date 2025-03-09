import streamlit as st
import pandas as pd
import os
import sqlite3

# ------------------- CONFIGURACIÓN -------------------
# Ruta del archivo Excel
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
SQLITE_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

# ------------------- CARGAR O CREAR BASE DE DATOS -------------------
def load_data():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
        st.error("⚠ No se encontró el archivo Excel en la ruta especificada.")
        return pd.DataFrame()

# ------------------- GUARDAR EN SQLITE -------------------
def save_to_sqlite(df):
    conn = sqlite3.connect(SQLITE_PATH)
    df.to_sql("escuelas_docentes", conn, if_exists="replace", index=False)
    conn.close()

# ------------------- INTERFAZ STREAMLIT -------------------
st.set_page_config(page_title="Gestión de Escuelas y Docentes", layout="wide")
st.title("📌 Gestión de Escuelas y Docentes")

# 📂 Cargar archivo Excel
df = load_data()

if not df.empty:
    # Mostrar datos con AgGrid para filtros avanzados
    st.dataframe(df)

    # ------------------- EDITAR DATOS -------------------
    st.subheader("✏️ Modificar Datos")

    with st.form("form_edit"):
        selected_index = st.number_input("Índice del registro a modificar", min_value=0, max_value=len(df)-1, step=1)
        col1, col2, col3 = st.columns(3)
        with col1:
            rfc = st.text_input("RFC", value=str(df.loc[selected_index, "RFC"]) if len(df) > 0 else "")
        with col2:
            nombre = st.text_input("Nombre", value=str(df.loc[selected_index, "Nombre"]) if len(df) > 0 else "")
        with col3:
            escuela = st.text_input("Escuela", value=str(df.loc[selected_index, "Nivel_Educativo"]) if len(df) > 0 else "")

        submitted = st.form_submit_button("Actualizar Registro")
        if submitted:
            df.at[selected_index, "RFC"] = rfc
            df.at[selected_index, "Nombre"] = nombre
            df.at[selected_index, "Nivel_Educativo"] = escuela
            st.success("✅ Registro actualizado correctamente.")
            df.to_excel(EXCEL_PATH, index=False)
            save_to_sqlite(df)

    # ------------------- AGREGAR NUEVO REGISTRO -------------------
    st.subheader("➕ Agregar Nueva Escuela")

    with st.form("form_add"):
        col1, col2, col3 = st.columns(3)
        with col1:
            new_rfc = st.text_input("RFC Nuevo")
        with col2:
            new_nombre = st.text_input("Nombre Docente")
        with col3:
            new_escuela = st.text_input("Escuela")

        add_submitted = st.form_submit_button("Agregar")
        if add_submitted:
            new_data = pd.DataFrame({"RFC": [new_rfc], "Nombre": [new_nombre], "Nivel_Educativo": [new_escuela]})
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_excel(EXCEL_PATH, index=False)
            save_to_sqlite(df)
            st.success("✅ Nueva escuela agregada con éxito.")

    # ------------------- DESCARGAR ARCHIVOS -------------------
    st.subheader("📥 Descargar Datos")

    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📩 Descargar CSV", csv, "datos.csv", "text/csv")

    with col2:
        excel_bytes = df.to_excel("datos_temporales.xlsx", index=False)
        with open("datos_temporales.xlsx", "rb") as f:
            st.download_button("📩 Descargar Excel", f, "datos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col3:
        save_to_sqlite(df)
        st.download_button("📩 Descargar SQLite", SQLITE_PATH, "datos.sqlite", "application/octet-stream")

st.write("---")
st.markdown("📌 **Desarrollado con Streamlit | Optimizado para gestión de docentes**")

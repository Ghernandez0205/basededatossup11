import streamlit as st
import pandas as pd
import sqlite3
import os

# ------------------- CONFIGURACIÓN -------------------
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
SQLITE_PATH = "datos.sqlite"  # Guardamos en la misma carpeta del script para evitar problemas de permisos

st.set_page_config(page_title="Gestión de Escuelas y Docentes", layout="wide")
st.title("📌 Gestión de Escuelas y Docentes")

# ------------------- CARGA DE ARCHIVO -------------------
def load_data():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
        st.warning("⚠ No se encontró el archivo Excel en la ruta especificada. Puedes subirlo manualmente.")
        uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])
        if uploaded_file is not None:
            temp_path = "datos_temporal.xlsx"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Archivo guardado en {temp_path}")
            return pd.read_excel(temp_path)
        else:
            return pd.DataFrame()

# ------------------- GUARDAR EN SQLITE -------------------
def save_to_sqlite(df):
    try:
        conn = sqlite3.connect(SQLITE_PATH)
        df.to_sql("escuelas_docentes", conn, if_exists="replace", index=False)
        conn.close()
        st.success("✅ Base de datos guardada correctamente en SQLite")
    except Exception as e:
        st.error(f"❌ Error al guardar en SQLite: {e}")

# ------------------- INTERFAZ STREAMLIT -------------------
df = load_data()

if not df.empty:
    # --- FILTROS AVANZADOS ---
    st.sidebar.header("🔎 Filtros de búsqueda")
    docente = st.sidebar.text_input("Buscar por nombre de docente:")
    escuela = st.sidebar.text_input("Buscar por nombre de escuela:")

    if docente:
        df = df[df["Nombre"].str.contains(docente, case=False, na=False)]
    if escuela:
        df = df[df["Escuela"].str.contains(escuela, case=False, na=False)]

    st.dataframe(df)

    # --- AGREGAR NUEVA ESCUELA ---
    st.subheader("🏫 Agregar Nueva Escuela a un Docente")
    with st.form("add_school_form"):
        col1, col2 = st.columns(2)
        with col1:
            new_docente = st.selectbox("Selecciona un docente:", df["Nombre"].unique())
        with col2:
            new_escuela = st.text_input("Nombre de la nueva escuela:")
        
        submitted = st.form_submit_button("Agregar Escuela")
        if submitted and new_escuela:
            new_row = pd.DataFrame({"Nombre": [new_docente], "Escuela": [new_escuela]})
            df = pd.concat([df, new_row], ignore_index=True)
            st.success(f"✅ Escuela '{new_escuela}' agregada al docente {new_docente}")

    # --- DESCARGAR ARCHIVOS ---
    st.subheader("📥 Descargar Datos")
    col1, col2, col3 = st.columns(3)

    with col1:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("📩 Descargar CSV", csv, "datos.csv", "text/csv")

    with col2:
        df.to_excel("datos_temporales.xlsx", index=False)
        with open("datos_temporales.xlsx", "rb") as f:
            st.download_button("📩 Descargar Excel", f, "datos.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with col3:
        save_to_sqlite(df)
        st.download_button("📩 Descargar SQLite", SQLITE_PATH, "datos.sqlite", "application/octet-stream")

st.write("---")
st.markdown("📌 **Desarrollado con Streamlit | Optimizado para gestión de docentes**")

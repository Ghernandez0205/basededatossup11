import streamlit as st
import pandas as pd
import os
import sqlite3

# ------------------- CONFIGURACIÓN -------------------
# Ruta del archivo Excel
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
SQLITE_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

st.set_page_config(page_title="Gestión de Escuelas y Docentes", layout="wide")
st.title("📌 Gestión de Escuelas y Docentes")

# ------------------- CARGA DE ARCHIVO -------------------
def load_data():
    # Verificar si el archivo existe en la ruta local
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH)
    else:
        # Permitir que el usuario suba el archivo manualmente
        st.warning("⚠ No se encontró el archivo Excel en la ruta especificada. Puedes subirlo manualmente.")
        uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])
        if uploaded_file is not None:
            # Guardar el archivo en una ubicación temporal
            temp_path = "datos_temporal.xlsx"
            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ Archivo guardado en {temp_path}")
            return pd.read_excel(temp_path)
        else:
            return pd.DataFrame()

# ------------------- GUARDAR EN SQLITE -------------------
def save_to_sqlite(df):
    conn = sqlite3.connect(SQLITE_PATH)
    df.to_sql("escuelas_docentes", conn, if_exists="replace", index=False)
    conn.close()

# ------------------- INTERFAZ STREAMLIT -------------------
df = load_data()

if not df.empty:
    st.dataframe(df)

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

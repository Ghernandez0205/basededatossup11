import streamlit as st
import pandas as pd
import sqlite3
import os
from io import BytesIO

# Ruta del archivo Excel local
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"

# Verificar si el archivo Excel existe
if not os.path.exists(EXCEL_PATH):
    st.error("❌ No se encontró el archivo Excel en la ruta especificada.")
    st.stop()

# Cargar el archivo Excel
@st.cache_data
def load_excel(file_path):
    return pd.ExcelFile(file_path)

excel_data = load_excel(EXCEL_PATH)

# Lista de hojas disponibles en el archivo
hojas = excel_data.sheet_names

# Interfaz de Streamlit
st.title("📌 Gestión de Escuelas y Docentes")
st.sidebar.header("📂 Opciones de visualización")

# Seleccionar la hoja de Excel a visualizar
sheet_selected = st.sidebar.selectbox("Seleccionar Hoja", hojas)

# Cargar datos de la hoja seleccionada
df = pd.read_excel(EXCEL_PATH, sheet_name=sheet_selected)

# Mostrar datos en Streamlit
st.subheader(f"📊 Datos de la hoja: {sheet_selected}")
st.dataframe(df, use_container_width=True)

# Función para agregar datos nuevos
st.sidebar.subheader("➕ Agregar Nueva Entrada")
cols = df.columns.tolist()
new_data = {col: st.sidebar.text_input(f"Ingresar {col}") for col in cols}

if st.sidebar.button("Agregar"):
    new_row = pd.DataFrame([new_data])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_excel(EXCEL_PATH, sheet_name=sheet_selected, index=False)
    st.success("✅ Nueva entrada agregada correctamente.")
    st.rerun()

# Función para eliminar filas seleccionadas
st.sidebar.subheader("❌ Eliminar Registros")
selected_rows = st.multiselect("Seleccionar registros a eliminar", df.index)

if st.sidebar.button("Eliminar Seleccionados"):
    df.drop(selected_rows, inplace=True)
    df.to_excel(EXCEL_PATH, sheet_name=sheet_selected, index=False)
    st.success("✅ Registros eliminados correctamente.")
    st.rerun()

# Función para descargar archivos en diferentes formatos
st.subheader("📥 Descargar Base de Datos")
formatos = ["Excel", "CSV", "SQLite"]
formato = st.selectbox("Selecciona el formato de descarga", formatos)

if st.button("Descargar"):
    if formato == "Excel":
        output = BytesIO()
        with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
            df.to_excel(writer, sheet_name="Datos", index=False)
        output.seek(0)
        st.download_button("📥 Descargar Excel", output, file_name="datos.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    elif formato == "CSV":
        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button("📥 Descargar CSV", csv_data, file_name="datos.csv", mime="text/csv")

    elif formato == "SQLite":
        db_path = "datos.sqlite"
        conn = sqlite3.connect(db_path)
        df.to_sql(sheet_selected, conn, if_exists="replace", index=False)
        conn.close()
        with open(db_path, "rb") as f:
            st.download_button("📥 Descargar SQLite", f, file_name="datos.sqlite", mime="application/octet-stream")


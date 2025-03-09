import streamlit as st
import pandas as pd
import sqlite3
import os
from datetime import datetime

# Ruta de la base de datos SQLite
DB_PATH = "C:\\Users\\sup11\\OneDrive\\Attachments\\Documentos\\Interfaces de phyton\\Base de datos\\datos.sqlite"

# Cargar la base de datos
@st.cache_data
def cargar_datos():
    conn = sqlite3.connect(DB_PATH)
    df_docentes = pd.read_sql("SELECT * FROM docentes", conn)
    df_escuelas = pd.read_sql("SELECT * FROM escuelas", conn)
    df_documentacion = pd.read_sql("SELECT * FROM documentacion", conn)
    df_situaciones = pd.read_sql("SELECT * FROM situaciones", conn)
    conn.close()
    return df_docentes, df_escuelas, df_documentacion, df_situaciones

# Guardar datos en la base de datos

def guardar_datos(df, tabla):
    conn = sqlite3.connect(DB_PATH)
    df.to_sql(tabla, conn, if_exists='replace', index=False)
    conn.close()
    st.success(f"Cambios guardados en la base de datos en la tabla {tabla}.")

# Interfaz
st.title("📘 Gestión de Docentes y Escuelas")
tabs = st.tabs(["📂 Documentación Inicial", "📋 Seguimiento de Documentación", "🚨 Situaciones Especiales", "📊 Generación de Reportes"])

df_docentes, df_escuelas, df_documentacion, df_situaciones = cargar_datos()

# 📂 Documentación Inicial
with tabs[0]:
    st.header("📂 Documentación Inicial")
    docente_seleccionado = st.selectbox("Selecciona un docente", df_docentes['Nombre'] + " " + df_docentes['Apellido_Paterno'] + " " + df_docentes['Apellido_Materno'])
    docs = ['Hoja de Datos', 'Reanudación', 'Horarios', 'FUP', 'Talón de Pago', 'Solicitud Día Económico']
    docs_entregados = st.multiselect("Selecciona los documentos entregados", docs)
    if st.button("Guardar Documentación Inicial"):
        df_documentacion = df_documentacion.append({"Docente": docente_seleccionado, "Documentos": ", ".join(docs_entregados), "Fecha_Entrega": datetime.now().strftime("%Y-%m-%d")}, ignore_index=True)
        guardar_datos(df_documentacion, "documentacion")

# 📋 Seguimiento de Documentación
with tabs[1]:
    st.header("📋 Seguimiento de Documentación")
    docente_seguimiento = st.selectbox("Selecciona un docente", df_docentes['Nombre'] + " " + df_docentes['Apellido_Paterno'] + " " + df_docentes['Apellido_Materno'], key="seguimiento")
    df_filtrado = df_documentacion[df_documentacion["Docente"] == docente_seguimiento]
    st.dataframe(df_filtrado)

# 🚨 Situaciones Especiales
with tabs[2]:
    st.header("🚨 Situaciones Especiales")
    docentes_afectados = st.multiselect("Selecciona los docentes afectados", df_docentes['Nombre'] + " " + df_docentes['Apellido_Paterno'] + " " + df_docentes['Apellido_Materno'])
    descripcion = st.text_area("Describe la situación especial")
    if st.button("Guardar Situación Especial"):
        for docente in docentes_afectados:
            df_situaciones = df_situaciones.append({"Docente": docente, "Descripción": descripcion, "Fecha": datetime.now().strftime("%Y-%m-%d")}, ignore_index=True)
        guardar_datos(df_situaciones, "situaciones")

# 📊 Generación de Reportes
with tabs[3]:
    st.header("📊 Generación de Reportes")
    columnas = st.multiselect("Selecciona qué columnas exportar", df_docentes.columns)
    if st.button("Exportar a Excel"):
        ruta_exportacion = os.path.join(os.getcwd(), "reporte_exportado.xlsx")
        df_docentes[columnas].to_excel(ruta_exportacion, index=False)
        st.success(f"Reporte guardado en: {ruta_exportacion}")
    if st.button("Exportar a SQLite"):
        guardar_datos(df_docentes[columnas], "reporte")


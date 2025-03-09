import streamlit as st
import pandas as pd
import sqlite3
import os

# 🔗 Configuración de la ruta de la base de datos SQLite
DB_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

# 🛠️ Función para conectarse a la base de datos
def get_connection():
    if os.path.exists(DB_PATH):
        return sqlite3.connect(DB_PATH, check_same_thread=False)
    else:
        st.error("❌ No se encontró la base de datos en la ruta especificada.")
        return None

conn = get_connection()

# Si la conexión falla, se detiene la ejecución
if conn is None:
    st.stop()

# 📌 Función para cargar datos de una tabla
def load_data(table_name):
    try:
        query = f"SELECT * FROM {table_name}"
        df = pd.read_sql(query, conn)
        return df
    except Exception as e:
        st.error(f"⚠️ Error al cargar la tabla '{table_name}': {e}")
        return pd.DataFrame()

# 📌 Obtener lista de tablas disponibles
def get_table_names():
    try:
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = pd.read_sql(query, conn)
        return tables["name"].tolist()
    except Exception as e:
        st.error(f"⚠️ No se pudieron obtener las tablas: {e}")
        return []

# 🎨 **Diseño de la interfaz**
st.title("📊 Gestión de Base de Datos")

# 📌 Mostrar lista de tablas disponibles
tables = get_table_names()
if not tables:
    st.error("⚠️ No hay tablas disponibles en la base de datos.")
    st.stop()

selected_table = st.selectbox("📌 Selecciona una tabla para visualizar:", tables)

# 📊 Cargar y mostrar datos en una tabla interactiva
df = load_data(selected_table)
if df.empty:
    st.warning(f"⚠️ La tabla '{selected_table}' no tiene registros.")
else:
    st.write("📋 **Datos de la tabla seleccionada:**")
    st.dataframe(df, use_container_width=True)

# 📈 **Visualización Gráfica**
if not df.empty:
    st.subheader("📊 Gráfico de Datos")

    numeric_columns = df.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_columns:
        x_axis = st.selectbox("📌 Selecciona el eje X:", numeric_columns)
        y_axis = st.selectbox("📌 Selecciona el eje Y:", numeric_columns)
        chart_type = st.radio("📊 Tipo de gráfico", ["Línea", "Barras", "Dispersión"])

        if chart_type == "Línea":
            st.line_chart(df[[x_axis, y_axis]].set_index(x_axis))
        elif chart_type == "Barras":
            st.bar_chart(df[[x_axis, y_axis]].set_index(x_axis))
        elif chart_type == "Dispersión":
            st.scatter_chart(df[[x_axis, y_axis]])
    else:
        st.warning("⚠️ No hay columnas numéricas para graficar.")

# 📥 **Botón para exportar datos a Excel**
st.subheader("📥 Descargar Datos")
if st.button("Exportar a Excel"):
    excel_path = f"{selected_table}.xlsx"
    df.to_excel(excel_path, index=False)
    with open(excel_path, "rb") as f:
        st.download_button(label="📥 Descargar Archivo Excel", data=f, file_name=excel_path, mime="application/vnd.ms-excel")

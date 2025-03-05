import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import os
from st_aggrid import AgGrid, GridOptionsBuilder

# Configurar la ruta de la base de datos normalizada
DB_PATH = "/mnt/data/base_datos_29D_normalizada.sqlite"

# Conectar a la base de datos
@st.cache_resource
def get_connection():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

conn = get_connection()

# Función para verificar si una tabla existe
def check_table_exists(table_name):
    query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
    result = pd.read_sql(query, conn)
    return not result.empty

# Función para cargar datos de la base de datos
def load_data(query):
    try:
        return pd.read_sql(query, conn)
    except Exception as e:
        st.error(f"Error al ejecutar la consulta SQL: {e}")
        return pd.DataFrame()

# Cargar datos de escuelas
if check_table_exists("escuelas"):
    escuelas_df = load_data("SELECT * FROM escuelas")
else:
    escuelas_df = pd.DataFrame()
    st.error("❌ La tabla 'escuelas' no existe en la base de datos.")

# Función para actualizar la base de datos
def update_database(table_name, df):
    conn = get_connection()
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.commit()

# Función para generar enlace de descarga de la base de datos
def download_database():
    with open(DB_PATH, "rb") as f:
        db_bytes = f.read()
    return db_bytes

# Configurar la interfaz de Streamlit
st.title("📌 Gestión de Docentes y Escuelas")

# Barra lateral para navegación
menu = st.sidebar.radio("Menú", ["Dashboard", "Gestión de Escuelas"])

if menu == "Gestión de Escuelas":
    st.subheader("🏫 Gestión de Escuelas")
    
    # Configurar la tabla editable
    gb = GridOptionsBuilder.from_dataframe(escuelas_df)
    gb.configure_default_column(editable=True)
    gb.configure_pagination()
    gb.configure_side_bar()
    grid_options = gb.build()

    response = AgGrid(escuelas_df, gridOptions=grid_options, editable=True, fit_columns_on_grid_load=True)
    updated_df = response['data']
    
    # Botón para guardar cambios en la base de datos
    if st.button("Guardar Cambios"):
        update_database("escuelas", updated_df)
        st.success("✅ Los cambios han sido guardados correctamente.")

    # Botón para agregar nueva escuela
    with st.form("agregar_escuela"):
        st.subheader("➕ Agregar Nueva Escuela")
        nombre = st.text_input("Nombre de la escuela")
        director = st.text_input("Nombre del director")
        direccion = st.text_input("Dirección")
        zona = st.text_input("Zona Escolar")
        sector = st.text_input("Sector")
        submit_button = st.form_submit_button("Agregar Escuela")
    
    if submit_button and nombre and director and direccion and zona and sector:
        nueva_escuela = pd.DataFrame([[nombre, director, direccion, zona, sector]],
                                     columns=["nombre", "director", "direccion", "zona", "sector"])
        escuelas_df = pd.concat([escuelas_df, nueva_escuela], ignore_index=True)
        update_database("escuelas", escuelas_df)
        st.success("✅ Escuela agregada exitosamente.")
    
    # Botón para eliminar una escuela seleccionada
    selected_rows = response['selected_rows']
    if selected_rows and st.button("Eliminar Escuela"):
        escuelas_df = escuelas_df[~escuelas_df['nombre'].isin([row['nombre'] for row in selected_rows])]
        update_database("escuelas", escuelas_df)
        st.success("✅ Escuela eliminada exitosamente.")

    # Botón para descargar la base de datos
    st.subheader("📥 Descargar Base de Datos")
    db_bytes = download_database()
    st.download_button(label="Descargar Base de Datos", data=db_bytes, file_name="base_datos_actualizada.sqlite", mime="application/octet-stream")


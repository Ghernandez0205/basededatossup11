import streamlit as st
import pandas as pd
import sqlite3
import os
import matplotlib.pyplot as plt

# Definir rutas
EXCEL_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.xlsx"
SQLITE_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.sqlite"

# Cargar Excel automáticamente
def load_excel():
    if os.path.exists(EXCEL_PATH):
        return pd.read_excel(EXCEL_PATH, sheet_name=None)
    else:
        st.error("❌ No se encontró el archivo Excel en la ruta especificada.")
        return None

# Guardar cambios en SQLite
def save_to_sqlite(df_dict):
    conn = sqlite3.connect(SQLITE_PATH)
    for sheet_name, df in df_dict.items():
        df.to_sql(sheet_name, conn, if_exists='replace', index=False)
    conn.close()

# Cargar datos desde SQLite
def load_from_sqlite():
    conn = sqlite3.connect(SQLITE_PATH)
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    tables = pd.read_sql(query, conn)['name'].tolist()
    df_dict = {table: pd.read_sql(f"SELECT * FROM {table}", conn) for table in tables}
    conn.close()
    return df_dict

# Configurar la interfaz
st.title("📌 Gestión de Escuelas y Docentes")
st.sidebar.header("Opciones de Visualización")
view_option = st.sidebar.radio("Selecciona una vista:", ["Tabla", "Gráficos", "Filtros Avanzados"])

# Cargar datos
excel_data = load_excel()
if excel_data:
    save_to_sqlite(excel_data)  # Guardar en SQLite automáticamente
    data = load_from_sqlite()  # Cargar desde SQLite
    selected_table = st.sidebar.selectbox("Selecciona una tabla:", list(data.keys()))
    df = data[selected_table]

    if view_option == "Tabla":
        st.subheader(f"📋 Datos de {selected_table}")
        edited_df = st.data_editor(df, use_container_width=True)
        if st.button("Guardar Cambios en SQLite"):
            save_to_sqlite({selected_table: edited_df})
            st.success("✅ Cambios guardados en SQLite")

    elif view_option == "Gráficos":
        st.subheader("📊 Análisis Gráfico")
        column = st.selectbox("Selecciona una columna para visualizar:", df.columns)
        fig, ax = plt.subplots()
        df[column].value_counts().plot(kind='bar', ax=ax)
        st.pyplot(fig)

    elif view_option == "Filtros Avanzados":
        st.subheader("🔍 Filtrar Datos")
        filter_column = st.selectbox("Selecciona una columna para filtrar:", df.columns)
        unique_values = df[filter_column].unique()
        selected_value = st.selectbox("Selecciona un valor:", unique_values)
        filtered_df = df[df[filter_column] == selected_value]
        st.dataframe(filtered_df)

    # Opciones de descarga
    st.sidebar.subheader("📥 Descargar Base de Datos")
    if st.sidebar.button("Descargar Excel"):
        excel_buffer = pd.ExcelWriter(EXCEL_PATH, engine='xlsxwriter')
        for table, df in data.items():
            df.to_excel(excel_buffer, sheet_name=table, index=False)
        excel_buffer.close()
        st.sidebar.download_button("Descargar Excel", open(EXCEL_PATH, "rb"), "datos_actualizados.xlsx")

    if st.sidebar.button("Descargar CSV"):
        csv_buffer = df.to_csv(index=False).encode("utf-8")
        st.sidebar.download_button("Descargar CSV", csv_buffer, "datos_actualizados.csv", "text/csv")

    if st.sidebar.button("Descargar SQLite"):
        st.sidebar.download_button("Descargar SQLite", open(SQLITE_PATH, "rb"), "datos_actualizados.sqlite")

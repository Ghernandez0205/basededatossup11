import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import os

# Configurar la ruta de la base de datos
DB_PATH = "C:\\Users\\sup11\\OneDrive\\Attachments\\Documentos\\Interfaces de phyton\\Base de datos\\base_datos_29D_normalizada.sqlite"

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

# Cargar datos de docentes
if check_table_exists("personal_educativo"):
    docentes_df = load_data("SELECT * FROM personal_educativo")
else:
    docentes_df = pd.DataFrame()
    st.error("❌ La tabla 'personal_educativo' no existe en la base de datos.")

# Cargar datos de escuelas
if check_table_exists("escuelas"):
    escuelas_df = load_data("SELECT * FROM escuelas")
else:
    escuelas_df = pd.DataFrame()
    st.error("❌ La tabla 'escuelas' no existe en la base de datos.")

# Cargar relación docentes-escuelas
if check_table_exists("docente_escuela"):
    docente_escuela_df = load_data("SELECT * FROM docente_escuela")
else:
    docente_escuela_df = pd.DataFrame()
    st.error("❌ La tabla 'docente_escuela' no existe en la base de datos.")

# Cargar historial de auditoría
if check_table_exists("auditoria_cambios"):
    auditoria_df = load_data("SELECT * FROM auditoria_cambios")
else:
    auditoria_df = pd.DataFrame()
    st.error("❌ La tabla 'auditoria_cambios' no existe en la base de datos.")

# Configurar la interfaz de Streamlit
st.title("📌 Gestión de Docentes y Escuelas")

# Barra lateral para navegación
menu = st.sidebar.radio("Menú", ["Dashboard", "Gestión de Docentes", "Gestión de Escuelas", "Gestión de Claves Presupuestales", "Historial de Auditoría", "Exportación de Datos"])

if menu == "Dashboard":
    st.subheader("📊 Resumen de Datos")
    if not docentes_df.empty:
        fig, ax = plt.subplots()
        docentes_df["Nivel_Educativo"].value_counts().plot(kind="bar", ax=ax, color=["#0047AB", "#E63946", "#F4A261"])
        ax.set_title("Distribución de Docentes por Nivel Educativo")
        ax.set_ylabel("Cantidad")
        st.pyplot(fig)
    else:
        st.warning("No hay datos disponibles para mostrar.")

elif menu == "Gestión de Docentes":
    st.subheader("📋 Lista de Docentes")
    st.dataframe(docentes_df)
    
    with st.form("add_docente"):
        st.write("Agregar Nuevo Docente")
        rfc = st.text_input("RFC")
        nombre = st.text_input("Nombre Completo")
        nivel = st.selectbox("Nivel Educativo", docentes_df["Nivel_Educativo"].unique() if not docentes_df.empty else [])
        escuela = st.selectbox("Escuela", escuelas_df["Nombre_Escuela"].unique() if not escuelas_df.empty else [])
        clave_pres = st.text_input("Clave Presupuestal")
        if st.form_submit_button("Guardar Docente"):
            conn.execute("INSERT INTO personal_educativo (RFC, Nombre, Nivel_Educativo, Clave_Presupuestal) VALUES (?, ?, ?, ?)", (rfc, nombre, nivel, clave_pres))
            conn.commit()
            st.success("Docente agregado correctamente")
    
    if not docentes_df.empty:
        eliminar = st.selectbox("Seleccionar Docente a Eliminar", docentes_df["RFC"])
        if st.button("Eliminar Docente"):
            conn.execute("DELETE FROM personal_educativo WHERE RFC = ?", (eliminar,))
            conn.commit()
            st.warning("Docente eliminado")

elif menu == "Gestión de Escuelas":
    st.subheader("🏫 Gestión de Escuelas")
    st.dataframe(escuelas_df)
    
    with st.form("add_escuela"):
        st.write("Agregar Nueva Escuela")
        nombre_escuela = st.text_input("Nombre de la Escuela")
        director = st.text_input("Director")
        direccion = st.text_input("Dirección")
        zona = st.text_input("Zona Escolar")
        sector = st.number_input("Sector", min_value=1, step=1)
        if st.form_submit_button("Guardar Escuela"):
            conn.execute("INSERT INTO escuelas (Nombre_Escuela, Director, Direccion, Zona_Escolar, Sector) VALUES (?, ?, ?, ?, ?)", (nombre_escuela, director, direccion, zona, sector))
            conn.commit()
            st.success("Escuela agregada correctamente")
    
elif menu == "Gestión de Claves Presupuestales":
    st.subheader("🔑 Gestión de Claves Presupuestales")
    st.dataframe(docente_escuela_df)
    
elif menu == "Historial de Auditoría":
    st.subheader("📜 Historial de Auditoría")
    st.dataframe(auditoria_df)
    
elif menu == "Exportación de Datos":
    st.subheader("📥 Exportación de Datos")
    
    def export_excel(dataframe):
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            dataframe.to_excel(writer, index=False, sheet_name="Datos Filtrados")
        processed_data = output.getvalue()
        return processed_data
    
    st.download_button(
        label="📥 Descargar Excel",
        data=export_excel(docentes_df),
        file_name="datos_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    def export_sqlite(dataframe, db_name="exported_db.sqlite"):
        export_path = os.path.join(os.getcwd(), db_name)
        conn_export = sqlite3.connect(export_path)
        dataframe.to_sql("personal_educativo", conn_export, if_exists="replace", index=False)
        conn_export.close()
        return export_path
    
    if st.button("📤 Exportar a SQLite"):
        sqlite_file = export_sqlite(docentes_df)
        with open(sqlite_file, "rb") as f:
            st.download_button("📥 Descargar SQLite", f, file_name="datos_filtrados.sqlite")

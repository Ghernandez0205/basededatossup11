import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt
from io import BytesIO
import os

# Configurar la ruta de la base de datos normalizada
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

# Cargar claves presupuestales
if check_table_exists("claves_presupuestales"):
    claves_pres_df = load_data("SELECT * FROM claves_presupuestales")
else:
    claves_pres_df = pd.DataFrame()
    st.error("❌ La tabla 'claves_presupuestales' no existe en la base de datos.")

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
    docentes_completo_df = docentes_df.merge(claves_pres_df, on="RFC", how="left")
    st.dataframe(docentes_completo_df)
    
elif menu == "Gestión de Escuelas":
    st.subheader("🏫 Gestión de Escuelas")
    st.dataframe(escuelas_df)
    
elif menu == "Gestión de Claves Presupuestales":
    st.subheader("🔑 Gestión de Claves Presupuestales")
    st.dataframe(claves_pres_df)
    
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
        data=export_excel(docentes_completo_df),
        file_name="datos_filtrados.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

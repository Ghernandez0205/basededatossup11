import streamlit as st
import pandas as pd
import sqlite3
import os

# Ruta de la base de datos en OneDrive
EXCEL_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.xlsx"
SQLITE_PATH = "C:/Users/sup11/OneDrive/Attachments/Documentos/Interfaces de phyton/Base de datos/datos.sqlite"

def load_excel():
    """Carga el archivo Excel y lo convierte en un DataFrame"""
    try:
        df = pd.read_excel(EXCEL_PATH)
        return df
    except Exception as e:
        st.error(f"Error al cargar el archivo: {e}")
        return pd.DataFrame()

def save_excel(df):
    """Guarda los cambios en el archivo Excel"""
    try:
        df.to_excel(EXCEL_PATH, index=False)
        st.success("📁 Archivo guardado exitosamente en OneDrive.")
    except Exception as e:
        st.error(f"Error al guardar el archivo: {e}")

def connect_db():
    """Conectar a la base de datos SQLite y crearla si no existe"""
    conn = sqlite3.connect(SQLITE_PATH)
    return conn

def save_to_sqlite(df):
    """Guardar los datos en SQLite"""
    conn = connect_db()
    df.to_sql("docentes", conn, if_exists="replace", index=False)
    conn.close()
    st.success("✅ Datos guardados en la base de datos SQLite")

def check_special_characters(text):
    """Verifica si el texto contiene caracteres especiales no permitidos"""
    special_chars = "áéíóúÁÉÍÓÚñÑ"  # Se pueden agregar más
    if any(char in special_chars for char in text):
        return True
    return False

# Streamlit UI
st.title("📚 Gestión de Docentes y Escuelas")

# Cargar datos
df = load_excel()

# Barra lateral con opciones
st.sidebar.header("Opciones")
menu = st.sidebar.radio("Selecciona una sección", ["📄 Lista de Docentes", "🏫 Escuelas", "📑 Documentación", "📊 Reportes", "⚙ Configuración"])

if menu == "📄 Lista de Docentes":
    st.header("📄 Lista de Docentes")
    filtro_rfc = st.text_input("🔍 Buscar por RFC")
    filtro_escuela = st.text_input("🏫 Buscar por Escuela")
    
    # Filtrado avanzado
    if filtro_rfc:
        df = df[df["RFC"].astype(str).str.contains(filtro_rfc, case=False, na=False)]
    if filtro_escuela:
        df = df[df["Escuela"].astype(str).str.contains(filtro_escuela, case=False, na=False)]
    
    st.dataframe(df)
    
    # Opciones para agregar/borrar
    if st.button("➕ Agregar Docente"):
        with st.form("Nuevo Docente"):
            nombre = st.text_input("Nombre Completo")
            rfc = st.text_input("RFC")
            escuela = st.text_input("Escuela")
            clave = st.text_input("Clave Presupuestal")
            enviar = st.form_submit_button("Guardar")
            
            if enviar:
                if check_special_characters(nombre) or check_special_characters(escuela):
                    st.warning("⚠️ Evita el uso de caracteres especiales como acentos o ñ.")
                else:
                    nuevo_dato = {"Nombre": nombre, "RFC": rfc, "Escuela": escuela, "Clave": clave}
                    df = df.append(nuevo_dato, ignore_index=True)
                    save_excel(df)
    
elif menu == "🏫 Escuelas":
    st.header("🏫 Gestión de Escuelas")
    
    escuela_nueva = st.text_input("🏫 Nueva Escuela")
    if st.button("➕ Agregar Escuela"):
        if check_special_characters(escuela_nueva):
            st.warning("⚠️ Evita el uso de caracteres especiales como acentos o ñ.")
        else:
            df["Escuela"].append(escuela_nueva)
            save_excel(df)

elif menu == "📑 Documentación":
    st.header("📑 Seguimiento de Documentación")
    doc_inicial = ["Hoja de Datos", "Reanudación", "Horarios"]
    doc_adicional = ["FUP", "Talón de Pago", "Solicitud Día Económico"]
    
    for doc in doc_inicial:
        df[doc] = st.checkbox(f"📌 {doc}")
    for doc in doc_adicional:
        df[doc] = st.checkbox(f"📌 {doc}")
    
    if st.button("💾 Guardar Documentación"):
        save_excel(df)

elif menu == "📊 Reportes":
    st.header("📊 Generación de Reportes")
    
    columnas = st.multiselect("📌 Selecciona qué columnas exportar", df.columns.tolist())
    
    if st.button("📥 Exportar a Excel"):
        df[columnas].to_excel("Reporte.xlsx", index=False)
        st.success("📁 Reporte generado correctamente")
    if st.button("📥 Exportar a SQLite"):
        save_to_sqlite(df)

elif menu == "⚙ Configuración":
    st.header("⚙ Configuración del Sistema")
    if st.button("🔄 Recargar Base de Datos"):
        df = load_excel()
        st.success("🔄 Base de datos actualizada correctamente.")

import streamlit as st
import pandas as pd
import os

# 📌 Ruta del archivo Excel (Usar `r""` para evitar problemas con caracteres especiales)
EXCEL_PATH = r"C:\Users\sup11\OneDrive\Attachments\Documentos\Interfaces de phyton\Base de datos\datos.xlsx"

# 📌 Cargar datos desde Excel
@st.cache_data
def cargar_datos():
    """Carga los datos desde Excel en DataFrames."""
    try:
        df_docentes = pd.read_excel(EXCEL_PATH, sheet_name="docentes")
        df_escuelas = pd.read_excel(EXCEL_PATH, sheet_name="escuelas")
        df_documentacion = pd.read_excel(EXCEL_PATH, sheet_name="documentacion")
        df_situaciones = pd.read_excel(EXCEL_PATH, sheet_name="situaciones_especiales")

        return df_docentes, df_escuelas, df_documentacion, df_situaciones
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return None, None, None, None

# 📌 Guardar datos en Excel
def guardar_datos(df_docentes, df_escuelas, df_documentacion, df_situaciones):
    """Guarda los cambios en el archivo Excel."""
    try:
        with pd.ExcelWriter(EXCEL_PATH, engine="openpyxl") as writer:
            df_docentes.to_excel(writer, sheet_name="docentes", index=False)
            df_escuelas.to_excel(writer, sheet_name="escuelas", index=False)
            df_documentacion.to_excel(writer, sheet_name="documentacion", index=False)
            df_situaciones.to_excel(writer, sheet_name="situaciones_especiales", index=False)
        st.success("✅ Datos guardados correctamente en Excel.")
    except Exception as e:
        st.error(f"❌ Error al guardar los datos: {e}")

# 📌 Interfaz Principal
st.title("📚 Gestión de Docentes y Escuelas")

# 📌 Cargar los datos
df_docentes, df_escuelas, df_documentacion, df_situaciones = cargar_datos()

# 📌 Seleccionar Vista
opcion = st.sidebar.radio("📌 Selecciona una opción:", ["Docentes", "Escuelas", "Seguimiento de Documentación", "Situaciones Especiales", "Exportar Datos"])

## **🔹 Gestión de Docentes**
if opcion == "Docentes":
    st.subheader("👨‍🏫 Gestión de Docentes")
    st.dataframe(df_docentes)

    # 📌 Agregar Nuevo Docente
    with st.expander("➕ Agregar Docente"):
        nuevo_nombre = st.text_input("Nombre del Docente")
        nuevo_apellido = st.text_input("Apellido del Docente")
        nuevo_rfc = st.text_input("RFC del Docente")

        if st.button("Guardar Docente"):
            nuevo_docente = pd.DataFrame({"Nombre": [nuevo_nombre], "Apellido": [nuevo_apellido], "RFC": [nuevo_rfc]})
            df_docentes = pd.concat([df_docentes, nuevo_docente], ignore_index=True)
            guardar_datos(df_docentes, df_escuelas, df_documentacion, df_situaciones)

    # 📌 Filtrar Docentes
    filtro_rfc = st.text_input("🔍 Filtrar por RFC")
    if filtro_rfc:
        df_filtrado = df_docentes[df_docentes["RFC"].str.contains(filtro_rfc, case=False, na=False)]
        st.dataframe(df_filtrado)

## **🔹 Gestión de Escuelas**
elif opcion == "Escuelas":
    st.subheader("🏫 Gestión de Escuelas")
    st.dataframe(df_escuelas)

    # 📌 Agregar Nueva Escuela
    with st.expander("➕ Agregar Escuela"):
        nueva_escuela = st.text_input("Nombre de la Escuela")
        nuevo_docente_asociado = st.selectbox("Docente Asociado", df_docentes["Nombre"])

        if st.button("Guardar Escuela"):
            nueva_fila = pd.DataFrame({"Escuela": [nueva_escuela], "Docente": [nuevo_docente_asociado]})
            df_escuelas = pd.concat([df_escuelas, nueva_fila], ignore_index=True)
            guardar_datos(df_docentes, df_escuelas, df_documentacion, df_situaciones)

## **🔹 Seguimiento de Documentación**
elif opcion == "Seguimiento de Documentación":
    st.subheader("📜 Seguimiento de Documentación")

    # 📌 Mostrar tabla con colores
    def aplicar_colores(val):
        if val == "Entregado":
            return "background-color: green; color: white"
        elif val == "Pendiente":
            return "background-color: yellow"
        elif val == "Faltante":
            return "background-color: red; color: white"
        return ""

    st.dataframe(df_documentacion.style.applymap(aplicar_colores))

## **🔹 Situaciones Especiales**
elif opcion == "Situaciones Especiales":
    st.subheader("⚠️ Registro de Situaciones Especiales")

    # 📌 Agregar Nueva Situación
    with st.expander("➕ Registrar Nueva Situación"):
        docente_afectado = st.selectbox("Docente Afectado", df_docentes["Nombre"])
        escuela_asociada = st.selectbox("Escuela Asociada", df_escuelas["Escuela"])
        descripcion = st.text_area("Descripción de la Situación")

        if st.button("Registrar Situación"):
            nueva_fila = pd.DataFrame({"Docente": [docente_afectado], "Escuela": [escuela_asociada], "Situación": [descripcion]})
            df_situaciones = pd.concat([df_situaciones, nueva_fila], ignore_index=True)
            guardar_datos(df_docentes, df_escuelas, df_documentacion, df_situaciones)

    # 📌 Mostrar Situaciones Registradas
    st.dataframe(df_situaciones)

## **🔹 Exportación de Datos**
elif opcion == "Exportar Datos":
    st.subheader("📤 Exportación de Datos")

    # 📌 Descargar en Excel
    excel_data = df_docentes.to_csv(index=False).encode('utf-8')
    st.download_button(label="📥 Descargar Docentes en CSV", data=excel_data, file_name="docentes.csv", mime="text/csv")

    # 📌 Descargar en SQLite
    if st.button("📥 Guardar Base de Datos en SQLite"):
        conn = sqlite3.connect("datos_exportados.sqlite")
        df_docentes.to_sql("docentes", conn, if_exists="replace", index=False)
        df_escuelas.to_sql("escuelas", conn, if_exists="replace", index=False)
        df_documentacion.to_sql("documentacion", conn, if_exists="replace", index=False)
        df_situaciones.to_sql("situaciones_especiales", conn, if_exists="replace", index=False)
        conn.close()
        st.success("✅ Datos guardados en SQLite con éxito.")


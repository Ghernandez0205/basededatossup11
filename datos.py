import streamlit as st
import sqlite3
import pandas as pd
import os

# 🌟 Estilo general de la aplicación
st.set_page_config(page_title="Gestión de Base de Datos", page_icon="📊", layout="wide")
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Gestión de Base de Datos</h1>", unsafe_allow_html=True)

# 📂 Selección y carga de la base de datos
uploaded_file = st.file_uploader("📂 Sube la base de datos SQLite", type=["sqlite"])

if uploaded_file:
    DB_PATH = f"/mnt/data/{uploaded_file.name}"
    with open(DB_PATH, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Base de datos cargada correctamente: {uploaded_file.name}")

    # Conexión a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Obtener nombres de las tablas
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tablas = [tabla[0] for tabla in cursor.fetchall()]

    # Diccionario para nombres legibles
    tabla_nombres_legibles = {
        "personal_educativo": "👩‍🏫 Personal Educativo",
        "escuelas": "🏫 Escuelas",
        "sqlite_sequence": "⚙️ Secuencia SQLite",
        "claves_presupuestales": "💰 Claves Presupuestales",
        "docente_escuela": "📚 Docente - Escuela",
        "auditoria_cambios": "📜 Auditoría de Cambios"
    }

    # Mostrar nombres de tablas de forma amigable
    st.sidebar.markdown("## 📌 Selecciona una tabla")
    tabla_seleccionada = st.sidebar.selectbox(
        "Elige una tabla para visualizar:", 
        opciones:= [tabla_nombres_legibles.get(tabla, tabla) for tabla in tablas]
    )

    # Obtener el nombre real de la tabla seleccionada
    tabla_real = next(k for k, v in tabla_nombres_legibles.items() if v == tabla_seleccionada)

    # Mostrar datos de la tabla seleccionada
    st.markdown(f"### 📋 Datos en la tabla **{tabla_seleccionada}**")
    df = pd.read_sql(f"SELECT * FROM {tabla_real}", conn)

    if df.empty:
        st.warning("⚠️ La tabla seleccionada está vacía.")
    else:
        # Opciones de visualización
        vista_opciones = ["Tabla completa", "Primeros 10 registros", "Vista Personalizada"]
        vista_seleccionada = st.radio("📊 Selecciona el tipo de vista", vista_opciones)

        if vista_seleccionada == "Tabla completa":
            st.dataframe(df, use_container_width=True)
        elif vista_seleccionada == "Primeros 10 registros":
            st.dataframe(df.head(10), use_container_width=True)
        else:
            num_filas = st.slider("Número de registros a mostrar:", 5, len(df), 10)
            st.dataframe(df.head(num_filas), use_container_width=True)

    # Botón para descargar la base de datos
    st.subheader("📥 Descargar Base de Datos")
    with open(DB_PATH, "rb") as f:
        db_bytes = f.read()
    st.download_button(label="⬇️ Descargar Base de Datos", data=db_bytes, file_name="base_datos_actualizada.sqlite", mime="application/octet-stream")

    # Cerrar conexión
    conn.close()

else:
    st.warning("⚠️ Por favor, sube un archivo SQLite para continuar.")


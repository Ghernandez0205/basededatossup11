import streamlit as st
import pandas as pd
import tempfile  # Para manejar archivos temporales

# 📂 Cargar archivo
st.header("📂 Sube tu archivo Excel")
uploaded_file = st.file_uploader("Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # 1️⃣ Crear un archivo temporal para guardar el Excel
    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        tmp_file_path = tmp_file.name  # Ruta del archivo temporal

    st.success(f"✅ Archivo guardado temporalmente en {tmp_file_path}")

    # 2️⃣ Leer y mostrar la tabla
    df = pd.read_excel(tmp_file_path)
    st.dataframe(df)

    # 3️⃣ Botón para descargar el archivo en múltiples formatos
    st.download_button(
        label="📥 Descargar Excel",
        data=uploaded_file.getvalue(),
        file_name="datos.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

else:
    st.warning("⚠️ No se ha subido ningún archivo todavía.")

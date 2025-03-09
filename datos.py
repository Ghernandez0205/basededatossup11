import streamlit as st
import os
import pandas as pd

# 1️⃣ Subir el archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # 2️⃣ Asegurar que el archivo se guarda en /mnt/data
    file_path = os.path.join("/mnt/data", uploaded_file.name)

    try:
        # 3️⃣ Guardar el archivo en /mnt/data
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Archivo guardado en {file_path}")

        # 4️⃣ Leer y mostrar el archivo
        df = pd.read_excel(file_path)
        st.dataframe(df)  # Mostrar datos en tabla

    except Exception as e:
        st.error(f"❌ Error al guardar el archivo: {str(e)}")

else:
    st.warning("⚠️ No se ha subido ningún archivo todavía.")

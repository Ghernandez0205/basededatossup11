import streamlit as st
import os
import pandas as pd

# 1️⃣ Subir el archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

# 2️⃣ Si se sube el archivo, guardarlo en `/mnt/data`
if uploaded_file is not None:
    file_path = os.path.join("/mnt/data", uploaded_file.name)

    # Guardar el archivo
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Archivo guardado en {file_path}")

    # 3️⃣ Leer y mostrar el archivo
    df = pd.read_excel(file_path)
    st.dataframe(df)  # Mostrar datos en tabla

else:
    st.warning("⚠️ No se ha subido ningún archivo todavía.")

import streamlit as st
import os
import pandas as pd

# Crear la carpeta en Streamlit Cloud si no existe
save_dir = "/mnt/data"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

# 1️⃣ Subir el archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # 2️⃣ Asegurar que el archivo se guarda en /mnt/data
    file_path = os.path.join(save_dir, uploaded_file.name)

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

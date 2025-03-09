import streamlit as st
import os
import pandas as pd

# 1️⃣ Crear la carpeta en Streamlit Cloud (si no existe)
save_dir = "/mnt/data"
os.makedirs(save_dir, exist_ok=True)  # Esto evita errores si la carpeta ya existe

# 2️⃣ Subir el archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # 3️⃣ Definir la ruta de guardado en /mnt/data
    file_path = os.path.join(save_dir, uploaded_file.name)

    try:
        # 4️⃣ Guardar el archivo
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        st.success(f"✅ Archivo guardado en {file_path}")

        # 5️⃣ Leer y mostrar el archivo
        df = pd.read_excel(file_path)
        st.dataframe(df)  # Mostrar los datos en tabla

    except Exception as e:
        st.error(f"❌ Error al guardar el archivo: {str(e)}")

else:
    st.warning("⚠️ No se ha subido ningún archivo todavía.")

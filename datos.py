import streamlit as st
import os
import pandas as pd

# 📂 Definir el directorio donde se guardará el archivo
save_dir = "/mnt/data"

# 1️⃣ Verificar si la carpeta existe antes de intentar crearla
if not os.path.exists(save_dir):
    try:
        os.makedirs(save_dir, exist_ok=True)
    except Exception as e:
        st.error(f"❌ No se pudo crear el directorio: {str(e)}")

# 2️⃣ Subir el archivo
uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])

if uploaded_file is not None:
    # 3️⃣ Ruta de guardado en /mnt/data
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

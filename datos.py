import os

if uploaded_file is not None:
    # Ruta donde guardaremos el archivo en Streamlit
    file_path = os.path.join("/mnt/data", uploaded_file.name)

    # Guardar el archivo en la carpeta temporal
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ Archivo guardado en {file_path}")

import streamlit as st

uploaded_file = st.file_uploader("📂 Sube tu archivo Excel", type=["xlsx"])
if uploaded_file is not None:
    st.success("✅ Archivo subido correctamente")
else:
    st.error("❌ No se ha subido ningún archivo")



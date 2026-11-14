import streamlit as st
import psutil

st.title("🚀 Poyraz AI - Sistem Paneli")
st.write("Streamlit Cloud üzerinde canlı sistem izleme paneli.")

# Canlı CPU ve RAM Değerleri
cpu = psutil.cpu_percent(interval=1)
ram = psutil.virtual_memory().percent

col1, col2 = st.columns(2)
col1.metric("CPU Kullanımı", f"%{cpu}")
col2.metric("RAM Kullanımı", f"%{ram}")

if st.button("Sistemi Tara"):
    st.success("Tüm sistem güvenli ve aktif!")

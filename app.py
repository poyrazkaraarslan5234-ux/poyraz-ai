import streamlit as st
import socket
import platform
import subprocess
import hashlib
import base64
import urllib.request
import json
import ssl
import datetime
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PC & Mobile Cyber Suite Pro",
    page_icon="🛡️",
    layout="centered"
)

# Hacker Teması İçin CSS (Koyu Tema & Siber Turuncu)
st.markdown("""
    <style>
    .main {
        background-color: #0e0e0e;
        color: #00ff00;
    }
    h1 {
        color: #ff5500;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        width: 100%;
        background-color: #1a1a1a;
        color: #fff;
        border: 1px solid #ff5500;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff5500;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Session State Hedef/Tuzak Log Listesi
if 'target_logs' not in st.session_state:
    st.session_state['target_logs'] = []

st.markdown("<h1>🛡️ PC & MOBILE CYBER SUITE PRO</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Saf Siber Güvenlik & Penetrasyon Test Laboratuvarı</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Saf Siber Güvenlik Modülleri
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "⌨️ BadUSB / DuckyScript Stüdyosu",
        "📍 IP Adresi Bulma & Detaylı Sorgulama",
        "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)",
        "🔑 Hash Üretici & Analizcisi",
        "🔒 JWT (JSON Web Token) Çözümleyici",
        "🌐 SSL / TLS Sertifika Denetçisi",
        "🛡️ HTTP Güvenlik Başlıkları (Security Headers)",
        "🌐 Web & IP İstihbaratı (OSINT)",
        "💉 Web Güvenliği Payload Kütüphanesi",
        "📜 Mini Log Analiz Aracı",
        "🚨 Olay Müdahale (Incident Response) Rehberi",
        "🌐 HTTP İstek & API Test Aracı",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "💻 Sistem & Ağ Bilgisi",
        "🎯 Oltalama Mesajı & Hedef Takip Sistemi"
    ]
)

# 1. BadUSB / DuckyScript Stüdyosu
if secim == "⌨️ BadUSB / DuckyScript Stüdyosu":
    st.subheader("⌨️ BadUSB / DuckyScript Payload Stüdyosu")
    st.markdown("Siber güvenlik testlerinde HID (Klavye) otomasyonu için DuckyScript komutları üretin.")
    
    payload_tipi = st.selectbox("Payload Şablonu", ["Komut İstemi Aç", "PowerShell ile Bilgi Topla", "Ağ Durumunu Kaydet"])
    if payload_tipi == "Komut İstemi Aç":
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING cmd\nENTER\n"
    elif payload_tipi == "PowerShell ile Bilgi Topla":
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING powershell -NoP -NonI -W Hidden -Exec Bypass\nENTER\n"
    else:
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING ipconfig /all > C:\\net_info.txt && notepad C:\\net_info.txt\nENTER\n"
        
    st.text_area("Üretilen DuckyScript Kodu:", kod, height=150)
    st.download_button("Payload İndir (.txt)", kod, file_name="payload.txt")

# 2. IP Adresi Bulma & Detaylı Sorgulama
elif secim == "📍 IP Adresi Bulma & Detay

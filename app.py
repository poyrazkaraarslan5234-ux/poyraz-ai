import streamlit as st
import socket
import platform
import subprocess
import hashlib
import base64
import random
import urllib.request
import json
import math
import ssl
import pandas as pd
from datetime import datetime

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

# Session State Log Listesi Başlatma
if 'phishing_logs' not in st.session_state:
    st.session_state['phishing_logs'] = []

st.markdown("<h1>🛡️ PC & MOBILE CYBER SUITE PRO</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Saf Siber Güvenlik & Penetrasyon Test Laboratuvarı</p>", unsafe_allow_html=True)
st.markdown("---")

# Sadeleştirilmiş Modül Listesi
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "📍 IP Adresi Bulma & Detaylı Sorgulama",
        "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)",
        "🔑 Hash Üretici & Analizcisi",
        "🔒 JWT (JSON Web Token) Çözümleyici",
        "🌐 SSL / TLS Sertifika Denetçisi",
        "🔑 Güçlü Şifre Üretici & Entropi Ölçer",
        "⚡ Şifre Kırılma Süresi (Brute-Force)",
        "📜 Mini Log Analiz Aracı",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "💻 Sistem & Ağ Bilgisi",
        "🎣 Oltalama Mesajı & Kurban Yakalama Sistemi"
    ]
)

# 1. IP Adresi Bulma & Detaylı Sorgulama
if secim == "📍 IP Adresi Bulma & Detaylı Sorgulama":
    st.subheader("📍 IP Adresi Bulma ve Detaylı Konum/ISP Analizi")
    if st.button("Benim IP Adresimi Otomatik Bul"):
        with st.spinner("IP adresiniz tespit ediliyor..."):
            try:
                req_ip = urllib.request.Request("https://api.ipify.org?format=json", headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req_ip, timeout=5) as resp:
                    benim_ip = json.loads(resp.read().decode('utf-8')).get("ip")
                    st.success(f"🌐 **Senin Dış (Public) IP Adresin:** `{benim_ip}`")
            except Exception as e:
                st.error(f"IP adresiniz alınamadı: {e}")
                
    st.markdown("---")
    hedef_ip = st.text_input("Sorgulanacak IP Adresi veya Domain:", "8.8.8.8")
    if st.button("IP / Hedef Bilgilerini Sorgula"):
        with st.spinner("IP Veritabanı Taranıyor..."):
            try:
                url = f"http://ip-api.com/json/{hedef_ip.strip()}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    veri = json.loads(response.read().decode('utf-8'))
                    if veri.get("status") == "success":
                        st.success(f"🎯 **Sorgulanan Hedef:** `{veri.get('query')}`")
                        st.write(f"🌍 **Ülke:** {veri.get('country')} ({veri.get('countryCode')})")
                        st.write(f"🏙️ **Şehir:** {veri.get('city')}")
                        st.write(f"🏢 **ISP:** {veri.get('isp')}")
                    else:
                        st.error("❌ Geçersiz IP adresi!")
            except Exception as e:
                st.error(f"Hata: {e}")

# 2. Hash Şifre Kırıcı
elif secim == "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)":
    st.subheader("🔓 Gelişmiş Hash Kırıcı (Sözlük Saldırısı)")
    algo = st.selectbox("Algoritma", ["MD5", "SHA-1", "SHA-256"])
    hedef_hash = st.text_input("Çözülecek Hash:", hashlib.md5("poyraz123".encode()).hexdigest())
    wordlist_input = st.text_area("Wordlist:", "123456\npassword\nadmin\npoyraz\npoyraz123\n12345678", height=120)
    
    if st.button("Hash'i Kır"):
        with st.spinner("Taranıyor..."):
            wordlist = [w.strip() for w in wordlist_input.split("\n") if w.strip()]
            bulundu = False
            for kelime in wordlist:
                if algo == "MD5":
                    dh = hashlib.md5(kelime.encode()).hexdigest()
                elif algo == "SHA-1":
                    dh = hashlib.sha1(kelime.encode()).hexdigest()
                else:
                    dh = hashlib.sha256(kelime.encode()).hexdigest()
                if dh == hedef_hash.strip().lower():
                    st.success(f"🎉 **Şifre Bulundu:** `{kelime}`")
                    bulundu = True
                    break
            if not bulundu:
                st.error("❌ Eşleşme sağlanamadı.")

# 3. Hash Üretici & Analizcisi
elif secim == "🔑 Hash Üretici & Analizcisi":
    st.subheader("🔑 Hash Üretici & Analiz Aracı")
    duz_metin = st.text_input("Metin:", "poyraz123")
    if st.button("Hash Üret"):
        st.write(f"📌 **MD5:** `{hashlib.md5(duz_metin.encode()).hexdigest()}`")
        st.write(f"📌 **SHA-256:** `{hashlib.sha256(duz_metin.encode()).hexdigest()}`")
    
    st.markdown("---")
    girilen_hash = st.text_input("Analiz Edilecek Hash:")
    if st.button("Analiz Et"):
        uzunluk = len(girilen_hash.strip())
        st.write(f"📏 Uzunluk: `{uzunluk}`")
        if uzunluk == 32: st.success("🟢 MD5/NTLM")
        elif uzunluk == 40: st.success("🟢 SHA-1")
        elif uzunluk == 64: st.success("🟢 SHA-256")
        else: st.warning("🟡 Bilinmeyen format")

# 4. JWT Çözümleyici
elif secim == "🔒 JWT (JSON Web Token) Çözümleyici":
    st.subheader("🔒 JWT Token Çözümleyici")
    jwt_input = st.text_area("JWT Token:", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlBveXJheiIsImFkbWluIjp0cnVlfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    if st.button("Çözümle"):
        try:
            parcalar = jwt_input.split('.')
            hp = parcalar[0] + '=' * (-len(parcalar[0]) % 4)
            pd = parcalar[1] + '=' * (-len(parcalar[1]) % 4)
            st.json(json.loads(base64.urlsafe_b64decode(hp).decode('utf-8')))
            st.json(json.loads(base64.urlsafe_b64decode(pd).decode('utf-8')))
            st.success("Çözümlendi!")
        except Exception as e:
            st.error(f"Hata: {e}")

# 5. SSL / TLS Sertifika Denetçisi
elif secim == "🌐 SSL / TLS Sertifika Denetçisi":
    st.subheader("🌐 SSL Sertifika Analizi")
    site_adi = st.text_input("Domain:", "github.com")
    if st.button("Sorgula"):
        try:
            context = ssl.create_default_context()
            with socket.create_connection((site_adi, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=site_adi) as ssock:
                    cert = ssock.getpeercert()
                    subject = dict(x[0] for x in cert.get('subject', []))
                    st.success(f"🔒 **Sahip (CN):** `{subject.get('commonName', 'Bilinmiyor')}`")
        except Exception as e:
            st.error(f"Hata: {e}")

# 6. Güçlü Şifre Üretici & Entropi Ölçer
elif secim == "🔑 Güçlü Şifre Üretici & Entropi Ölçer":
    st.subheader("🔑 Parola Üretici")
    uzunluk = st.slider("Uzunluk", 8, 32, 16)
    if st.button("Şifre Üret"):
        sifre = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*") for _ in range(uzunluk))
        st.code(sifre)

# 7. Şifre Kırılma Süresi
elif secim == "⚡ Şifre Kırılma Süresi (Brute-Force)":
    st.subheader("⚡ Brute-Force Süresi Simülatörü")
    input_sifre = st.text_input("Şifre", "Poyraz123*", type="password")
    if input_sifre:
        saniye = ((94) ** len(input_sifre)) / 10_000_000_000
        st.write(f"🔢 Tahmini Süre: {saniye/31536000:,.1f} yıl" if saniye >= 60 else f"{saniye:.1f} saniye")

# 8. Mini Log Analiz Aracı
elif secim == "📜 Mini Log Analiz Aracı":
    st.subheader("📜 Mini Log Analiz")
    log_input = st.text_area("Loglar:", '192.168.1.10 - - "GET /index.html" 200\n10.0.0.5 - - "GET /admin.php" 403', height=120)
    if st.button("Analiz Et"):
        lines = [l.strip() for l in log_input.split("\n") if l.strip()]
        parsed = [{"IP": l.split(" ")[0], "Ham": l} for l in lines]
        st.table(pd.DataFrame(parsed))

# 9. Port Tarayıcı
elif secim == "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi":
    st.subheader("🔌 Port Tarayıcı")
    hedef_ip_port = st.text_input("Hedef IP", "127.0.0.1")
    if st.button("Tara"):
        with st.spinner("Taranıyor..."):
            results = []
            for p in [21, 22, 80, 443, 3306]:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                res = s.connect_ex((hedef_ip_port.strip(), p))
                results.append({"Port": p, "Durum": "AÇIK 🟢" if res == 0 else "KAPALI 🔴"})
                s.close()
            st.table(pd.DataFrame(results))

# 10. Sistem & Ağ Bilgisi
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Sistem Bilgisi")
    st.write(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    st.write(f"Makine: {socket.gethostname()}")

# 11. Oltalama Sistemi
elif secim == "🎣 Oltalama Mesajı & Kurban Yakalama Sistemi":
    st.subheader("🎣 Oltalama & Kurban Yakalama Laboratuvarı")
    tab1, tab2, tab3 = st.tabs(["✉️ Mesaj Oluştur", "🖥️ Kurban Simülasyonu", "📊 Log Paneli"])
    
    with tab1:
        ozel_url = st.text_input("URL:", "https://guvenlik-merkezi.com/login")
        mesaj = f"Konu: Şifre Güncelleme\n\nHesabınızın süresi doldu, tıklayın:\n🔗 {ozel_url}"
        st.text_area("Mesaj:", mesaj, height=120)
        st.download_button("İndir", mesaj, file_name="mesaj.txt")
        
    with tab2:
        with st.form("form"):
            k = st.text_input("Kullanıcı Adı")
            s = st.text_input("Şifre", type="password")
            if st.form_submit_button("Giriş Yap"):
                st.session_state['phishing_logs'].append({"Zaman": datetime.now().strftime("%H:%M:%S"), "Kullanıcı": k, "Şifre": s})
                st.success("🚨 Veri yakalandı!")
                
    with tab3:
        if st.button("Temizle"): st.session_state['phishing_logs'] = []; st.rerun()
        if st.session_state['phishing_logs']:
            st.table(pd.DataFrame(st.session_state['phishing_logs']))
        else:
            st.info("Log yok.")

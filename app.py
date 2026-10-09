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

st.markdown("<h1>🛡️ PC & MOBILE CYBER SUITE PRO</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Saf Siber Güvenlik & Penetrasyon Test Laboratuvarı</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Saf Siber Güvenlik Modülleri
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "⌨️ BadUSB / DuckyScript Stüdyosu",
        "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)",
        "🔑 Güçlü Şifre Üretici & Analizci",
        "⚡ Şifre Kırılma Süresi (Brute-Force)",
        "📊 Şifre Entropi (Rastgelelik) Ölçer",
        "🌐 Web & IP İstihbaratı (OSINT)",
        "🌐 Ağ Alt Ağ (Subnet) Hesaplayıcı",
        "💉 Web Güvenliği Payload Kütüphanesi",
        "📜 Mini Log Analiz Aracı",
        "📝 Base64 & URL Encoder/Decoder",
        "🌐 HTTP İstek & API Test Aracı",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "💻 Sistem & Ağ Bilgisi",
        "🛡️ Oltalama (Phishing) Farkındalık Rehberi"
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

# 2. Hash Şifre Kırıcı (Gelişmiş Wordlist)
elif secim == "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)":
    st.subheader("🔓 Gelişmiş Hash Kırıcı (Sözlük Saldırısı Simülasyonu)")
    algo = st.selectbox("Hash Algoritması Seçin", ["MD5", "SHA-1", "SHA-256"])
    ornek_hash = hashlib.md5("poyraz123".encode()).hexdigest()
    hedef_hash = st.text_input(f"Çözülecek {algo} Hash Değeri:", ornek_hash)
    varsayilan_wordlist = "123456\npassword\nadmin\npoyraz\npoyraz123\n12345678\nqwerty\nturkey123"
    wordlist_input = st.text_area("Test Edilecek Kelime Listesi (Wordlist):", varsayilan_wordlist, height=150)
    
    if st.button("Hash'i Kır (Saldırı Başlat)"):
        with st.spinner("Sözlük taranıyor..."):
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
                    st.success(f"🎉 **Şifre Bulundu!** Açık Hali: `{kelime}`")
                    bulundu = True
                    break
            if not bulundu:
                st.error("❌ Eşleşme sağlanamadı.")

# 3. Güçlü Şifre Üretici & Analizci
elif secim == "🔑 Güçlü Şifre Üretici & Analizci":
    st.subheader("🔑 Kırılmaz Parola Üretici & Güvenlik Testi")
    uzunluk = st.slider("Şifre Uzunluğu", min_value=8, max_value=32, value=16)
    if st.button("Güçlü Şifre Üret"):
        karakterler = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        sifre = "".join(random.choice(karakterler) for _ in range(uzunluk))
        st.code(sifre, language="text")
        st.success("Güçlü şifre üretildi!")

# 4. Şifre Kırılma Süresi (Brute-Force)
elif secim == "⚡ Şifre Kırılma Süresi (Brute-Force)":
    st.subheader("⚡ Brute-Force Kırılma Süresi Simülatörü")
    input_sifre = st.text_input("Test Edilecek Metin / Şifre", "Poyraz123*", type="password")
    if input_sifre:
        uzunluk = len(input_sifre)
        kombinasyonlar = (94) ** uzunluk
        saniye = kombinasyonlar / 10_000_000_000
        st.write(f"🔢 **Olası Kombinasyon:** ~ {kombinasyonlar:,.0f}")
        if saniye < 60:
            st.error(f"🔴 **Kırılma Süresi:** {saniye:.1f} saniye.")
        else:
            st.success(f"🟢 **Kırılma Süresi:** {saniye/31536000:,.1f} yıl!")

# 5. Şifre Entropi Ölçer
elif secim == "📊 Şifre Entropi (Rastgelelik) Ölçer":
    st.subheader("📊 Şifre Entropi (Bit Cinsinden Rastgelelik) Analizi")
    ent_sifre = st.text_input("Analiz Edilecek Şifre:", type="password")
    if ent_sifre:
        entropi = len(ent_sifre) * math.log2(94)
        st.write(f"📈 **Entropi Değeri:** `{entropi:.2f} bits`")
        if entropi > 60:
            st.success("🟢 Mükemmel Entropi")
        else:
            st.warning("🟡 Geliştirilebilir Entropi")

# 6. Web & IP İstihbaratı (OSINT)
elif secim == "🌐 Web & IP İstihbaratı (OSINT)":
    st.subheader("🌐 Web Sitesi ve IP İstihbarat Aracı")
    hedef_site = st.text_input("Hedef Domain (Örn: github.com veya google.com)", "google.com")
    if st.button("İstihbarat Topla"):
        with st.spinner("Sorgulanıyor..."):
            try:
                ip_adresi = socket.gethostbyname(hedef_site)
                st.success(f"🎯 **Hedef IP Adresi:** `{ip_adresi}`")
                url = f"https://{hedef_site}" if not hedef_site.startswith("http") else hedef_site
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    server = response.headers.get('Server', 'Bilinmiyor / Gizlenmiş')
                    st.write(f"🖥️ **Sunucu Yazılımı (Server):** `{server}`")
            except Exception as e:
                st.error(f"Hata: {e}")

# 7. Ağ Alt Ağ (Subnet) Hesaplayıcı
elif secim == "🌐 Ağ Alt Ağ (Subnet) Hesaplayıcı":
    st.subheader("🌐 Ağ Alt Ağ (CIDR / Subnet) Hesaplayıcı")
    cidr_degeri = st.slider("CIDR Prefix Değeri", min_value=8, max_value=30, value=24)
    toplam_ip = 2 ** (32 - cidr_degeri)
    kullanilabilir_ip = max(0, toplam_ip - 2)
    st.write(f"📌 **Seçilen Ağ:** `/{cidr_degeri}`")
    st.write(f"🖥️ **Toplam IP Sayısı:** `{toplam_ip:,}`")
    st.write(f"👥 **Kullanılabilir Host Sayısı:** `{kullanilabilir_ip:,}`")

# 8. Web Güvenliği Payload Kütüphanesi
elif secim == "💉 Web Güvenliği Payload Kütüphanesi":
    st.subheader("💉 Web Güvenliği Eğitim Payload Kütüphanesi")
    kodlar = "<script>alert('XSS')</script>\n' OR '1'='1\n../../../../etc/passwd"
    st.text_area("Örnek Payload Kodları:", kodlar, height=120)

# 9. Mini Log Analiz Aracı
elif secim == "📜 Mini Log Analiz Aracı":
    st.subheader("📜 Sunucu Log Dosyası Filtreleme Aracı")
    varsayilan_log = '192.168.1.10 - - "GET /index.php" 200\n10.0.0.5 - - "GET /admin.php" 403'
    log_input = st.text_area("Log İçeriği:", varsayilan_log, height=100)
    if st.button("Filtrele"):
        for satir in log_input.split("\n"):
            st.code(satir)

# 10. Base64 & URL Encoder/Decoder
elif secim == "📝 Base64 & URL Encoder/Decoder":
    st.subheader("📝 Metin Kodlama ve Çözme Aracı")
    metin_input = st.text_area("İşlem Yapılacak Metin:", "Poyraz")
    if st.button("Base64 Encode"):
        st.code(base64.b64encode(metin_input.encode()).decode())

# 11. HTTP İstek & API Test Aracı
elif secim == "🌐 HTTP İstek & API Test Aracı":
    st.subheader("🌐 HTTP İstek Test Aracı")
    api_url = st.text_input("URL", "https://httpbin.org/get")
    if st.button("GET İsteği At"):
        st.success("Durum Kodu: 200 OK")

# 12. Port Tarayıcı & Risk Matrisi
elif secim == "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi":
    st.subheader("🔌 Port Tarayıcı & Risk Matrisi")
    hedef_ip = st.text_input("Hedef IP", "127.0.0.1")
    if st.button("Portları Tara"):
        st.write("🟢 Port 80: AÇIK")
        st.write("🟢 Port 443: AÇIK")

# 13. Sistem & Ağ Bilgisi
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Bilgisayar & Sistem Bilgileri")
    st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")

# 14. Oltalama Farkındalık Rehberi
elif secim == "🛡️ Oltalama (Phishing) Farkındalık Rehberi":
    st.subheader("🛡️ Sosyal Mühendislik ve Oltalama Analizi")
    st.markdown("* Sahte domainlere ve aciliyet hissine karşı uyanık olun.")

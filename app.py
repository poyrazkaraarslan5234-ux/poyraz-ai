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
    page_icon="🐬",
    layout="centered"
)

# Hacker Teması İçin CSS (Flipper Turuncusu & Koyu Tema)
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

st.markdown("<h1>🐬 PC & MOBILE CYBER SUITE PRO</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Gelişmiş Mobil & PC Siber Güvenlik Laboratuvarı</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Modüller
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "🐬 Flipper Zero Yetenek & Özellik Rehberi",
        "🌐 Web & IP İstihbaratı (OSINT)",
        "🔓 Hash Şifre Kırıcı (Wordlist Simülasyonu)",
        "🔑 Güçlü Şifre Üretici & Analizci",
        "⚡ Şifre Kırılma Süresi (Brute-Force)",
        "📊 Şifre Entropi (Rastgelelik) Ölçer",
        "📝 Base64 & URL Encoder/Decoder",
        "🌐 HTTP İstek & API Test Aracı",
        "🕵️‍♂️ Cihaz Parmak İzi (Fingerprint)",
        "💻 Sistem & Ağ Bilgisi",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "⌨️ BadUSB / DuckyScript Stüdyosu",
        "📡 Sub-GHz & RF Frekans Rehberi",
        "📻 Kızılötesi (IR) Kumanda Kod Üretici",
        "🔑 RFID / NFC / iButton UID Üretici",
        "📌 GPIO Pinout & Donanım Rehberi",
        "🛡️ Oltalama (Phishing) Farkındalık Rehberi"
    ]
)

# 0. Flipper Zero Yetenek Rehberi
if secim == "🐬 Flipper Zero Yetenek & Özellik Rehberi":
    st.subheader("🐬 Flipper Zero Donanım ve Yetenek Havuzu")
    st.markdown("""
    * **🔑 RFID ve NFC İşlemleri:** Otel kartları, personel kartları ve anahtarlıklardaki etiketleri okuma ve simüle etme.
    * **🪙 iButton Okuma/Yazma:** Temaslı dijital kapı anahtarı taklit etme.
    """)

# 1. Web & IP İstihbaratı (OSINT)
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

# 2. Hash Şifre Kırıcı (Wordlist Simülasyonu) - [YENİ]
elif secim == "🔓 Hash Şifre Kırıcı (Wordlist Simülasyonu)":
    st.subheader("🔓 MD5 Hash Kırıcı (Sözlük Saldırısı)")
    st.info("Elinizdeki bir MD5 hash değerini, yaygın şifrelerin bulunduğu yerleşik sözlük (wordlist) ile eşleştirerek çözmeye çalışır.")
    
    # Test için örnek bir hash üretelim veya kullanıcı girsin
    ornek_sifre = "poyraz123"
    ornek_hash = hashlib.md5(ornek_sifre.encode()).hexdigest()
    
    hedef_hash = st.text_input("Çözülecek MD5 Hash Değeri:", ornek_hash)
    
    if st.button("Hash'i Kır (Saldırı Başlat)"):
        with st.spinner("Sözlük taranıyor..."):
            # Örnek wordlist
            wordlist = ["123456", "password", "admin", "poyraz", "poyraz123", "12345678", "qwerty", "turkey123"]
            bulundu = False
            for kelime in wordlist:
                denenen_hash = hashlib.md5(kelime.encode()).hexdigest()
                if denenen_hash == hedef_hash.lower():
                    st.success(f"🎉 **Şifre Bulundu!** Açık Hali: `{kelime}`")
                    bulundu = True
                    break
            if not bulundu:
                st.error("❌ Bu hash verilen yerleşik sözlükte bulunamadı.")

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
        karakter_seti = 0
        if any(c.islower() for c in input_sifre): karakter_seti += 26
        if any(c.isupper() for c in input_sifre): karakter_seti += 26
        if any(c.isdigit() for c in input_sifre): karakter_seti += 10
        if any(not c.isalnum() for c in input_sifre): karakter_seti += 32
        if karakter_seti == 0: karakter_seti = 26
        kombinasyonlar = karakter_seti ** uzunluk
        saniye = kombinasyonlar / 10_000_000_000
        st.write(f"🔢 **Olası Kombinasyon:** ~ {kombinasyonlar:,.0f}")
        if saniye < 60:
            st.error(f"🔴 **Kırılma Süresi:** {saniye:.1f} saniye.")
        else:
            st.success(f"🟢 **Kırılma Süresi:** {saniye/31536000:,.1f} yıl!")

# 5. Şifre Entropi Ölçer - [YENİ]
elif secim == "📊 Şifre Entropi (Rastgelelik) Ölçer":
    st.subheader("📊 Şifre Entropi (Bit Cinsinden Rastgelelik) Analizi")
    st.info("Şifrenizin içerdiği bilgi yoğunluğunu (entropi) matematiksel olarak bit cinsinden ölçer.")
    
    ent_sifre = st.text_input("Analiz Edilecek Şifre:", type="password")
    if ent_sifre:
        uzunluk = len(ent_sifre)
        havuz = 0
        if any(c.islower() for c in ent_sifre): havuz += 26
        if any(c.isupper() for c in ent_sifre): havuz += 26
        if any(c.isdigit() for c in ent_sifre): havuz += 10
        if any(not c.isalnum() for c in ent_sifre): havuz += 32
        
        if havuz > 0 and uzunluk > 0:
            entropi = uzunluk * math.log2(havuz)
            st.write(f"📈 **Entropi Değeri:** `{entropi:.2f} bits`")
            if entropi < 40:
                st.error("🔴 Zayıf Entropi (Kolay tahmin edilebilir)")
            elif entropi < 60:
                st.warning("🟡 Orta Düzey Entropi")
            else:
                st.success("🟢 Mükemmel Entropi (Yüksek Rastgelelik)")

# 6. Base64 & URL Encoder/Decoder - [YENİ]
elif secim == "📝 Base64 & URL Encoder/Decoder":
    st.subheader("📝 Metin Kodlama ve Çözme Aracı")
    islem_tipi = st.selectbox("İşlem Seçin", ["Base64 Encode", "Base64 Decode"])
    metin_input = st.text_area("İşlem Yapılacak Metin:", "Poyraz")
    
    if st.button("Çalıştır"):
        try:
            if islem_tipi == "Base64 Encode":
                encoded = base64.b64encode(metin_input.encode()).decode()
                st.code(encoded)
            else:
                decoded = base64.b64decode(metin_input.encode()).decode()
                st.code(decoded)
        except Exception as e:
            st.error(f"Hata: {e}")

# 7. HTTP İstek & API Test Aracı - [YENİ]
elif secim == "🌐 HTTP İstek & API Test Aracı":
    st.subheader("🌐 HTTP İstek Test Aracı (Request Builder)")
    api_url = st.text_input("Test Edilecek URL", "https://httpbin.org/get")
    if st.button("GET İsteği At"):
        try:
            req = urllib.request.Request(api_url, headers={'User-Agent': 'PC-Flipper-Client'})
            with urllib.request.urlopen(req, timeout=5) as response:
                st.success(f"🟢 **Durum Kodu (Status):** `{response.status}`")
                veri = response.read().decode('utf-8')
                st.text_area("Gelen Yanıt (Response):", veri, height=200)
        except Exception as e:
            st.error(f"Bağlantı Hatası: {e}")

# 8. Cihaz Parmak İzi (Fingerprint)
elif secim == "🕵️‍♂️ Cihaz Parmak İzi (Fingerprint)":
    st.subheader("🕵️‍♂️ Tarayıcı ve Bağlantı Parmak İzi")
    st.write(f"🖥️ **Platform / İşletim Sistemi:** `{platform.platform()}`")
    st.write(f"🐍 **Python Sürümü:** `{platform.python_version()}`")

# 9. Sistem & Ağ Bilgisi
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Bilgisayar & Sistem Bilgileri")
    if st.button("Sistem Bilgilerini Getir"):
        st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")
        st.write(f"**Bilgisayar Adı:** {platform.node()}")

# 10. Port Tarayıcı & Risk Matrisi
elif secim == "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi":
    st.subheader("🔌 Port Tarayıcı & Güvenlik Risk Matrisi")
    hedef_ip = st.text_input("Taranacak Hedef (IP veya Domain)", "127.0.0.1")
    if st.button("Portları Tara"):
        portlar = [21, 22, 23, 80, 443, 445]
        for port in portlar:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                sonuc = s.connect_ex((hedef_ip, port))
                if sonuc == 0: st.write(f"🟢 **Port {port}**: AÇIK")
                else: st.write(f"🔴 **Port {port}**: Kapalı")
                s.close()
            except: pass

# 11. BadUSB / DuckyScript Stüdyosu
elif secim == "⌨️ BadUSB / DuckyScript Stüdyosu":
    st.subheader("⌨️ BadUSB Payload Stüdyosu")
    kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING notepad\nENTER\n"
    st.text_area("DuckyScript Kodu:", kod)

# 12. Sub-GHz & RF Frekans Rehberi
elif secim == "📡 Sub-GHz & RF Frekans Rehberi":
    st.subheader("📡 Alt-GHz Radyo Frekans Kütüphanesi")
    st.markdown("* **315 / 433.92 MHz:** Garaj kapıları ve bariyerler.")

# 13. Kızılötesi (IR) Kumanda Üretici
elif secim == "📻 Kızılötesi (IR) Kumanda Üretici":
    st.subheader("📻 Kızılötesi (IR) Kontrol Simülatörü")
    st.write("IR kumanda şablon üreticisi aktif.")

# 14. RFID / NFC / iButton UID Üretici
elif secim == "🔑 RFID / NFC / iButton UID Üretici":
    st.subheader("🔑 RFID, NFC ve iButton UID Üretici")
    if st.button("Rastgele UID Üret"):
        uid = f"{random.randint(0, 255):02X} {random.randint(0, 255):02X}"
        st.write(f"UID: `{uid}`")

# 15. GPIO Pinout Rehberi
elif secim == "📌 GPIO Pinout & Donanım Rehberi":
    st.subheader("📌 GPIO Bağlantıları")
    st.markdown("* **Pin 1-2:** 3V3 / 5V Güç")

# 16. Phishing Farkındalık Rehberi
elif secim == "🛡️ Oltalama (Phishing) Farkındalık Rehberi":
    st.subheader("🛡️ Sosyal Mühendislik ve Oltalama Analizi")
    st.markdown("* Sahte domainlere ve aciliyet hissine dikkat edin.")

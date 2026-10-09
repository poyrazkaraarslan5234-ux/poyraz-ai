import streamlit as st
import socket
import platform
import subprocess
import hashlib
import base64

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PC-Flipper Ultimate Paneli",
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

st.markdown("<h1>🐬 PC-FLIPPER ULTIMATE PANELİ</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Siber Güvenlik, Keşif ve Araç Merkezi</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü (Flipper Kategorileri)
secim = st.sidebar.selectbox(
    "Flipper Modülleri",
    [
        "💻 Sistem & Donanım Bilgisi",
        "🔌 Gelişmiş Port Tarayıcı",
        "⌨️ BadUSB / Payload Oluşturucu",
        "📶 Kayıtlı Wi-Fi Profilleri",
        "🔐 Kripto & Hash Araçları",
        "📡 Sub-GHz & RFID Frekans Rehberi"
    ]
)

# 1. Sistem Bilgisi
if secim == "💻 Sistem & Donanım Bilgisi":
    st.subheader("💻 Bilgisayar Sistem Bilgileri")
    if st.button("Bilgileri Getir"):
        with st.spinner("Taranıyor..."):
            st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")
            st.write(f"**Bilgisayar Adı:** {platform.node()}")
            st.write(f"**İşlemci:** {platform.processor()}")
            try:
                yerel_ip = socket.gethostbyname(socket.gethostname())
                st.write(f"**Yerel IP:** {yerel_ip}")
            except:
                pass
            st.success("Tamamlandı!")

# 2. Port Tarayıcı
elif secim == "🔌 Gelişmiş Port Tarayıcı":
    st.subheader("🔌 Port Tarayıcı")
    hedef_ip = st.text_input("Taranacak Hedef (IP veya Domain)", "127.0.0.1")
    timeout_suresi = st.slider("Zaman Aşımı (Saniye)", 0.5, 3.0, 1.0)
    
    if st.button("Portları Tara"):
        with st.spinner("Portlar yoklanıyor..."):
            portlar = [21, 22, 23, 80, 443, 445, 3306, 8080, 8443]
            for port in portlar:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(timeout_suresi)
                    sonuc = s.connect_ex((hedef_ip, port))
                    if sonuc == 0:
                        st.write(f"🟢 **Port {port}**: AÇIK")
                    else:
                        st.write(f"🔴 **Port {port}**: Kapalı / Reddedildi")
                    s.close()
                except:
                    pass
            st.success("Tarama bitti.")

# 3. BadUSB / Payload Oluşturucu (Rubber Ducky Tarzı)
elif secim == "⌨️ BadUSB / Payload Oluşturucu":
    st.subheader("⌨️ BadUSB / Keystroke Payload Oluşturucu")
    st.info("Flipper'ın BadUSB özelliğine benzer şekilde, otomatik klavye komutları (DuckyScript) üretebilirsiniz.")
    
    payload_turu = st.selectbox("Payload Senaryosu Seçin", [
        "Not Defteri Aç ve Mesaj Yaz",
        "Komut İstemi (CMD) Aç",
        "IP Adreslerini Dosyaya Kaydet (IpConfig)"
    ])
    
    if payload_turu == "Not Defteri Aç ve Mesaj Yaz":
        kod = """DELAY 1000\nGUI r\nDELAY 200\nSTRING notepad\nENTER\nDELAY 500\nSTRING Merhaba, bu PC-Flipper tarafindan yazildi!\n"""
    elif payload_turu == "Komut İstemi (CMD) Aç":
        kod = """DELAY 1000\nGUI r\nDELAY 200\nSTRING cmd\nENTER\nDELAY 300\nSTRING color 0a && cls\nENTER\n"""
    else:
        kod = """DELAY 1000\nGUI r\nDELAY 200\nSTRING cmd\nENTER\nDELAY 300\nSTRING ipconfig > C:\\ip.txt && notepad C:\\ip.txt\nENTER\n"""
        
    st.text_area("Üretilen DuckyScript Kodu:", kod, height=150)
    st.download_button("Payload Dosyasını İndir (.txt)", kod, file_name="payload.txt")

# 4. Kayıtlı Wi-Fi'ler
elif secim == "📶 Kayıtlı Wi-Fi Profilleri":
    st.subheader("📶 Kayıtlı Wi-Fi Ağ Profilleri")
    st.info("Bilgisayarın hafızasındaki Wi-Fi ağlarını listeler (Lokal çalıştırıldığında tam sonuç verir).")
    if st.button("Wi-Fi Profillerini Listele"):
        with st.spinner("Okunuyor..."):
            try:
                sonuc = subprocess.check_output("netsh wlan show profiles", shell=True, encoding="latin5")
                st.text(sonuc)
            except Exception as e:
                st.error(f"Hata: {e}")

# 5. Kripto & Hash Araçları
elif secim == "🔐 Kripto & Hash Araçları":
    st.subheader("🔐 Şifreleme ve Hash Üretici")
    metin = st.text_input("İşlem Yapılacak Metin:", "Poyraz123")
    
    if metin:
        md5_hash = hashlib.md5(metin.encode()).hexdigest()
        sha256_hash = hashlib.sha256(metin.encode()).hexdigest()
        b64_encode = base64.b64encode(metin.encode()).decode()
        
        st.write(f"**MD5:** `{md5_hash}`")
        st.write(f"**SHA-256:** `{sha256_hash}`")
        st.write(f"**Base64 Şifreli:** `{b64_encode}`")

# 6. Sub-GHz & RFID Frekans Rehberi
elif secim == "📡 Sub-GHz & RFID Frekans Rehberi":
    st.subheader("📡 Popüler Frekanslar ve Kart Türleri Rehberi")
    st.markdown("""
    * **315 MHz / 433.92 MHz:** Araba kumandaları, garaj kapıları, akıllı ev sistemleri.
    * **868 MHz / 915 MHz:** Uzun mesafe IoT sensörleri, endüstriyel kumandalar.
    * **125 kHz (RFID):** Eski tip apartman kapı giriş kartları, personel kartları, hayvançipleri.
    * **13.56 MHz (NFC / RFID):** İstanbulkart, temassız kredi kartları, otobüs biletleri, otel kartları.
    """)
    st.success("Bu rehber Flipper Zero'nun tarama yaptığı ana frekans aralıklarını listeler.")

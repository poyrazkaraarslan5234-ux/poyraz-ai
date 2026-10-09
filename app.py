import streamlit as st
import socket
import platform
import subprocess
import hashlib
import base64
import random

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PC-Flipper Ultimate Suite",
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

st.markdown("<h1>🐬 PC-FLIPPER ULTIMATE SUITE</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Flipper Zero Donanım & Yazılım Özellikleri Simülatörü</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Flipper'ın Tüm Kategorileri
secim = st.sidebar.selectbox(
    "Flipper Modülleri",
    [
        "💻 Sistem & Ağ Bilgisi",
        "🔌 Gelişmiş Port Tarayıcı",
        "⌨️ BadUSB / DuckyScript Stüdyosu",
        "📡 Sub-GHz & RF Frekans Rehberi",
        "📻 Kızılötesi (IR) Kumanda Kod Üretici",
        "🔑 RFID / NFC / iButton UID Üretici",
        "📌 GPIO Pinout & Donanım Rehberi",
        "🔐 Kripto & Hash Araçları"
    ]
)

# 1. Sistem & Ağ Bilgisi
if secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Bilgisayar & Sistem Bilgileri")
    if st.button("Sistem Bilgilerini Getir"):
        with st.spinner("Taranıyor..."):
            st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")
            st.write(f"**Bilgisayar Adı:** {platform.node()}")
            st.write(f"**İşlemci:** {platform.processor()}")
            try:
                yerel_ip = socket.gethostbyname(socket.gethostname())
                st.write(f"**Yerel IP Adresi:** {yerel_ip}")
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

# 3. BadUSB / DuckyScript Stüdyosu
elif secim == "⌨️ BadUSB / DuckyScript Stüdyosu":
    st.subheader("⌨️ BadUSB Payload Stüdyosu")
    st.info("Flipper'ın BadUSB özelliği için otomatik klavye komutları (DuckyScript) oluşturun.")
    
    payload_turu = st.selectbox("Payload Şablonu Seçin", [
        "Not Defteri Aç ve Mesaj Yaz",
        "Komut İstemi (CMD) Renkli Başlat",
        "IP Bilgilerini Dosyaya Kaydet",
        "Arka Planda Web Sitesi Aç"
    ])
    
    if payload_turu == "Not Defteri Aç ve Mesaj Yaz":
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING notepad\nENTER\nDELAY 500\nSTRING Merhaba, bu PC-Flipper tarafindan yazildi!\n"
    elif payload_turu == "Komut İstemi (CMD) Renkli Başlat":
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING cmd\nENTER\nDELAY 300\nSTRING color 0a && cls\nENTER\n"
    elif payload_turu == "IP Bilgilerini Dosyaya Kaydet":
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING cmd\nENTER\nDELAY 300\nSTRING ipconfig > C:\\ip_report.txt && notepad C:\\ip_report.txt\nENTER\n"
    else:
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING powershell Start-Process 'https://github.\nENTER\n"
        
    st.text_area("Üretilen DuckyScript Kodu:", kod, height=150)
    st.download_button("Payload Dosyasını İndir (.txt)", kod, file_name="payload.txt")

# 4. Sub-GHz & RF Frekans Rehberi
elif secim == "📡 Sub-GHz & RF Frekans Rehberi":
    st.subheader("📡 Sub-GHz Radyo Frekans Kütüphanesi")
    st.markdown("""
    * **315 MHz:** Amerikan tipi araç kumandaları ve garaj kapıları.
    * **433.92 MHz:** Avrupa ve Türkiye'deki standart bariyerler, garajlar, ev alarm sistemleri.
    * **868 MHz / 915 MHz:** Uzun menzilli IoT cihazları, akıllı sayaçlar, endüstriyel kumandalar.
    * **300-348 MHz / 387-464 MHz:** Geniş bant serbest telsiz ve kumanda aralığı.
    """)
    st.info("Flipper Zero bu frekanslarda RAW (Ham) sinyal kaydı yapabilir ve sabit kodlu kumandaları taklit edebilir.")

# 5. Kızılötesi (IR) Kumanda Üretici
elif secim == "📻 Kızılötesi (IR) Kumanda Üretici":
    st.subheader("📻 Kızılötesi (Infrared) Evrensel Kumanda Simülatörü")
    st.info("Televizyon, klima ve ses sistemleri için Flipper uyumlu IR sinyal veri yapıları.")
    
    cihaz = st.selectbox("Cihaz Türü Seçin", ["Televizyon (TV)", "Klima (AC)", "Ses Sistemi (Audio)"])
    marka = st.text_input("Marka Adı (Örn: Samsung, Sony, LG)", "Samsung")
    
    if st.button("IR Kodunu Üret"):
        ir_ornek = f"#
\n# Flipper Zero IR File
\n# Brand: {marka} - Device: {cihaz}
\n#
\nname: {marka}_Power_Toggle
\ntype: parsed
\nprotocol: NEC
\naddress: 04 00 00 00
\ncommand: 07 00 00 00"
        st.code(ir_ornek, language="text")
        st.success("IR komut dosyası oluşturuldu! Flipper IR klasörüne atarak kullanabilirsiniz.")

# 6. RFID / NFC / iButton UID Üretici
elif secim == "🔑 RFID / NFC / iButton UID Üretici":
    st.subheader("🔑 Kart UID (Kimlik Numarası) Üretici")
    st.info("Test amaçlı rastgele kart UID'leri oluşturun (EM4100, Mifare Classic, iButton).")
    
    kart_turu = st.selectbox("Kart Tipi", ["125 kHz RFID (EM4100)", "13.56 MHz NFC (Mifare Classic 4-byte)", "iButton (Dallas DS1990)"])
    
    if st.button("Rastgele UID Üret"):
        if kart_turu == "125 kHz RFID (EM4100)":
            uid = f"{random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X}"
        elif kart_turu == "13.56 MHz NFC (Mifare Classic 4-byte)":
            uid = f"{random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X}"
        else:
            uid = f"01 {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} FF"
            
        st.write(f"**Üretilen UID:** `{uid}`")
        st.success("Test UID başarıyla oluşturuldu!")

# 7. GPIO Pinout & Donanım Rehberi
elif secim == "📌 GPIO Pinout & Donanım Rehberi":
    st.subheader("📌 Flipper Zero 18-Pin GPIO Pinout Şeması")
    st.markdown("""
    Flipper Zero'nun üst kısmındaki pinlerin görevleri:
    * **Pin 1 (3V3):** 3.3 Volt Güç Çıkışı
    * **Pin 2 (5V):** 5 Volt Güç Çıkışı (USB üzerinden beslenir)
    * **Pin 3 & 4 (GND):** Topraklama (Ground)
    * **Pin 5 (A7 / GPIO):** Genel amaçlı analog/dijital pin
    * **Pin 6 (A6 / GPIO):** Genel amaçlı pin
    * **Pin 7 (A4 / TX):** UART Veri İletimi
    * **Pin 8 (A3 / RX):** UART Veri Alımı
    * **Pin 9 (PA14 / SWCLK):** Debug Saat Pini
    * **Pin 10 (PA13 / SWDIO):** Debug Veri Pini
    """)
    st.warning("GPIO ile çalışırken harici sensörlerin voltaj değerlerine (3.3V / 5V) dikkat edin!")

# 8. Kripto & Hash Araçları
elif secim == "🔐 Kripto & Hash Araçları":
    st.subheader("🔐 Şifreleme, Hash ve Encoding Araçları")
    metin = st.text_input("Dönüştürülecek Metin:", "Poyraz123")
    
    if metin:
        md5_hash = hashlib.md5(metin.encode()).hexdigest()
        sha256_hash = hashlib.sha256(metin.encode()).hexdigest()
        b64_encode = base64.b64encode(metin.encode()).decode()
        
        st.write(f"**MD5 Hash:** `{md5_hash}`")
        st.write(f"**SHA-256 Hash:** `{sha256_hash}`")
        st.write(f"**Base64 Encode:** `{b64_encode}`")

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
st.write("<p style='text-align: center; color: #888;'>Flipper Zero Donanım & Yazılım Özellikleri Merkezi</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Flipper'ın Tüm Kategorileri ve Yeni Özellikler
secim = st.sidebar.selectbox(
    "Flipper Modülleri",
    [
        "🐬 Flipper Zero Yetenek & Özellik Rehberi",
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

# 0. Flipper Zero Yetenek & Özellik Rehberi (Yeni Eklenen Detaylı Modül)
if secim == "🐬 Flipper Zero Yetenek & Özellik Rehberi":
    st.subheader("🐬 Flipper Zero Donanım ve Yetenek Havuzu")
    st.info("Flipper Zero'nun fiziksel olarak barındırdığı ve bu panelde simüle ettiğimiz tüm ana özellikleri:")
    
    st.markdown("""
    * **🔑 RFID ve NFC İşlemleri:** Otel kartları, personel kartları ve çeşitli anahtarlıklardaki RFID ile NFC etiketlerini okuyabilir, kopyalayabilir ve simüle edebilir.
    * **📻 Kızılötesi (IR) Kontrol:** Televizyon, klima ve ses sistemleri gibi kızılötesi kumandaya sahip cihazları kontrol edebilir veya mevcut kumandaların sinyal verip vermediğini test edebilir.
    * **📡 Alt-GHz Radyo Frekansları:** Garaj kapıları, bariyerler, uzaktan kumandalı anahtarlar ve panjur sistemleri gibi radyo frekansı kullanan cihazların sinyallerini yakalayıp analiz edebilir.
    * **⌨️ BadUSB / Komut Otomasyonu:** Bilgisayarlara USB üzerinden bağlandığında bir klavye (HID - İnsan Arayüz Cihazı) gibi davranarak DuckyScript dilinde yazılmış otomatik komut dosyalarını çalıştırabilir.
    * **🪙 iButton Okuma ve Yazma:** Eski tip temaslı dijital kapı anahtarlarını ve iButton etiketlerini okuyup taklit edebilir.
    * **📌 GPIO Bağlantıları:** Üzerindeki GPIO pinleri sayesinde harici modüllere, sensörlere veya devre kartlarına bağlanarak sinyal jeneratörü veya donanım test aracı olarak kullanılabilir.
    * **🐬 Sanal Evcil Hayvan:** Ekranındaki piksel sanatıyla yapılmış yunus karakteri, cihazla etkileşime geçtikçe seviye atlayan bir sanal evcil hayvan oyun mekaniği sunar.
    """)
    st.success("Bu panel, Flipper Zero'nun dijital ve yazılımsal gücünü bilgisayarınıza ve telefonunuza taşır!")

# 1. Sistem & Ağ Bilgisi
elif secim == "💻 Sistem & Ağ Bilgisi":
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
    st.subheader("⌨️ BadUSB Payload Stüdyosu (HID Otomasyonu)")
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
        kod = "DELAY 1000\nGUI r\nDELAY 200\nSTRING powershell Start-Process 'https://github.com'\nENTER\n"
        
    st.text_area("Üretilen DuckyScript Kodu:", kod, height=150)
    st.download_button("Payload Dosyasını İndir (.txt)", kod, file_name="payload.txt")

# 4. Sub-GHz & RF Frekans Rehberi
elif secim == "📡 Sub-GHz & RF Frekans Rehberi":
    st.subheader("📡 Alt-GHz Radyo Frekans Kütüphanesi")
    st.markdown("""
    * **Garaj Kapıları & Bariyerler (315 MHz / 433.92 MHz):** Türkiye ve dünyadaki standart bariyerlerin ve uzaktan kumandalı kapıların sinyal aralığı.
    * **Uzaktan Kumandalı Anahtarlar & Panjur Sistemleri:** Sabit kodlu veya rolling-code (değişen kodlu) RF sinyalleri.
    * **868 MHz / 915 MHz:** Uzun menzilli IoT cihazları, akıllı sayaçlar, endüstriyel alarmlar.
    """)
    st.info("Flipper Zero bu frekanslarda RAW (Ham) sinyal kaydı yapabilir ve analiz edebilir.")

# 5. Kızılötesi (IR) Kumanda Üretici
elif secim == "📻 Kızılötesi (IR) Kumanda Üretici":
    st.subheader("📻 Kızılötesi (IR) Kontrol Simülatörü")
    st.info("Televizyon, klima ve ses sistemleri için kızılötesi kumanda sinyal yapıları.")
    
    cihaz = st.selectbox("Cihaz Türü Seçin", ["Televizyon (TV)", "Klima (AC)", "Ses Sistemi (Audio)"])
    marka = st.text_input("Marka Adı (Örn: Samsung, Sony, LG)", "Samsung")
    
    if st.button("IR Kodunu Üret"):
        ir_ornek = f"""#
# Flipper Zero IR File
# Brand: {marka} - Device: {cihaz}
#
name: {marka}_Power_Toggle
type: parsed
protocol: NEC
address: 04 00 00 00
command: 07 00 00 00"""
        st.code(ir_ornek, language="text")
        st.success("IR komut dosyası oluşturuldu!")

# 6. RFID / NFC / iButton UID Üretici
elif secim == "🔑 RFID / NFC / iButton UID Üretici":
    st.subheader("🔑 RFID, NFC ve iButton UID Üretici")
    st.info("Otel kartları, personel kartları ve iButton anahtarlar için test UID'leri oluşturun.")
    
    kart_turu = st.selectbox("Etiket Tipi", ["RFID (EM4100 125 kHz)", "NFC (Mifare Classic 13.56 MHz)", "iButton (Dallas DS1990)"])
    
    if st.button("Rastgele UID Üret"):
        if "RFID" in kart_turu or "NFC" in kart_turu:
            uid = f"{random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X}"
        else:
            uid = f"01 {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} FF"
            
        st.write(f"**Üretilen Kimlik (UID):** `{uid}`")
        st.success("Test UID başarıyla üretildi!")

# 7. GPIO Pinout & Donanım Rehberi
elif secim == "📌 GPIO Pinout & Donanım Rehberi":
    st.subheader("📌 GPIO Bağlantıları ve Donanım Şeması")
    st.markdown("""
    Flipper Zero üzerindeki GPIO pinleri ile harici modüller ve sensörler arası bağlantı rehberi:
    * **Pin 1 (3V3) & Pin 2 (5V):** Güç Çıkışları
    * **Pin 3 & 4 (GND):** Topraklama (Ground)
    * **Pin 5 & 6 (A7 / A6):** Genel Amaçlı Analog/Dijital Pinler
    * **Pin 7 & 8 (TX / RX):** UART Seri Haberleşme Pinleri
    * **Pin 9 & 10 (SWCLK / SWDIO):** Debug ve Donanım Test Pinleri
    """)
    st.warning("GPIO üzerinden harici devre kartları ve sensörlerle çalışırken voltaj sınırlarına dikkat edin!")

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

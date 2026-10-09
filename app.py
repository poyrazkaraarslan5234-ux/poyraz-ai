import streamlit as st
import socket
import platform
import subprocess
import hashlib
import base64
import random
import urllib.request
import json

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PC & Mobile Cyber Suite",
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

st.markdown("<h1>🐬 PC & MOBILE CYBER SUITE</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Mobil ve PC Uyumlu Siber Güvenlik & Keşif Merkezi</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Modüller
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "🐬 Flipper Zero Yetenek & Özellik Rehberi",
        "🌐 Web & IP İstihbaratı (OSINT)",
        "🔑 Güçlü Şifre Üretici & Analizci",
        "💻 Sistem & Ağ Bilgisi",
        "🔌 Gelişmiş Port Tarayıcı",
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
    * **📻 Kızılötesi (IR) Kontrol:** TV, klima ve ses sistemleri kumanda testleri ve sinyal kopyalama.
    * **📡 Alt-GHz Radyo Frekansları:** Garaj kapıları, bariyerler ve panjur sistemlerinin RF sinyallerini analiz etme.
    * **⌨️ BadUSB / Komut Otomasyonu:** HID klavye simülasyonu ile DuckyScript otomasyonları.
    * **🪙 iButton Okuma/Yazma:** Temaslı dijital kapı anahtarı taklit etme.
    * **📌 GPIO Bağlantıları:** Harici sensörler ve devre kartları için sinyal jeneratörü.
    * **🐬 Sanal Evcil Hayvan:** Yunus karakteri ile seviye atlama mekaniği.
    """)

# 1. Web & IP İstihbaratı (OSINT) - Hem telefondan hem PC'den çalışır
elif secim == "🌐 Web & IP İstihbaratı (OSINT)":
    st.subheader("🌐 Web Sitesi ve IP İstihbarat Aracı")
    st.info("Telefondan veya bilgisayardan herhangi bir domainin (web sitesinin) IP adresini ve sunucu bilgilerini sorgulayın.")
    
    hedef_site = st.text_input("Hedef Domain (Örn: github.com veya google.com)", "google.com")
    
    if st.button("İstihbarat Topla"):
        with st.spinner("Sorgulanıyor..."):
            try:
                ip_adresi = socket.gethostbyname(hedef_site)
                st.success(f"🎯 **Hedef IP Adresi:** `{ip_adresi}`")
                
                # HTTP Header Bilgilerini Çekme Denemesi
                url = f"https://{hedef_site}" if not hedef_site.startswith("http") else hedef_site
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    server = response.headers.get('Server', 'Bilinmiyor / Gizlenmiş')
                    content_type = response.headers.get('Content-Type', 'Bilinmiyor')
                    st.write(f"🖥️ **Sunucu Yazılımı (Server):** `{server}`")
                    st.write(f"📄 **İçerik Tipi:** `{content_type}`")
            except Exception as e:
                st.error(f"Sorgulama sırasında hata oluştu: {e}")

# 2. Güçlü Şifre Üretici & Analizci
elif secim == "🔑 Güçlü Şifre Üretici & Analizci":
    st.subheader("🔑 Kırılmaz Parola Üretici & Güvenlik Testi")
    st.info("Hesaplarınız için özel kriptografik şifreler üretin ve mevcut şifrenizin gücünü test edin.")
    
    uzunluk = st.slider("Şifre Uzunluğu", min_value=8, max_value=32, value=16)
    
    if st.button("Güçlü Şifre Üret"):
        karakterler = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        sifre = "".join(random.choice(karakterler) for _ in range(uzunluk))
        st.code(sifre, language="text")
        st.success("Bu şifreyi kırmak yüzyıllar sürer kanki!")
        
    st.markdown("---")
    test_sifre = st.text_input("Mevcut Şifreni Test Et:", type="password")
    if test_sifre:
        puan = len(test_sifre)
        if puan < 6:
            st.error("🔴 Zayıf Şifre! Hemen değiştirmelisin.")
        elif puan < 12:
            st.warning("🟡 Orta Güçte Şifre. Özel karakter ekleyebilirsin.")
        else:
            st.success("🟢 Çok Güçlü Şifre!")

# 3. Sistem & Ağ Bilgisi
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

# 4. Port Tarayıcı
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

# 5. BadUSB / DuckyScript Stüdyosu
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

# 6. Sub-GHz & RF Frekans Rehberi
elif secim == "📡 Sub-GHz & RF Frekans Rehberi":
    st.subheader("📡 Alt-GHz Radyo Frekans Kütüphanesi")
    st.markdown("""
    * **Garaj Kapıları & Bariyerler (315 MHz / 433.92 MHz):** Standart bariyer ve kumanda aralığı.
    * **Uzaktan Kumandalı Anahtarlar & Panjur Sistemleri:** Sabit kodlu ve rolling-code RF sinyalleri.
    * **868 MHz / 915 MHz:** Uzun menzilli IoT cihazları ve endüstriyel alarmlar.
    """)

# 7. Kızılötesi (IR) Kumanda Üretici
elif secim == "📻 Kızılötesi (IR) Kumanda Üretici":
    st.subheader("📻 Kızılötesi (IR) Kontrol Simülatörü")
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

# 8. RFID / NFC / iButton UID Üretici
elif secim == "🔑 RFID / NFC / iButton UID Üretici":
    st.subheader("🔑 RFID, NFC ve iButton UID Üretici")
    kart_turu = st.selectbox("Etiket Tipi", ["RFID (EM4100 125 kHz)", "NFC (Mifare Classic 13.56 MHz)", "iButton (Dallas DS1990)"])
    
    if st.button("Rastgele UID Üret"):
        if "RFID" in kart_turu or "NFC" in kart_turu:
            uid = f"{random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X}"
        else:
            uid = f"01 {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} {random.randint(0, 255):02X} FF"
        st.write(f"**Üretilen Kimlik (UID):** `{uid}`")
        st.success("Test UID başarıyla üretildi!")

# 9. GPIO Pinout Rehberi
elif secim == "📌 GPIO Pinout & Donanım Rehberi":
    st.subheader("📌 GPIO Bağlantıları ve Donanım Şeması")
    st.markdown("""
    * **Pin 1 & 2 (3V3 / 5V):** Güç Çıkışları
    * **Pin 3 & 4 (GND):** Topraklama
    * **Pin 5 & 6 (A7 / A6):** Analog/Dijital Pinler
    * **Pin 7 & 8 (TX / RX):** UART Seri Haberleşme
    """)

# 10. Phishing Farkındalık Rehberi
elif secim == "🛡️ Oltalama (Phishing) Farkındalık Rehberi":
    st.subheader("🛡️ Sosyal Mühendislik ve Oltalama Analizi")
    st.markdown("""
    Siber güvenlikte en yaygın saldırı türü olan Phishing (Oltalama) tekniklerine karşı bilmeniz gerekenler:
    * **Sahte Domainler:** `g00gle.com` veya `faceb0ok.com` gibi benzer yazılımlı alan adlarına dikkat edin.
    * **Aciliyet Hissi:** *"Hesabınız kapatılacak, hemen tıklayın!"* tarzı psikolojik baskılara karşı uyanık olun.
    * **İki Aşamalı Doğrulama (2FA):** Tüm hesaplarınızda SMS veya Authenticator uygulamalarıyla 2FA kullanın.
    """)
    st.success("Bilinçli olmak en güçlü sızma testi savunmasıdır!")

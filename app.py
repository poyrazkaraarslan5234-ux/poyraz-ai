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
        "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)",
        "👤 Hesap / Giriş Şifresi Brute-Force",
        "🔑 Güçlü Şifre Üretici & Analizci",
        "⚡ Şifre Kırılma Süresi (Brute-Force)",
        "📊 Şifre Entropi (Rastgelelik) Ölçer",
        "📝 Base64 & URL Encoder/Decoder",
        "🌐 HTTP İstek & API Test Aracı",
        "💻 Sistem & Ağ Bilgisi",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "⌨️ BadUSB / DuckyScript Stüdyosu",
        "📻 Kızılötesi (IR) Kumanda Kod Üretici",
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

# 2. Hash Şifre Kırıcı (Gelişmiş Wordlist)
elif secim == "🔓 Hash Şifre Kırıcı (Gelişmiş Wordlist)":
    st.subheader("🔓 Gelişmiş Hash Kırıcı (Sözlük Saldırısı)")
    algo = st.selectbox("Hash Algoritması Seçin", ["MD5", "SHA-1", "SHA-256"])
    
    ornek_sifre = "poyraz123"
    if algo == "MD5":
        ornek_hash = hashlib.md5(ornek_sifre.encode()).hexdigest()
    elif algo == "SHA-1":
        ornek_hash = hashlib.sha1(ornek_sifre.encode()).hexdigest()
    else:
        ornek_hash = hashlib.sha256(ornek_sifre.encode()).hexdigest()
        
    hedef_hash = st.text_input(f"Çözülecek {algo} Hash Değeri:", ornek_hash)
    varsayilan_wordlist = "123456\npassword\nadmin\npoyraz\npoyraz123\n12345678\nqwerty\nturkey123\nankara52"
    wordlist_input = st.text_area("Test Edilecek Kelime Listesi (Wordlist):", varsayilan_wordlist, height=150)
    
    if st.button("Hash'i Kır (Saldırı Başlat)"):
        with st.spinner("Sözlük taranıyor..."):
            wordlist = [w.strip() for w in wordlist_input.split("\n") if w.strip()]
            bulundu = False
            for kelime in wordlist:
                if algo == "MD5":
                    denenen_hash = hashlib.md5(kelime.encode()).hexdigest()
                elif algo == "SHA-1":
                    denenen_hash = hashlib.sha1(kelime.encode()).hexdigest()
                else:
                    denenen_hash = hashlib.sha256(kelime.encode()).hexdigest()
                    
                if denenen_hash == hedef_hash.strip().lower():
                    st.success(f"🎉 **Şifre Başarıyla Bulundu!** Açık Hali: `{kelime}`")
                    bulundu = True
                    break
            if not bulundu:
                st.error("❌ Eşleşme sağlanamadı!")

# 3. Hesap / Giriş Şifresi Brute-Force Simülatörü - [YENİ]
elif secim == "👤 Hesap / Giriş Şifresi Brute-Force":
    st.subheader("👤 Veritabanı / Hesap Şifresi Brute-Force Simülatörü")
    st.info("Sistemde kayıtlı bir kullanıcı hesabının (Örn: admin veya poyraz) şifresini sözlük kullanarak test eden simülasyon modülü.")
    
    hedef_kullanici = st.text_input("Hedef Kullanıcı Adı", "admin")
    # Gizli gerçek şifrenin hash'i (Örn: şifre "sifre123" olsun)
    gercek_sifre = "sifre123"
    hedef_kullanici_hash = hashlib.md5(gercek_sifre.encode()).hexdigest()
    
    st.write(f"🔒 **Hedef Hesap:** `{hedef_kullanici}` (Arka planda gizli şifre ile test ediliyor)")
    
    hesap_wordlist = st.text_area("Denenecek Şifre Listesi (Wordlist)", "123456\nadmin123\npassword\nsifre123\npoyraz2026\nroot", height=150)
    
    if st.button("Hesap Şifresini Kır (Brute-Force Başlat)"):
        with st.spinner("Hesap şifresi taranıyor..."):
            liste = [s.strip() for s in hesap_wordlist.split("\n") if s.strip()]
            kirildi = False
            
            for deneme in liste:
                deneme_hash = hashlib.md5(deneme.encode()).hexdigest()
                if deneme_hash == hedef_kullanici_hash:
                    st.success(f"🔓 **Hesap Ele Geçirildi!** Kullanıcı: `{hedef_kullanici}` | Doğru Şifre: `{deneme}`")
                    kirildi = True
                    break
                    
            if not kirildi:
                st.error("❌ Tüm şifreler denendi ancak hesap şifresi listede bulunamadı!")

# 4. Güçlü Şifre Üretici & Analizci
elif secim == "🔑 Güçlü Şifre Üretici & Analizci":
    st.subheader("🔑 Kırılmaz Parola Üretici & Güvenlik Testi")
    uzunluk = st.slider("Şifre Uzunluğu", min_value=8, max_value=32, value=16)
    if st.button("Güçlü Şifre Üret"):
        karakterler = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+"
        sifre = "".join(random.choice(karakterler) for _ in range(uzunluk))
        st.code(sifre, language="text")
        st.success("Güçlü şifre üretildi!")

# 5. Şifre Kırılma Süresi (Brute-Force)
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

# 6. Şifre Entropi Ölçer
elif secim == "📊 Şifre Entropi (Rastgelelik) Ölçer":
    st.subheader("📊 Şifre Entropi (Bit Cinsinden Rastgelelik) Analizi")
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
                st.error("🔴 Zayıf Entropi")
            elif entropi < 60:
                st.warning("🟡 Orta Düzey Entropi")
            else:
                st.success("🟢 Mükemmel Entropi")

# 7. Base64 & URL Encoder/Decoder
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

# 8. HTTP İstek & API Test Aracı
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

# 12. Kızılötesi (IR) Kumanda Üretici
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

# 13. Phishing Farkındalık Rehberi
elif secim == "🛡️ Oltalama (Phishing) Farkındalık Rehberi":
    st.subheader("🛡️ Sosyal Mühendislik ve Oltalama Analizi")
    st.markdown("""
    * **Sahte Domainler:** `g00gle.com` benzeri alan adlarına dikkat edin.
    * **Aciliyet Hissi:** Psikolojik baskı içeren mesajlara karşı uyanık olun.
    * **2FA:** Tüm hesaplarınızda iki aşamalı doğrulama kullanın.
    """)

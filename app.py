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

# Sadeleştirilmiş ve Güçlendirilmiş Modül Listesi
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
        "🔑 Güçlü Şifre Üretici & Entropi Ölçer",
        "⚡ Şifre Kırılma Süresi (Brute-Force)",
        "🌐 Ağ Alt Ağ (Subnet) Hesaplayıcı",
        "📜 Mini Log Analiz Aracı",
        "📝 Base64 & URL Encoder/Decoder",
        "🌐 HTTP İstek & API Test Aracı",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "💻 Sistem & Ağ Bilgisi",
        "🎣 Eğitim Amaçlı Oltalama Şablon Üreticisi"
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
elif secim == "📍 IP Adresi Bulma & Detaylı Sorgulama":
    st.subheader("📍 IP Adresi Bulma ve Detaylı Konum/ISP Analizi")
    st.info("Bu modül dış (public) IP adresinizi otomatik bulur ve istediğiniz IP'yi sorgulamanızı sağlar.")
    
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
    st.write("### 🔍 Harici IP Adresi Sorgulama")
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
                        st.write(f"🏙️ **Şehir / Bölge:** {veri.get('city')} / {veri.get('regionName')}")
                        st.write(f"🏢 **İnternet Servis Sağlayıcı (ISP):** {veri.get('isp')}")
                        st.write(f"📡 **Organizasyon / AS:** {veri.get('org')} ({veri.get('as')})")
                    else:
                        st.error("❌ Geçersiz IP adresi veya sorgu başarısız oldu!")
            except Exception as e:
                st.error(f"Bağlantı Hatası: {e}")

# 3. Hash Şifre Kırıcı (Gelişmiş Wordlist)
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

# 4. Hash Üretici & Analizcisi
elif secim == "🔑 Hash Üretici & Analizcisi":
    st.subheader("🔑 Kriptografik Hash Üretim & Analiz Aracı")
    duz_metin = st.text_input("Hash'lenecek Metin / Şifre:", "poyraz123")
    if st.button("Hash Üret"):
        st.write(f"📌 **MD5:** `{hashlib.md5(duz_metin.encode()).hexdigest()}`")
        st.write(f"📌 **SHA-1:** `{hashlib.sha1(duz_metin.encode()).hexdigest()}`")
        st.write(f"📌 **SHA-256:** `{hashlib.sha256(duz_metin.encode()).hexdigest()}`")
    
    st.markdown("---")
    girilen_hash = st.text_input("Analiz Edilecek Hash Değeri:")
    if st.button("Hash Türünü Analiz Et"):
        uzunluk = len(girilen_hash.strip())
        st.write(f"📏 **Karakter Uzunluğu:** `{uzunluk}`")
        if uzunluk == 32:
            st.success("🟢 Muhtemel Tür: **MD5** veya **NTLM**")
        elif uzunluk == 40:
            st.success("🟢 Muhtemel Tür: **SHA-1**")
        elif uzunluk == 64:
            st.success("🟢 Muhtemel Tür: **SHA-256**")
        else:
            st.warning("🟡 Standart formatlarla eşleşmedi.")

# 5. JWT Çözümleyici
elif secim == "🔒 JWT (JSON Web Token) Çözümleyici":
    st.subheader("🔒 JWT Token İnceleme ve Çözümleme Aracı")
    jwt_input = st.text_area("JWT Token Değerini Yapıştırın:", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IlBveXJheiIsImFkbWluIjp0cnVlfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c")
    if st.button("JWT Çözümle"):
        try:
            parcalar = jwt_input.split('.')
            if len(parcalar) >= 2:
                hp = parcalar[0] + '=' * (-len(parcalar[0]) % 4)
                hd = base64.urlsafe_b64decode(hp).decode('utf-8')
                pp = parcalar[1] + '=' * (-len(parcalar[1]) % 4)
                pd = base64.urlsafe_b64decode(pp).decode('utf-8')
                st.subheader("📋 Header:")
                st.json(json.loads(hd))
                st.subheader("📦 Payload:")
                st.json(json.loads(pd))
                st.success("Çözümlendi!")
            else:
                st.error("Hatalı JWT formatı.")
        except Exception as e:
            st.error(f"Hata: {e}")

# 6. SSL / TLS Sertifika Denetçisi
elif secim == "🌐 SSL / TLS Sertifika Denetçisi":
    st.subheader("🌐 Web Sitesi SSL Sertifika Güvenlik Analizi")
    site_adi = st.text_input("Hedef Alan Adı (Örn: github.com)", "github.com")
    if st.button("Sertifikayı Sorgula"):
        with st.spinner("İnceleniyor..."):
            try:
                context = ssl.create_default_context()
                with socket.create_connection((site_adi, 443), timeout=5) as sock:
                    with context.wrap_socket(sock, server_hostname=site_adi) as ssock:
                        cert = ssock.getpeercert()
                        subject = dict(x[0] for x in cert.get('subject', []))
                        issuer = dict(x[0] for x in cert.get('issuer', []))
                        st.success(f"🔒 **Sertifika Sahibi (CN):** `{subject.get('commonName', 'Bilinmiyor')}`")
                        st.info(f"🏛️ **Veren Otorite:** `{issuer.get('organizationName', 'Bilinmiyor')}`")
            except Exception as e:
                st.error(f"Hata: {e}")

# 7. HTTP Güvenlik Başlıkları Denetçisi
elif secim == "🛡️ HTTP Güvenlik Başlıkları (Security Headers)":
    st.subheader("🛡️ Web Sitesi Güvenlik Başlıkları Denetçisi")
    hedef_url = st.text_input("Test Edilecek URL", "https://github.com")
    if st.button("Başlıkları Tara"):
        with st.spinner("Taranıyor..."):
            try:
                req = urllib.request.Request(hedef_url, headers={'User-Agent': 'CyberSuite-Scanner'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    headers = response.headers
                    for b in ['Content-Security-Policy', 'Strict-Transport-Security', 'X-Frame-Options']:
                        if b in headers:
                            st.success(f"🟢 **{b}:** `{headers.get(b)}`")
                        else:
                            st.warning(f"🔴 **{b}:** Bulunamadı")
            except Exception as e:
                st.error(f"Hata: {e}")

# 8. Güçlü Şifre Üretici & Entropi Ölçer
elif secim == "🔑 Güçlü Şifre Üretici & Entropi Ölçer":
    st.subheader("🔑 Parola Üretici & Entropi Analizi")
    uzunluk = st.slider("Şifre Uzunluğu", 8, 32, 16)
    if st.button("Güçlü Şifre Üret"):
        sifre = "".join(random.choice("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+") for _ in range(uzunluk))
        st.code(sifre)
    
    st.markdown("---")
    ent_sifre = st.text_input("Test Edilecek Şifre Entropisi:", type="password")
    if ent_sifre:
        entropi = len(ent_sifre) * math.log2(94)
        st.write(f"📈 **Entropi Değeri:** `{entropi:.2f} bits`")

# 9. Şifre Kırılma Süresi (Brute-Force)
elif secim == "⚡ Şifre Kırılma Süresi (Brute-Force)":
    st.subheader("⚡ Brute-Force Kırılma Süresi Simülatörü")
    input_sifre = st.text_input("Test Şifresi", "Poyraz123*", type="password")
    if input_sifre:
        saniye = ((94) ** len(input_sifre)) / 10_000_000_000
        st.write(f"🔢 Tahmini Kırılma Süresi: {saniye/31536000:,.1f} yıl" if saniye >= 60 else f"{saniye:.1f} saniye")

# 10. Ağ Alt Ağ (Subnet) Hesaplayıcı
elif secim == "🌐 Ağ Alt Ağ (Subnet) Hesaplayıcı":
    st.subheader("🌐 Subnet Hesaplayıcı")
    cidr = st.slider("CIDR Maskesi", 8, 30, 24)
    st.write(f"Toplam IP Adresi Sayısı: `{2**(32-cidr):,}`")

# 11. Mini Log Analiz Aracı
elif secim == "📜 Mini Log Analiz Aracı":
    st.subheader("📜 Mini Web Log Analiz Aracı")
    sample_log = '192.168.1.10 - - [30/Oct/2026:12:00:00 +0300] "GET /index.html HTTP/1.1" 200 1024\n10.0.0.5 - - [30/Oct/2026:12:01:00 +0300] "GET /admin.php HTTP/1.1" 403 512'
    log_input = st.text_area("Log İçeriği:", sample_log, height=150)
    if st.button("Logları Analiz Et"):
        lines = [l.strip() for l in log_input.split("\n") if l.strip()]
        st.write(f"📊 Toplam Log Satırı: **{len(lines)}**")
        parsed = []
        for line in lines:
            parts = line.split(" ")
            ip = parts[0] if len(parts) > 0 else "Bilinmiyor"
            status = "-"
            for p in parts:
                if p.isdigit() and len(p) == 3:
                    status = p
                    break
            parsed.append({"IP Adresi": ip, "Durum Kodu": status, "Ham Satır": line})
        st.table(pd.DataFrame(parsed))

# 12. Base64 & URL Encoder/Decoder
elif secim == "📝 Base64 & URL Encoder/Decoder":
    st.subheader("📝 Base64 Çevirici")
    m = st.text_area("Metin:", "Poyraz")
    if st.button("Base64 Encode Et"):
        st.code(base64.b64encode(m.encode()).decode())

# 13. HTTP İstek & API Test Aracı
elif secim == "🌐 HTTP İstek & API Test Aracı":
    st.subheader("🌐 HTTP İstek & API Test Aracı")
    api_url = st.text_input("Test URL", "https://httpbin.org/get")
    if st.button("İstek Gönder"):
        with st.spinner("İstek yapılıyor..."):
            try:
                req = urllib.request.Request(api_url, headers={'User-Agent': 'CyberSuite-Tester'})
                with urllib.request.urlopen(req, timeout=5) as resp:
                    code = resp.getcode()
                    headers = dict(resp.headers.items())
                    body = resp.read().decode('utf-8', errors='ignore')
                    st.success(f"HTTP Durum Kodu: `{code}`")
                    st.subheader("📋 Yanıt Başlıkları:")
                    st.json(headers)
                    st.subheader("📦 Yanıt Gövdesi (Body):")
                    st.code(body[:1000])
            except Exception as e:
                st.error(f"İstek başarısız: {e}")

# 14. Port Tarayıcı & Risk Matrisi
elif secim == "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi":
    st.subheader("🔌 Gelişmiş Port Tarayıcı & Risk Matrisi")
    hedef_ip_port = st.text_input("Hedef IP / Domain", "127.0.0.1")
    taranacak_portlar = st.text_input("Taranacak Portlar (Virgülle ayırın)", "21,22,25,80,443,3306,8080")
    if st.button("Port Taraması Başlat"):
        with st.spinner("Portlar taranıyor..."):
            ports = [int(p.strip()) for p in taranacak_portlar.split(",") if p.strip().isdigit()]
            results = []
            for p in ports:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1)
                try:
                    res = s.connect_ex((hedef_ip_port.strip(), p))
                    if res == 0:
                        results.append({"Port": p, "Durum": "AÇIK 🟢", "Risk": "Yüksek / Orta" if p in [21,22,3306] else "Düşük"})
                    else:
                        results.append({"Port": p, "Durum": "KAPALI 🔴", "Risk": "Yok"})
                except:
                    results.append({"Port": p, "Durum": "Hata ⚠️", "Risk": "Bilinmiyor"})
                finally:
                    s.close()
            st.table(pd.DataFrame(results))

# 15. Sistem & Ağ Bilgisi
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Sistem Bilgisi")
    st.write(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    st.write(f"Makine Adı: {socket.gethostname()}")

# 16. Eğitim Amaçlı Oltalama Şablon Üreticisi (YENİ)
elif secim == "🎣 Eğitim Amaçlı Oltalama Şablon Üreticisi":
    st.subheader("🎣 Eğitim Amaçlı Oltalama (Phishing) Şablon Üreticisi")
    st.info("Bu modül, siber güvenlik farkındalık eğitimleri ve oltalama simülasyonları için güvenli HTML giriş sayfası şablonları üretir.")
    
    sim_turu = st.selectbox("Simülasyon Şablonu", ["Kurumsal E-Posta Giriş Sayfası", "Bulut Depolama Oturum Açma", "Şifre Sıfırlama Sayfası"])
    
    if st.button("Eğitim Şablonu Üret"):
        html_code = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <title>{sim_turu} - Güvenlik Simülasyonu</title>
    <style>
        body {{ background: #f4f4f4; font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
        .box {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); width: 350px; text-align: center; }}
        .warning {{ background: #ff5500; color: white; padding: 10px; font-size: 12px; margin-bottom: 15px; border-radius: 4px; font-weight: bold; }}
        input {{ width: 100%; padding: 10px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; }}
        button {{ width: 100%; padding: 10px; background: #333; color: white; border: none; border-radius: 4px; font-weight: bold; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="box">
        <div class="warning">🚨 EĞİTİM AMAÇLI SİMÜLASYON SAYFASIDIR.<br>Gerçek şifrenizi girmeyiniz!</div>
        <h2>{sim_turu}</h2>
        <form>
            <input type="text" placeholder="Kullanıcı Adı / E-Posta" required>
            <input type="password" placeholder="Şifre" required>
            <button type="submit">Giriş Yap</button>
        </form>
    </div>
</body>
</html>"""
        st.success("Eğitim şablonu başarıyla oluşturuldu!")
        st.text_area("Üretilen HTML Kodu:", html_code, height=200)
        st.download_button("Şablonu İndir (.html)", html_code, file_name="phishing_simulation.html", mime="text/html")

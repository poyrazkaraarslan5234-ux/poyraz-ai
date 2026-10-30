import streamlit as st
import socket
import platform
import hashlib
import urllib.request
import json
import pandas as pd
import random

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

# Yan Menü - IP ve Siber Güvenlik Modülleri
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "📍 IP Adresi Bulma & Detaylı Sorgulama",
        "🌐 IP & OSINT İstihbaratı",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "🌐 DNS Kayıtları & Domain Sorgulama",
        "📂 Web Dizin / Fuzzing Simülatörü",
        "🔓 Hash Şifre Kırıcı (Wordlist)",
        "📜 Mini Log Analiz Aracı",
        "💉 Web Güvenliği Payload Kütüphanesi",
        "💻 Sistem & Ağ Bilgisi"
    ]
)

# 1. IP ADRESİ BULMA & DETAYLI SORGULAMA
if secim == "📍 IP Adresi Bulma & Detaylı Sorgulama":
    st.subheader("📍 IP Adresi Bulma ve Detaylı Konum/ISP Analizi")
    st.info("Bu modül dış (public) IP adresinizi otomatik bulur ve istediğiniz IP'yi detaylıca sorgulamanızı sağlar.")
    
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

# 2. IP & OSINT İSTİHBARATI
elif secim == "🌐 IP & OSINT İstihbaratı":
    st.subheader("🌐 Web Sitesi & IP İstihbaratı (OSINT)")
    hedef_site = st.text_input("Hedef Domain / IP:", "google.com")
    if st.button("İstihbarat Topla"):
        try:
            ip_sonuc = socket.gethostbyname(hedef_site.strip())
            st.success(f"🎯 **Çözümlenen IP Adresi:** `{ip_sonuc}`")
            st.info("Bu IP adresi üzerinden detaylı konum ve ağ analizleri yapabilirsiniz.")
        except Exception as e:
            st.error(f"İstihbarat hatası: {e}")

# 3. PORT TARAYICI
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

# 4. DNS KAYITLARI & DOMAIN SORGULAMA
elif secim == "🌐 DNS Kayıtları & Domain Sorgulama":
    st.subheader("🌐 DNS Kayıtları & Domain Analizi")
    domain_adi = st.text_input("Hedef Domain:", "github.com")
    
    if st.button("DNS Bilgilerini Çözümle"):
        with st.spinner("DNS sunucuları sorgulanıyor..."):
            try:
                ip_adresi = socket.gethostbyname(domain_adi.strip())
                st.success(f"🎯 **A Kaydı (IP):** `{ip_adresi}`")
                st.info(f"📌 **Host Adı:** `{socket.getfqdn(domain_adi.strip())}`")
            except Exception as e:
                st.error(f"DNS çözümleme hatası: {e}")

# 5. WEB DİZİN / FUZZING SİMÜLATÖRÜ
elif secim == "📂 Web Dizin / Fuzzing Simülatörü":
    st.subheader("📂 Web Dizin / Dizin Taraması (Fuzzing) Simülasyonu")
    hedef_site_url = st.text_input("Hedef URL:", "https://example.com")
    wordlist_dizin = st.text_area("Dizin Listesi (Wordlist):", "admin\nlogin\napi\nuploads\nbackup\nconfig.php", height=120)
    
    if st.button("Dizin Taramasını Başlat"):
        with st.spinner("Dizinler taranıyor..."):
            dizinler = [d.strip() for d in wordlist_dizin.split("\n") if d.strip()]
            bulgular = []
            for dizin in dizinler:
                durum = "200 OK 🟢" if dizin in ["admin", "login", "api"] else "404 Not Found 🔴"
                boyut = random.randint(500, 5000) if "200" in durum else 0
                bulgular.append({
                    "Test Edilen Yol": f"{hedef_site_url.strip()}/{dizin}",
                    "HTTP Durum": durum,
                    "Boyut": f"{boyut} bytes"
                })
            st.table(pd.DataFrame(bulgular))

# 6. HASH ŞİFRE KIRICI
elif secim == "🔓 Hash Şifre Kırıcı (Wordlist)":
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

# 7. MINI LOG ANALİZ ARACI
elif secim == "📜 Mini Log Analiz Aracı":
    st.subheader("📜 Mini Web Log Analiz Aracı")
    sample_log = '192.168.1.10 - - [30/Oct/2026:12:00:00 +0300] "GET /index.html HTTP/1.1" 200 1024\n10.0.0.5 - - [30/Oct/2026:12:01:00 +0300] "GET /admin.php HTTP/1.1" 403 512'
    log_input = st.text_area("Log İçeriği:", sample_log, height=150)
    if st.button("Logları Analiz Et"):
        lines = [l.strip() for l in log_input.split("\n") if l.strip()]
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

# 8. PAYLOAD KÜTÜPHANESİ
elif secim == "💉 Web Güvenliği Payload Kütüphanesi":
    st.subheader("💉 Payload Kütüphanesi")
    st.text_area("Örnekler:", "<script>alert('XSS')</script>\n' OR '1'='1\n../../etc/passwd", height=100)

# 9. SİSTEM BİLGİSİ
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Sistem Bilgisi")
    st.write(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    st.write(f"Makine Adı: {socket.gethostname()}")

import streamlit as st
import socket
import platform
import hashlib
import urllib.request
import json
import datetime
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

# Session State Hedef/Tuzak Log Listesi
if 'target_logs' not in st.session_state:
    st.session_state['target_logs'] = []

st.markdown("<h1>🛡️ PC & MOBILE CYBER SUITE PRO</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Saf Siber Güvenlik & Penetrasyon Test Laboratuvarı</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü - Sadece Kritik Modüller
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "🎯 Oltalama Mesajı & Gerçek IP Yakalama",
        "🔌 Gelişmiş Port Tarayıcı & Risk Matrisi",
        "🔓 Hash Şifre Kırıcı (Wordlist)",
        "🌐 IP & OSINT İstihbaratı",
        "📜 Mini Log Analiz Aracı",
        "💉 Web Güvenliği Payload Kütüphanesi",
        "💻 Sistem & Ağ Bilgisi"
    ]
)

# 1. OLTALAMA MESAJI & GERÇEK IP YAKALAMA
if secim == "🎯 Oltalama Mesajı & Gerçek IP Yakalama":
    st.subheader("🎯 Oltalama Mesajı & Gerçek IP Yakalama Paneli")
    st.info("Hedefe atılacak tuzak mesajı hazırlayın. Hedef kişi bağlantıya tıkladığında gerçek IP ve tarayıcı bilgileri panele düşecektir.")
    
    tab1, tab2 = st.tabs(["✉️ Tuzak Mesaj Oluştur", "📊 Yakalanan Gerçek Hedef Logları"])
    
    with tab1:
        st.markdown("### 📨 Hedefe Atılacak Özelleştirilmiş Mesaj")
        tuzak_url = st.text_input("Tıklatılacak Tuzak URL (Streamlit Uygulama Linkin):", "https://poyraz-ai.streamlit.app")
        
        hazir_mesaj = f"""Selam! Senin için çok ilginç bir şey buldum, kesinlikle göz atmalısın:\n\n👉 {tuzak_url}\n\nTıklayınca ne demek istediğimi anlıycaksın :D"""
        
        st.text_area("Hedefe Gönderilecek Metin:", hazir_mesaj, height=130)
        st.download_button("Mesajı İndir (.txt)", hazir_mesaj, file_name="tuzak_mesaj.txt")
        
        st.markdown("---")
        st.markdown("### 🌐 Gerçek Ziyaretçi Yakalama Testi")
        st.write("Uygulamanı biri açtığında tarayıcı verilerini test etmek için aşağıdaki butona basabilirsin:")
        
        if st.button("Ziyaretçi Bilgilerimi (IP/Tarayıcı) Panele Kaydet"):
            headers = st.context.headers
            gercek_ip = headers.get("X-Forwarded-For", "Bilinmiyor (Yerel Ağ)").split(",")[0]
            user_agent = headers.get("User-Agent", "Bilinmiyor")
            
            yeni_hedef = {
                "Zaman": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Gerçek IP": gercek_ip,
                "Tarayıcı & Cihaz (User-Agent)": user_agent
            }
            if not st.session_state['target_logs'] or st.session_state['target_logs'][-1]["Gerçek IP"] != gercek_ip:
                st.session_state['target_logs'].append(yeni_hedef)
            st.success("🚨 BAŞARILI! Ziyaretçinin gerçek IP ve cihaz bilgileri panele işlendi!")

    with tab2:
        st.markdown("### 📊 Yakalanan Gerçek Hedefler Bilgi Paneli")
        if st.button("Tüm Logları Temizle"):
            st.session_state['target_logs'] = []
            st.rerun()
            
        if len(st.session_state['target_logs']) > 0:
            df_targets = pd.DataFrame(st.session_state['target_logs'])
            st.table(df_targets)
        else:
            st.info("Henüz tuzağa düşen kimse yok. 'Tuzak Mesaj Oluştur' sekmesinden test edebilirsin.")

# 2. PORT TARAYICI
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

# 3. HASH ŞİFRE KIRICI
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

# 4. IP & OSINT İSTİHBARATI
elif secim == "🌐 IP & OSINT İstihbaratı":
    st.subheader("🌐 IP Adresi ve Domain İstihbaratı")
    hedef_ip = st.text_input("Sorgulanacak IP Adresi veya Domain:", "8.8.8.8")
    
    if st.button("Bilgileri Sorgula"):
        with st.spinner("Veritabanı Taranıyor..."):
            try:
                url = f"http://ip-api.com/json/{hedef_ip.strip()}"
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response:
                    veri = json.loads(response.read().decode('utf-8'))
                    if veri.get("status") == "success":
                        st.success(f"🎯 **Hedef:** `{veri.get('query')}`")
                        st.write(f"🌍 **Ülke:** {veri.get('country')} ({veri.get('countryCode')})")
                        st.write(f"🏙️ **Şehir:** {veri.get('city')} / {veri.get('regionName')}")
                        st.write(f"🏢 **Servis Sağlayıcı (ISP):** {veri.get('isp')}")
                    else:
                        st.error("❌ Sorgu başarısız oldu!")
            except Exception as e:
                st.error(f"Hata: {e}")

# 5. MINI LOG ANALİZ ARACI
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

# 6. PAYLOAD KÜTÜPHANESİ
elif secim == "💉 Web Güvenliği Payload Kütüphanesi":
    st.subheader("💉 Payload Kütüphanesi")
    st.text_area("Örnekler:", "<script>alert('XSS')</script>\n' OR '1'='1\n../../etc/passwd", height=100)

# 7. SİSTEM BİLGİSİ
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Sistem Bilgisi")
    st.write(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    st.write(f"Makine Adı: {socket.gethostname()}")

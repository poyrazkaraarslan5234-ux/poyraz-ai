import streamlit as st
import socket
import platform
import pandas as pd
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Cyber Suite - IP & Cihaz Yakalama Tuzağı",
    page_icon="🎯",
    layout="centered"
)

# Hacker Teması İçin CSS
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

# Session State Log Listesi
if 'target_logs' not in st.session_state:
    st.session_state['target_logs'] = []

st.markdown("<h1>🎯 IP & CİHAZ YAKALAMA TUZAĞI</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Bağlantıya Tıklayan Kişinin Bilgilerini Yakalama Paneli</p>", unsafe_allow_html=True)
st.markdown("---")

# Modül Listesi (Gereksizler Temizlendi)
secim = st.sidebar.selectbox(
    "Siber Güvenlik Modülleri",
    [
        "🎯 Hedef Yakalama & Mesaj Tuzağı",
        "🔌 Gelişmiş Port Tarayıcı",
        "💻 Sistem & Ağ Bilgisi"
    ]
)

# 1. HEDEF YAKALAMA & MESAJ TUZAĞI
if secim == "🎯 Hedef Yakalama & Mesaj Tuzağı":
    st.subheader("🎯 Hedef Kişi İçin Tuzak Mesaj & Log Paneli")
    st.info("Hedefe atılacak mesajı oluşturun. Kişi bağlantıya tıkladığında simüle edilen cihaz ve IP bilgileri panele düşecektir.")
    
    tab1, tab2 = st.tabs(["✉️ Tuzak Mesaj Oluştur", "📊 Yakalanan Hedef Bilgileri (Panel)"])
    
    with tab1:
        st.markdown("### 📨 Hedefe Atılacak Özelleştirilmiş Mesaj")
        konu_basligi = st.text_input("Mesaj Konusu / Bahane:", "Önemli Fotoğraf / Dosya Paylaşımı")
        tuzak_url = st.text_input("Tıklatılacak Tuzak URL:", "https://discord-gift-nitro.com/claim/free")
        
        hazir_mesaj = f"""Selam! Senin için çok ilginç bir şey buldum, kesinlikle göz atmalısın:\n\n👉 {tuzak_url}\n\nTıklayınca ne demek istediğimi anlıycaksın :D"""
        
        st.text_area("Hedefe Gönderilecek Metin:", hazir_mesaj, height=130)
        st.download_button("Mesajı İndir (.txt)", hazir_mesaj, file_name="tuzak_mesaj.txt")
        
        st.markdown("---")
        st.markdown("### 🧪 Test Alanı (Bağlantıya Tıklama Simülasyonu)")
        st.write("Hedef kişinin bağlantıya tıkladığını simüle etmek için aşağıdaki butona basabilirsin:")
        
        if st.button("Hedef Bağlantıya Tıkladı (Simülasyonu Tetikle)"):
            # Hedefin verilerini yakalama simülasyonu
            yeni_hedef = {
                "Tıklama Zamanı": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Hedef IP": "185.120.xx.xx (Yakalandı)",
                "Cihaz / İşletim Sistemi": "Android / Mobile Chrome",
                "Tarayıcı Dili": "Türkçe (tr-TR)",
                "Ekran Çözünürlüğü": "1080x2340"
            }
            st.session_state['target_logs'].append(yeni_hedef)
            st.success("🚨 BAŞARILI! Hedef bağlantıya tıkladı ve bilgileri sisteme düştü!")

    with tab2:
        st.markdown("### 📊 Yakalanan Hedeflerin Bilgi Paneli")
        if st.button("Tüm Logları Temizle"):
            st.session_state['target_logs'] = []
            st.rerun()
            
        if len(st.session_state['target_logs']) > 0:
            df_targets = pd.DataFrame(st.session_state['target_logs'])
            st.table(df_targets)
        else:
            st.info("Henüz tuzağa düşen kimse yok. 'Tuzak Mesaj Oluştur' sekmesinden simülasyonu test edebilirsin.")

# 2. PORT TARAYICI
elif secim == "🔌 Gelişmiş Port Tarayıcı":
    st.subheader("🔌 Gelişmiş Port Tarayıcı")
    hedef_ip_port = st.text_input("Hedef IP / Domain", "127.0.0.1")
    taranacak_portlar = st.text_input("Taranacak Portlar (Virgülle ayırın)", "21,22,80,443")
    if st.button("Port Taraması Başlat"):
        ports = [int(p.strip()) for p in taranacak_portlar.split(",") if p.strip().isdigit()]
        results = []
        for p in ports:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            try:
                res = s.connect_ex((hedef_ip_port.strip(), p))
                if res == 0:
                    results.append({"Port": p, "Durum": "AÇIK 🟢"})
                else:
                    results.append({"Port": p, "Durum": "KAPALI 🔴"})
            except:
                results.append({"Port": p, "Durum": "Hata ⚠️"})
            finally:
                s.close()
        st.table(pd.DataFrame(results))

# 3. SİSTEM BİLGİSİ
elif secim == "💻 Sistem & Ağ Bilgisi":
    st.subheader("💻 Sistem Bilgisi")
    st.write(f"İşletim Sistemi: {platform.system()} {platform.release()}")
    st.write(f"Makine Adı: {socket.gethostname()}")

import streamlit as st
import socket
import platform
import subprocess

# Sayfa Yapılandırması
st.set_page_config(
    page_title="PC-Flipper Web Paneli",
    page_icon="🛡️",
    layout="centered"
)

# Hacker Teması İçin CSS (Koyu tema & Flipper turuncusu vurgular)
st.markdown("""
    <style>
    .main {
        background-color: #121212;
        color: #00ff00;
    }
    h1 {
        color: #ffa500;
        text-align: center;
        font-family: 'Courier New', monospace;
    }
    .stButton>button {
        width: 100%;
        background-color: #222;
        color: #fff;
        border: 1px solid #ffa500;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ffa500;
        color: #000;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.markdown("<h1>🛡️ PC-FLIPPER WEB PANELİ</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Telefondan ve Bilgisayardan Siber Keşif Merkezi</p>", unsafe_allow_html=True)
st.markdown("---")

# Yan Menü (Hangi işlemi yapmak istiyorsun?)
secim = st.sidebar.selectbox(
    "Menü Seçin",
    ["Sistem Bilgisi", "Ağ Cihazlarını Tara", "Port Tara", "Kayıtlı Wi-Fi'ler"]
)

# 1. Sistem Bilgisi
if secim == "Sistem Bilgisi":
    st.subheader("💻 Bilgisayar Sistem Bilgileri")
    if st.button("Bilgileri Getir"):
        with st.spinner("Bilgiler taranıyor..."):
            st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")
            st.write(f"**Bilgisayar Adı:** {platform.node()}")
            st.write(f"**İşlemci:** {platform.processor()}")
            try:
                yerel_ip = socket.gethostbyname(socket.gethostname())
                st.write(f"**Yerel IP Adresi:** {yerel_ip}")
            except:
                pass
            st.success("İşlem tamamlandı!")

# 2. Ağ Cihazlarını Tara
elif secim == "Ağ Cihazlarını Tara":
    st.subheader("🔍 Yerel Ağ Taraması (Ping Sweep)")
    st.info("Aynı ağa bağlı olan aktif cihazları listeler.")
    if st.button("Ağı Tara"):
        with st.spinner("Ağdaki cihazlar taranıyor, lütfen bekleyin..."):
            try:
                hostname = socket.gethostname()
                yerel_ip = socket.gethostbyname(hostname)
                ip_parcalari = yerel_ip.rsplit('.', 1)[0]
                
                bulunanlar = []
                progress_bar = st.progress(0)
                
                for i in range(1, 30):  # Hızlı olması için ilk 30 IP
                    hedef = f"{ip_parcalari}.{i}"
                    parametre = "-n 1" if platform.system().lower() == "windows" else "-c 1"
                    islem = subprocess.Popen(f"ping {parametre} -w 50 {hedef}", stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                    islem.wait()
                    
                    if islem.returncode == 0:
                        bulunanlar.append(hedef)
                    progress_bar.progress(i / 30)
                
                if bulunanlar:
                    st.success(f"Toplam {len(bulunanlar)} aktif cihaz bulundu:")
                    for cihaz in bulunanlar:
                        st.code(cihaz)
                else:
                    st.warning("Aktif cihaz bulunamadı.")
            except Exception as e:
                st.error(f"Hata oluştu: {e}")

# 3. Port Tara
elif secim == "Port Tara":
    st.subheader("🔌 Port Tarayıcı")
    hedef_ip = st.text_input("Taranacak IP Adresi", "192.168.1.1")
    if st.button("Portları Tara"):
        with st.spinner(f"{hedef_ip} taranıyor..."):
            portlar = [21, 22, 23, 80, 443, 445, 3306, 8080]
            for port in portlar:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.3)
                    sonuc = s.connect_ex((hedef_ip, port))
                    if sonuc == 0:
                        st.write(f"🟢 **Port {port}**: AÇIK")
                    else:
                        st.write(f"🔴 **Port {port}**: Kapalı")
                    s.close()
                except:
                    pass
            st.success("Port taraması bitti.")

# 4. Kayıtlı Wi-Fi'ler
elif secim == "Kayıtlı Wi-Fi'ler":
    st.subheader("📶 Kayıtlı Wi-Fi Ağ Profilleri")
    if st.button("Wi-Fi Profillerini Listele"):
        with st.spinner("Profiller okunuyor..."):
            try:
                sonuc = subprocess.check_output("netsh wlan show profiles", shell=True, encoding="latin5")
                st.text(sonuc)
            except Exception as e:
                st.error(f"Hata: {e}")

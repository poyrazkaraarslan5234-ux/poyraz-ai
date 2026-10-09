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

# Hacker Teması İçin CSS
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
""", unsafe_allow_html=True,)

st.markdown("<h1>🛡️ PC-FLIPPER WEB PANELİ</h1>", unsafe_allow_html=True)
st.write("<p style='text-align: center; color: #888;'>Bulut Tabanlı Siber Keşif Merkezi</p>", unsafe_allow_html=True)
st.markdown("---")

secim = st.sidebar.selectbox(
    "Menü Seçin",
    ["Sistem Bilgisi", "Port Tara", "Kayıtlı Wi-Fi'ler"]
)

# 1. Sistem Bilgisi
if secim == "Sistem Bilgisi":
    st.subheader("💻 Sistem Bilgileri")
    if st.button("Bilgileri Getir"):
        with st.spinner("Bilgiler okunuyor..."):
            st.write(f"**İşletim Sistemi:** {platform.system()} {platform.release()}")
            st.write(f"**Bilgisayar Adı:** {platform.node()}")
            st.write(f"**İşlemci:** {platform.processor()}")
            try:
                yerel_ip = socket.gethostbyname(socket.gethostname())
                st.write(f"**IP / Host Adresi:** {yerel_ip}")
            except:
                pass
            st.success("İşlem tamamlandı!")

# 2. Port Tara (Hedef IP'nin portlarını kontrol eder)
elif secim == "Port Tara":
    st.subheader("🔌 Port Tarayıcı")
    hedef_ip = st.text_input("Taranacak IP veya Domain (örn: 127.0.0.1 veya google.com)", "127.0.0.1")
    timeout_suresi = st.slider("Zaman Aşımı Süresi (Saniye)", min_value=0.5, max_value=3.0, value=1.0, step=0.5)
    
    if st.button("Portları Tara"):
        with st.spinner(f"{hedef_ip} taranıyor..."):
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
                except socket.timeout:
                    st.write(f"🟡 **Port {port}**: Zaman Aşımı")
                except:
                    pass
            st.success("Tarama tamamlandı.")

# 3. Kayıtlı Wi-Fi'ler
elif secim == "Kayıtlı Wi-Fi'ler":
    st.subheader("📶 Kayıtlı Wi-Fi Ağ Profilleri")
    st.info("Not: Bu özellik sadece kendi bilgisayarınızda (lokalde) çalışırken bilgisayarınızdaki Wi-Fi profillerini gösterir.")
    if st.button("Wi-Fi Profillerini Listele"):
        with st.spinner("Profiller okunuyor..."):
            try:
                sonuc = subprocess.check_output("netsh wlan show profiles", shell=True, encoding="latin5")
                st.text(sonuc)
            except Exception as e:
                st.error(f"Bulut sunucusunda yerel Wi-Fi profilleri okunamaz: {e}")

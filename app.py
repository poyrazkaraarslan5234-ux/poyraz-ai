import hashlib
import socket
import subprocess
import platform
import streamlit as st
import requests
import pandas as pd

# Sayfa Yapılandırması
st.set_page_config(
    page_title="Siber Güvenlik & Ağ Analiz Paneli",
    page_icon="🛡️",
    layout="wide"
)

# Özel CSS İyileştirmeleri
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stSidebar {
        background-color: #161b22;
    }
    </style>
""", unsafe_allow_html=True)

# Başlık
st.title("🛡️ Siber Güvenlik ve Ağ Analiz Paneli")
st.markdown("Bu panel; yerel ağ teşhisi, bilgi toplama (OSINT), şifreleme ve sistem güvenlik kontrolleri yapmanızı sağlar.")

# Kenar Çubuğu (Sidebar) Menüsü
st.sidebar.title("🛠️ Araçlar")
menu = st.sidebar.selectbox(
    "Bir modül seçin:",
    ["Ana Sayfa", "Ağ ve Port Tarama", "Bilgi Toplama (OSINT)", "Hash & Şifre Araçları", "Yerel Sistem Bilgileri"]
)

# --- 1. ANA SAYFA ---
if menu == "Ana Sayfa":
    st.subheader("Hoş Geldiniz!")
    st.info("Sol menüden kullanmak istediğiniz siber güvenlik veya ağ analiz aracını seçebilirsiniz.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🔍 Özellikler")
        st.markdown("""
        - **Ağ & Port Tarama:** Hızlı port kontrolü ve socket testleri.
        - **DNS & IP Sorgulama:** Hedef adresler hakkında keşif araçları.
        - **Kriptografi:** Hash (MD5, SHA256) üretme ve güçlü şifre oluşturma.
        - **Sistem Teşhisi:** Yerel ağ bağlantılarını ve durumlarını inceleme.
        """)
    with col2:
        st.markdown("### ⚠️ Yasal Uyarı")
        st.warning("Bu araç yalnızca eğitim, kişisel geliştirme ve yetkili sistem denetimleri amacıyla tasarlanmıştır. İzin alınmayan hedef sistemler üzerinde taranması ve test edilmesi yasal sorumluluk doğurabilir.")

# --- 2. AĞ VE PORT TARAMA ---
elif menu == "Ağ ve Port Tarama":
    st.subheader("🌐 Ağ ve Port Tarama Aracı")
    
    target_ip = st.text_input("Hedef IP Adresi veya Domain", "127.0.0.1")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Hızlı Port Kontrolü")
        default_ports = [21, 22, 23, 25, 53, 80, 110, 443, 3306, 8080]
        selected_ports = st.multiselect("Kontrol Edilecek Portlar", default_ports, default=[21, 22, 80, 443, 3306])
        
        if st.button("Portları Tara"):
            if not target_ip:
                st.error("Lütfen geçerli bir IP veya domain girin.")
            else:
                results = []
                with st.spinner("Portlar taranıyor..."):
                    for port in selected_ports:
                        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        s.settimeout(1)
                        try:
                            result = s.connect_ex((target_ip, port))
                            if result == 0:
                                results.append({"Port": port, "Durum": "AÇIK 🟢"})
                            else:
                                results.append({"Port": port, "Durum": "KAPALI 🔴"})
                        except Exception:
                            results.append({"Port": port, "Durum": "Hata ⚠️"})
                        finally:
                            s.close()
                
                df = pd.DataFrame(results)
                st.table(df)

    with col2:
        st.markdown("#### Ping / Erişilebilirlik Testi")
        ping_target = st.text_input("Ping Atılacak Adres", "google.com")
        if st.button("Ping Gönder"):
            with st.spinner("Ping atılıyor..."):
                param = "-n" if platform.system().lower() == "windows" else "-c"
                command = ["ping", param, "2", ping_target]
                try:
                    output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
                    st.code(output)
                except subprocess.CalledProcessError as e:
                    st.error(f"Ping başarısız oldu:\n{e.output}")

# --- 3. BİLGİ TOPLAMA (OSINT) ---
elif menu == "Bilgi Toplama (OSINT)":
    st.subheader("🕵️ Bilgi Toplama ve Keşif Aracı")
    
    domain_input = st.text_input("Hedef Domain (Örn: example.com)", "google.com")
    
    if st.button("Bilgileri Getir"):
        if not domain_input:
            st.error("Lütfen bir domain girin.")
        else:
            with st.spinner("Bilgiler toplanıyor..."):
                # IP Adresi Çözümleme
                try:
                    ip_addr = socket.gethostbyname(domain_input)
                    st.success(f"**IP Adresi:** {ip_addr}")
                except socket.gaierror:
                    st.error("IP adresi çözümlenemedi.")
                    ip_addr = None

                # IP Geolocation (Konum Bilgisi)
                if ip_addr:
                    try:
                        response = requests.get(f"http://ip-api.com/json/{ip_addr}", timeout=3)
                        data = response.json()
                        if data["status"] == "success":
                            col1, col2, col3 = st.columns(3)
                            col1.metric("Ülke", data.get("country", "-"))
                            col2.metric("Şehir", data.get("city", "-"))
                            col3.metric("İSS (ISP)", data.get("isp", "-"))
                    except Exception:
                        st.info("Coğrafi konum bilgisi alınamadı.")

# --- 4. HASH & ŞİFRE ARAÇLARI ---
elif menu == "Hash & Şifre Araçları":
    st.subheader("🔑 Kriptografi ve Parola Araçları")
    
    tab1, tab2 = st.tabs(["Hash Oluşturucu", "Güçlü Parola Üreteci"])
    
    with tab1:
        text_to_hash = st.text_input("Hash'lenecek Metin", "merhaba")
        if text_to_hash:
            st.markdown(f"**MD5:** `{hashlib.md5(text_to_hash.encode()).hexdigest()}`")
            st.markdown(f"**SHA-256:** `{hashlib.sha256(text_to_hash.encode()).hexdigest()}`")
            st.markdown(f"**SHA-512:** `{hashlib.sha512(text_to_hash.encode()).hexdigest()}`")
            
    with tab2:
        import random
        import string
        
        length = st.slider("Parola Uzunluğu", 8, 32, 16)
        use_symbols = st.checkbox("Özel Karakterler İçersin (!@#$)", value=True)
        
        if st.button("Güçlü Parola Üret"):
            chars = string.ascii_letters + string.digits
            if use_symbols:
                chars += string.punctuation
            password = "".join(random.choice(chars) for _ in range(length))
            st.code(password)

# --- 5. YEREL SİSTEM BİLGİLERİ ---
elif menu == "Yerel Sistem Bilgileri":
    st.subheader("💻 Yerel Sistem Teşhisi")
    
    st.markdown("#### Aktif Ağ Soketleri (Netstat Özeti)")
    if st.button("Bağlantıları Listele"):
        with st.spinner("Soketler taranıyor..."):
            try:
                # Windows için netstat -an komutu
                command = ["netstat", "-an"]
                output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
                # Çok uzun olmaması için ilk 30 satırı gösterelim
                lines = output.split("\n")[:30]
                st.code("\n".join(lines))
            except Exception as e:
                st.error(f"Komut çalıştırılamadı: {e}")

import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Özel Instagram Tarzı Profil Kartı Tasarımı (CSS)
st.markdown("""
    <style>
    .profile-card {
        display: flex;
        align-items: center;
        background-color: #1e1e1e;
        padding: 10px 15px;
        border-radius: 12px;
        margin-bottom: 8px;
        border: 1px solid #333;
    }
    .profile-ring {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 2px;
        margin-right: 15px;
        flex-shrink: 0;
    }
    .profile-inner {
        width: 100%;
        height: 100%;
        background-color: #121212;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    }
    .profile-info {
        display: flex;
        flex-direction: column;
        flex-grow: 1;
    }
    .profile-name {
        color: #ffffff;
        font-weight: bold;
        font-size: 16px;
        text-decoration: none;
    }
    .profile-name:hover {
        text-decoration: underline;
        color: #0095f6;
    }
    .badge-free {
        color: #2ecc71;
        font-size: 11px;
        font-weight: bold;
    }
    .badge-taken {
        color: #e74c3c;
        font-size: 11px;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# Arayüz Başlığı
st.title("Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu (Sınırsız Sürüm)")

# Mod Seçimi
mod = st.selectbox(
    "Arama Modunu Seç:",
    [
        "1. Tek Kelime Sınırsız Kombinasyon", 
        "2. İki Kelime Birleştirici (Name Mixer)", 
        "3. Doğum Yılı / Yaş Kombinasyonları"
    ]
)

# Müsaitlik Tahmin Fonksiyonu
def musaitlik_tahmini(kullanici_adi):
    if len(kullanici_adi) > 12 or "_" in kullanici_adi or "." in kullanici_adi or any(c.isdigit() for c in kullanici_adi):
        return "Boşta Olabilir", "badge-free"
    else:
        return "Alınmış Olabilir", "badge-taken"

# 1. Tek Kelime - TÜM Kombinasyonları Döken Fonksiyon
@st.cache_data
def sinirsiz_kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    kombinasyonlar = set()
    kombinasyonlar.add(temiz)
    
    # Leet Speak
    leet = temiz.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '5')
    if leet != temiz:
        kombinasyonlar.add(leet)

    # Harf Ekleme / Çoğaltma
    if len(temiz) > 0:
        ilk = temiz[0]
        son = temiz[-1]
        kombinasyonlar.add(ilk + temiz)          
        kombinasyonlar.add(temiz + son)          
        kombinasyonlar.add(ilk + ilk + temiz[1:]) 
        kombinasyonlar.add(temiz[:-1] + son + son) 
        
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i] + temiz[i:])

    # Harf Eksiltme
    if len(temiz) > 2:
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i+1:])

    # Alttan çizgi ve nokta çeşitleri
    if len(temiz) > 1:
        for i in range(1, len(temiz)):
            kombinasyonlar.add(temiz[:i] + "_" + temiz[i:])
            kombinasyonlar.add(temiz[:i] + "." + temiz[i:])
        kombinasyonlar.add("_".join(list(temiz)))
        kombinasyonlar.add(".".join(list(temiz)))

    on_ekler = ["", "_", ".", "x", "z", "real", "official", "the", "i", "m"]
    
    arka_ekler = [""]
    for i in range(200):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ekler = [
        "yilmaz", "kaya", "demir", "celik", "yildiz", "ozturk", "aydin", "arslan", "sahin",
        "34", "35", "52", "06", "07", "61", "99", "16", "26", "41",
        "2023", "2024", "2025", "2026", "tc", "bey", "pro", "x", "z", "insta", "store",
        "tv", "offical", "fan", "hq", "gram", "net", "com", "tr", "iz", "orijinal"
    ]
    arka_ekler.extend(ekler)
    
    for on in on_ekler:
        for arka in arka_ekler:
            if not on and not arka:
                continue
            kombinasyonlar.add(f"{on}{temiz}{arka}")
            kombinasyonlar.add(f"{arka}{temiz}{on}")
            
            if arka:
                kombinasyonlar.add(f"{temiz}_{arka}")
                kombinasyonlar.add(f"{temiz}.{arka}")
                kombinasyonlar.add(f"{on}_{temiz}_{arka}")
                kombinasyonlar.add(f"{on}.{temiz}.{arka}")

    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# 2. İki Kelime Sınırsız Mixer
@st.cache_data
def sinirsiz_mixer(kelime1, kelime2):
    k1 = kelime1.lower().strip().replace(" ", "")
    k2 = kelime2.lower().strip().replace(" ", "")
    if not k1 or not k2:
        return []
        
    kombinasyonlar = set()
    
    birlestirmeler = [
        f"{k1}{k2}", f"{k1}_{k2}", f"{k1}.{k2}",
        f"{k2}{k1}", f"{k2}_{k1}", f"{k2}.{k1}",
        f"{k1[0]}{k2}", f"{k1}{k2[0]}",
        f"{k1[0]}_{k2}", f"{k1}.{k2[0]}"
    ]
    for b in birlestirmeler:
        kombinasyonlar.add(b)
        
    for ek in ["34", "35", "06", "52", "99", "2025", "2026", "official", "real", "x", "z", "pro"]:
        kombinasyonlar.add(f"{k1}{k2}{ek}")
        kombinasyonlar.add(f"{k1}_{k2}_{ek}")
        kombinasyonlar.add(f"{k1}.{k2}.{ek}")
        kombinasyonlar.add(f"{k2}{k1}{ek}")
        kombinasyonlar.add(f"{k2}_{k1}_{ek}")

    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# 3. Doğum Yılı / Yaş Sınırsız Üretici
@st.cache_data
def sinirsiz_yil(kelime, yil_deger):
    temiz = kelime.lower().strip().replace(" ", "")
    y = str(yil_deger).strip()
    if not temiz or not y:
        return []
        
    kombinasyonlar = set()
    
    sekiller = [
        f"{temiz}{y}", f"{temiz}_{y}", f"{temiz}.{y}",
        f"{y}{temiz}", f"{y}_{temiz}", f"{y}.{temiz}"
    ]
    for s in sekiller:
        kombinasyonlar.add(s)
        
    if len(y) == 4:
        kisa_yil = y[2:]
        kombinasyonlar.add(f"{temiz}{kisa_yil}")
        kombinasyonlar.add(f"{temiz}_{kisa_yil}")
        kombinasyonlar.add(f"{temiz}.{kisa_yil}")
        kombinasyonlar.add(f"{kisa_yil}{temiz}")

    for ek in ["_", ".", "x", "z", "real", "official"]:
        kombinasyonlar.add(f"{temiz}{ek}{y}")
        kombinasyonlar.add(f"{y}{ek}{temiz}")

    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# Arayüz Çalıştırma Alanı
if mod == "1. Tek Kelime Sınırsız Kombinasyon":
    aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")
    if aranan:
        adaylar = sinirsiz_kombinasyon_uret(aranan)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"'{aranan}' için üretilen TÜM **{len(sonuclar)}** adet hesap hazırlandı!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("📥 Tüm Listeyi .TXT Olarak İndir", txt_icerigi, file_name=f"poyraz_ai_{aranan}_tum_hesaplar.txt", mime="text/plain")
        
        st.markdown("### 📋 Toplu Kopyalama Alanı")
        st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
        
        st.markdown(f"### 🔗 Sınırsız Profil Kartları ({len(sonuclar)} Adet)")
        with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=False):
            for k, url in zip(adaylar, sonuclar):
                durum, sinif = musaitlik_tahmini(k)
                st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-ring"><div class="profile-inner">👤</div></div>
                        <div class="profile-info">
                            <a class="profile-name" href="{url}" target="_blank">@{k}</a>
                            <span class="{sinif}">Tahmini Durum: {durum}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

elif mod == "2. İki Kelime Birleştirici (Name Mixer)":
    c1, c2 = st.columns(2)
    with c1: k1 = st.text_input("Birinci Kelime (Ad):")
    with c2: k2 = st.text_input("İkinci Kelime (Soyad):")
    
    if k1 and k2:
        adaylar = sinirsiz_mixer(k1, k2)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"Harmanlanan TÜM **{len(sonuclar)}** adet hesap hazırlandı!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("📥 Tüm Listeyi .TXT Olarak İndir", txt_icerigi, file_name=f"poyraz_ai_mixer_tum.txt", mime="text/plain")
        
        st.markdown("### 📋 Toplu Kopyalama Alanı")
        st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
        
        st.markdown(f"### 🔗 Sınırsız Profil Kartları ({len(sonuclar)} Adet)")
        with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=True):
            for k, url in zip(adaylar, sonuclar):
                durum, sinif = musaitlik_tahmini(k)
                st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-ring"><div class="profile-inner">👤</div></div>
                        <div class="profile-info">
                            <a class="profile-name" href="{url}" target="_blank">@{k}</a>
                            <span class="{sinif}">Tahmini Durum: {durum}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

else: # Doğum Yılı / Yaş Sınırsız
    c1, c2 = st.columns(2)
    with c1: isim = st.text_input("İsim veya Kelime:")
    with c2: dogum_yili = st.text_input("Doğum Yılı (Örn: 2005):", value="2005")
    
    if isim and dogum_yili:
        adaylar = sinirsiz_yil(isim, dogum_yili)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"Yıllarla harmanlanan TÜM **{len(sonuclar)}** adet hesap hazırlandı!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("📥 Tüm Listeyi .TXT Olarak İndir", txt_icerigi, file_name=f"poyraz_ai_yil_tum.txt", mime="text/plain")
        
        st.markdown("### 📋 Toplu Kopyalama Alanı")
        st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
        
        st.markdown(f"### 🔗 Sınırsız Profil Kartları ({len(sonuclar)} Adet)")
        with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=True):
            for k, url in zip(adaylar, sonuclar):
                durum, sinif = musaitlik_tahmini(k)
                st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-ring"><div class="profile-inner">👤</div></div>
                        <div class="profile-info">
                            <a class="profile-name" href="{url}" target="_blank">@{k}</a>
                            <span class="{sinif}">Tahmini Durum: {durum}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

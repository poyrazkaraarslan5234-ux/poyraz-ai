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
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# Gelişmiş Mod Seçimi
mod = st.selectbox(
    "Arama Modunu Seç:",
    [
        "1. Tek Kelime Akilli Arama", 
        "2. Iki Kelime Birlestirici (Name Mixer)", 
        "3. Dogum Yili / Yas Kombinasyonlari", 
        "4. Ultra Kisa / Nadir Isimler"
    ]
)

# Gelişmiş Filtreler (Kenar Çubuğu veya Expander)
with st.expander("Gelismis Filtreler ve Kisitlamalar (Tikla Ac)", expanded=False):
    min_uzunluk = st.slider("En Az Karakter Sayisi", 3, 10, 3)
    max_uzunluk = st.slider("En Cok Karakter Sayisi", 10, 30, 30)
    nokta_yasakla = st.checkbox("Nokta (.) Kullanma", value=False)
    cizgi_yasakla = st.checkbox("Alttan Cizgi (_) Kullanma", value=False)

def filtreleri_uygula(liste):
    filtrelenmis = []
    for k in liste:
        if len(k) < min_uzunluk or len(k) > max_uzunluk:
            continue
        if nokta_yasakla and "." in k:
            continue
        if cizgi_yasakla and "_" in k:
            continue
        filtrelenmis.append(k)
    return filtrelenmis

# Müsaitlik Tahmin Fonksiyonu
def musaitlik_tahmini(kullanici_adi):
    if len(kullanici_adi) > 12 or "_" in kullanici_adi or "." in kullanici_adi or any(c.isdigit() for c in kullanici_adi):
        return "Bosta Olabilir", "badge-free"
    else:
        return "Alinmis Olabilir", "badge-taken"

# 1. Tek Kelime Arama Fonksiyonu
@st.cache_data
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    kombinasyonlar = set()
    kombinasyonlar.add(temiz)
    
    leet = temiz.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '5')
    if leet != temiz:
        kombinasyonlar.add(leet)

    if len(temiz) > 0:
        ilk = temiz[0]
        son = temiz[-1]
        kombinasyonlar.add(ilk + temiz)          
        kombinasyonlar.add(temiz + son)          
        kombinasyonlar.add(ilk + ilk + temiz[1:]) 
        kombinasyonlar.add(temiz[:-1] + son + son) 
        
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i] + temiz[i:])

    if len(temiz) > 2:
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i+1:])

    if len(temiz) > 1:
        for i in range(1, len(temiz)):
            kombinasyonlar.add(temiz[:i] + "_" + temiz[i:])
        kombinasyonlar.add("_".join(list(temiz)))

    on_ekler = ["", "_", ".", "x", "z", "real"]
    arka_ekler = [""]
    for i in range(50):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ekler = [
        "yilmaz", "kaya", "demir", "celik", "yildiz", "ozturk", "aydin",
        "34", "35", "52", "06", "07", "61", "99",
        "2025", "2026", "tc", "bey", "pro", "x", "z", "insta", "store"
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

    return sorted(list(set(kombinasyonlar)), key=len)

# 2. İki Kelime Birleştirici
@st.cache_data
def mixer_uret(kelime1, kelime2):
    k1 = kelime1.lower().strip().replace(" ", "")
    k2 = kelime2.lower().strip().replace(" ", "")
    if not k1 or not k2:
        return []
        
    kombinasyonlar = set()
    kombinasyonlar.add(f"{k1}{k2}")
    kombinasyonlar.add(f"{k1}_{k2}")
    kombinasyonlar.add(f"{k1}.{k2}")
    kombinasyonlar.add(f"{k2}{k1}")
    kombinasyonlar.add(f"{k2}_{k1}")
    
    if len(k1) > 3 and len(k2) > 3:
        kombinasyonlar.add(f"{k1[:3]}{k2}")
        kombinasyonlar.add(f"{k1}{k2[:3]}")
        kombinasyonlar.add(f"{k1[:3]}_{k2}")
        kombinasyonlar.add(f"{k1}_{k2[:3]}")

    for ek in ["34", "35", "06", "52", "99", "2026", "official", "real"]:
        kombinasyonlar.add(f"{k1}{k2}{ek}")
        kombinasyonlar.add(f"{k1}_{k2}_{ek}")
        kombinasyonlar.add(f"{k1}.{k2}.{ek}")

    return sorted(list(set(kombinasyonlar)), key=len)

# 3. Doğum Yılı / Yaş Kombinasyonları
@st.cache_data
def yil_uret(kelime, yil_deger):
    temiz = kelime.lower().strip().replace(" ", "")
    y = str(yil_deger).strip()
    if not temiz or not y:
        return []
        
    kombinasyonlar = set()
    kombinasyonlar.add(f"{temiz}{y}")
    kombinasyonlar.add(f"{temiz}_{y}")
    kombinasyonlar.add(f"{temiz}.{y}")
    kombinasyonlar.add(f"{y}{temiz}")
    kombinasyonlar.add(f"{y}_{temiz}")
    
    # Kısa yıl formatı (örn: 2005 -> 05)
    if len(y) == 4:
        kisa_yil = y[2:]
        kombinasyonlar.add(f"{temiz}{kisa_yil}")
        kombinasyonlar.add(f"{temiz}_{kisa_yil}")
        kombinasyonlar.add(f"{temiz}.{kisa_yil}")

    return sorted(list(set(kombinasyonlar)), key=len)

# 4. Ultra Kısa / Nadir İsimler
@st.cache_data
def kisa_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if len(temiz) < 3:
        return [temiz]
        
    kombinasyonlar = set()
    # Sadece ilk 3-4 harf ile harmanlamalar
    kombinasyonlar.add(temiz[:3])
    kombinasyonlar.add(temiz[:4])
    kombinasyonlar.add(f"_{temiz[:3]}")
    kombinasyonlar.add(f".{temiz[:3]}")
    kombinasyonlar.add(f"{temiz[:3]}x")
    kombinasyonlar.add(f"x{temiz[:3]}")
    kombinasyonlar.add(f"{temiz[:3]}z")
    
    return sorted(list(set(kombinasyonlar)), key=len)

# Arayüz İşleyişi
if mod == "1. Tek Kelime Akilli Arama":
    aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")
    if aranan:
        adaylar = filtreleri_uygula(kombinasyon_uret(aranan))
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"'{aranan}' icin filtrelenmis toplam {len(sonuclar)} adet hesap hazirlandi!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("Tum Linkleri .TXT Olarak Indir", txt_icerigi, file_name=f"poyraz_ai_{aranan}.txt", mime="text/plain")
        st.text_area("Toplu Kopyalama Alani:", txt_icerigi, height=200)
        
        with st.expander("Sonuclari Goster", expanded=False):
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

elif mod == "2. Iki Kelime Birlestirici (Name Mixer)":
    c1, c2 = st.columns(2)
    with c1: k1 = st.text_input("Birinci Kelime (Ad):")
    with c2: k2 = st.text_input("Ikinci Kelime (Soyad):")
    
    if k1 and k2:
        adaylar = filtreleri_uygula(mixer_uret(k1, k2))
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"Harmanlanmis toplam {len(sonuclar)} adet hesap hazirlandi!")
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("Linkleri .TXT Olarak Indir", txt_icerigi, file_name=f"poyraz_ai_mixer.txt", mime="text/plain")
        st.text_area("Toplu Kopyalama Alani:", txt_icerigi, height=200)
        
        with st.expander("Sonuclari Goster", expanded=True):
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

elif mod == "3. Dogum Yili / Yas Kombinasyonlari":
    c1, c2 = st.columns(2)
    with c1: isim = st.text_input("Isim veya Kelime:")
    with c2: dogum_yili = st.text_input("Dogum Yili (Orn: 2005):", value="2005")
    
    if isim and dogum_yili:
        adaylar = filtreleri_uygula(yil_uret(isim, dogum_yili))
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"Dogum yilli toplam {len(sonuclar)} adet hesap hazirlandi!")
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("Linkleri .TXT Olarak Indir", txt_icerigi, file_name=f"poyraz_ai_yil.txt", mime="text/plain")
        st.text_area("Toplu Kopyalama Alani:", txt_icerigi, height=200)
        
        with st.expander("Sonuclari Goster", expanded=True):
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

else: # Ultra Kısa / Nadir İsimler
    kisa_isim = st.text_input("Kisa / Nadir Isim Uretmek Icin Kelime Girin:")
    if kisa_isim:
        adaylar = filtreleri_uygula(kisa_uret(kisa_isim))
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"Ultra kisa nadir toplam {len(sonuclar)} adet hesap hazirlandi!")
        txt_icerigi = "\n".join(sonuclar)
        st.download_button("Linkleri .TXT Olarak Indir", txt_icerigi, file_name=f"poyraz_ai_kisa.txt", mime="text/plain")
        st.text_area("Toplu Kopyalama Alani:", txt_icerigi, height=200)
        
        with st.expander("Sonuclari Goster", expanded=True):
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

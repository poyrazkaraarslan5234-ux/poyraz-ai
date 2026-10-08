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

# Mod Seçimi (Tek Kelime vs Kelime Birlestirici)
mod = st.radio("Arama Modunu Seç:", ["Tek Kelime Akilli Arama", "Iki Kelime Birlestirici (Name Mixer)"], horizontal=True)

# Müsaitlik Tahmin Fonksiyonu (Heuristic)
def musaitlik_tahmini(kullanici_adi):
    # Çok uzun, rastgele sayı içeren veya karmaşık isimlerin boşta olma ihtimali yüksektir
    if len(kullanici_adi) > 12 or "_" in kullanici_adi or "." in kullanici_adi or any(c.isdigit() for c in kullanici_adi):
        return "Bosta Olabilir", "badge-free"
    else:
        return "Alinmis Olabilir", "badge-taken"

# Kombinasyon Üreten Fonksiyon (Tek Kelime)
@st.cache_data
def kombinasyon_uret(kelime):
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

    # Alttan çizgi ve nokta
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

    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# Kombinasyon Üreten Fonksiyon (İki Kelime Birlestirici)
@st.cache_data
def mixer_uret(kelime1, kelime2):
    k1 = kelime1.lower().strip().replace(" ", "")
    k2 = kelime2.lower().strip().replace(" ", "")
    if not k1 or not k2:
        return []
        
    kombinasyonlar = set()
    
    # Hibrit Birleşimler
    kombinasyonlar.add(f"{k1}{k2}")
    kombinasyonlar.add(f"{k1}_{k2}")
    kombinasyonlar.add(f"{k1}.{k2}")
    kombinasyonlar.add(f"{k2}{k1}")
    kombinasyonlar.add(f"{k2}_{k1}")
    
    # Kısa kesitli birleşimler
    if len(k1) > 3 and len(k2) > 3:
        kombinasyonlar.add(f"{k1[:3]}{k2}")
        kombinasyonlar.add(f"{k1}{k2[:3]}")
        kombinasyonlar.add(f"{k1[:3]}_{k2}")
        kombinasyonlar.add(f"{k1}_{k2[:3]}")

    # Sayılı ekler
    for ek in ["34", "35", "06", "52", "99", "2026", "official", "real"]:
        kombinasyonlar.add(f"{k1}{k2}{ek}")
        kombinasyonlar.add(f"{k1}_{k2}_{ek}")
        kombinasyonlar.add(f"{k1}.{k2}.{ek}")

    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# Arayüz Mantığı
if mod == "Tek Kelime Akilli Arama":
    aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")
    if aranan:
        adaylar = kombinasyon_uret(aranan)
        
        st.markdown("### Filtreleme")
        filtre = st.radio("Gorunum Sec:", ["Tumu", "Sadece Cizgili/Noktali", "Sadece Sayili"], horizontal=True)
        
        filtrelenmis = []
        for k in adaylar:
            if filtre == "Sadece Cizgili/Noktali" and ("_" in k or "." in k):
                filtrelenmis.append(k)
            elif filtre == "Sadece Sayili" and any(c.isdigit() for c in k):
                filtrelenmis.append(k)
            elif filtre == "Tumu":
                filtrelenmis.append(k)
                
        if not filtrelenmis:
            filtrelenmis = adaylar
            
        sonuclar = [f"https://www.instagram.com/{k}/" for k in filtrelenmis]
        st.success(f"'{aranan}' icin toplam {len(sonuclar)} adet hesap hazirlandi!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button(
            label="Tum Linkleri .TXT Olarak Indir",
            data=txt_icerigi,
            file_name=f"poyraz_ai_{aranan}_varyasyonlar.txt",
            mime="text/plain"
        )

        st.markdown("### Toplu Kopyalama Alani")
        st.text_area("Tum sonuclari buradan kopyalayabilirsin:", txt_icerigi, height=200)
        
        st.markdown(f"### Instagram Profil Kartlari ({len(sonuclar)} Adet)")
        with st.expander("Tum Listeyi Ekranda Gor (Tıkla Aç)", expanded=False):
            for k, url in zip(filtrelenmis, sonuclar):
                durum, sinif = musaitlik_tahmini(k)
                st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-ring">
                            <div class="profile-inner">👤</div>
                        </div>
                        <div class="profile-info">
                            <a class="profile-name" href="{url}" target="_blank">@{k}</a>
                            <span class="{sinif}">Tahmini Durum: {durum}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

else: # İki Kelime Birleştirici (Name Mixer)
    col1, col2 = st.columns(2)
    with col1:
        kelime1 = st.text_input("Birinci Kelime (Örn: adın):")
    with col2:
        kelime2 = st.text_input("İkinci Kelime (Örn: soyadın):")
        
    if kelime1 and kelime2:
        adaylar = mixer_uret(kelime1, kelime2)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
        st.success(f"'{kelime1}' ve '{kelime2}' harmanlanarak toplam {len(sonuclar)} adet hibrit hesap üretildi!")
        
        txt_icerigi = "\n".join(sonuclar)
        st.download_button(
            label="Harmanlanmış Linkleri .TXT Olarak İndir",
            data=txt_icerigi,
            file_name=f"poyraz_ai_mixer_{kelime1}_{kelime2}.txt",
            mime="text/plain"
        )

        st.markdown("### Toplu Kopyalama Alanı")
        st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
        
        st.markdown(f"### Harmanlanmış Profil Kartları ({len(sonuclar)} Adet)")
        with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=True):
            for k, url in zip(adaylar, sonuclar):
                durum, sinif = musaitlik_tahmini(k)
                st.markdown(f"""
                    <div class="profile-card">
                        <div class="profile-ring">
                            <div class="profile-inner">👤</div>
                        </div>
                        <div class="profile-info">
                            <a class="profile-name" href="{url}" target="_blank">@{k}</a>
                            <span class="{sinif}">Tahmini Durum: {durum}</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

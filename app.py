import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# --- YAN MENÜ (ÖZELLEŞTİRME VE KATEGORİLER) ---
st.sidebar.header("⚙ Gelişmiş Ayarlar")

kategori = st.sidebar.selectbox(
    "🎯 Hazır Kategori Seç",
    ["Özel / Manuel", "🎮 Oyuncu (Gamer)", "🎵 Müzisyen / Sanatçı", "💼 İşletme / Store", "🔥 Popüler / Global"]
)

default_ekler = "official, real, tr, 34, 52"
if kategori == "🎮 Oyuncu (Gamer)":
    default_ekler = "gaming, esports, 777, tv, twitch, nrg, pro, x"
elif kategori == "🎵 Müzisyen / Sanatçı":
    default_ekler = "music, sound, beat, prod, live, official, art"
elif kategori == "💼 İşletme / Store":
    default_ekler = "store, shop, global, tr, official, corp, market"
elif kategori == "🔥 Popüler / Global":
    default_ekler = "real, official, 99, 07, 35, x, z, the, style"

secilen_uzunluk = st.sidebar.slider("Sayısal Ek Sınırı (0 ile X arası)", 10, 150, 40)
ozel_ek_giris = st.sidebar.text_input("Özel Eklerin (Virgülle ayır)", default_ekler)

konum_secimi = st.sidebar.radio(
    "📍 Kombinasyon Konumu",
    ["Tümü (Başa, Sona ve Ortaya)", "Sadece Kelimenin Başına", "Sadece Kelimenin Sonuna"]
)

# Kombinasyon Üreten Fonksiyon (Tüm olası varyasyonlar)
def kombinasyon_uret(kelime, max_sayi, ek_listesi, konum):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    on_ekler = ["", "_", ".", "__", "._", "_.", "x", "z", "i", "the", "real", "official", "pro", "m"]
    
    arka_ekler = [""]
    for i in range(max_sayi):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ekstra_ekler = [e.strip() for e in ek_listesi.split(",") if e.strip()]
    ozel_ekler = [
        "11", "21", "34", "35", "52", "07", "53", "61", "06", "99", 
        "123", "333", "007", "1903", "1905", "1907", "2023", "2024", "2025", "2026",
        "tc", "bey", "hanim", "s", "pro", "x", "z", "b", "jr",
        "insta", "gram", "profil", "hesap", "corp", "store", "tv"
    ] + ekstra_ekler
    
    arka_ekler.extend(ozel_ekler)
    
    kombinasyonlar = set()
    
    for on in on_ekler:
        for arka in arka_ekler:
            if konum == "Tümü (Başa, Sona ve Ortaya)":
                kombinasyonlar.add(f"{on}{temiz}{arka}")
                kombinasyonlar.add(f"{on}{temiz}_{arka}")
                kombinasyonlar.add(f"{on}{temiz}.{arka}")
                kombinasyonlar.add(f"{on}{temiz}__{arka}")
                kombinasyonlar.add(f"{arka}{temiz}{on}")
                kombinasyonlar.add(f"{arka}_{temiz}{on}")
                kombinasyonlar.add(f"{arka}.{temiz}{on}")
            elif konum == "Sadece Kelimenin Başına":
                kombinasyonlar.add(f"{arka}{temiz}")
                kombinasyonlar.add(f"{arka}_{temiz}")
                kombinasyonlar.add(f"{arka}.{temiz}")
            elif konum == "Sadece Kelimenin Sonuna":
                kombinasyonlar.add(f"{temiz}{arka}")
                kombinasyonlar.add(f"{temiz}_{arka}")
                kombinasyonlar.add(f"{temiz}.{arka}")

    # Önce en kısa olanlar (az ek alanlar), sonra uzun olanlar sıralansın
    return sorted(list(kombinasyonlar), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Tüm varyasyonlar üretiliyor ve sıralanıyor...'):
        adaylar = kombinasyon_uret(aranan, secilen_uzunluk, ozel_ek_giris, konum_secimi)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
    st.success(f"**'{aranan}'** için olabilecek tüm **{len(sonuclar)}** varyasyon en kısadan uzuna hazırlandı!")
    
    # 1. Dosya İndirme Butonu (.txt olarak)
    txt_icerigi = "\n".join(sonuclar)
    st.download_button(
        label="📥 Tüm Linkleri .TXT Olarak İndir",
        data=txt_icerigi,
        file_name=f"poyraz_ai_{aranan}_kombinasyonlar.txt",
        mime="text/plain"
    )

    # 2. Toplu Kopyalama Alanı
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Tüm sonuçları buradan tek hareketle kopyalayabilirsin:", txt_icerigi, height=150)
    
    # 3. Önizleme Listesi
    st.markdown("### 🔗 Profil Linkleri Önizlemesi")
    for url in sonuclar:
        st.markdown(f"- [{url}]({url})")

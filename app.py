import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# --- YAN MENÜ (ÖZELLEŞTİRME VE KATEGORİLER) ---
st.sidebar.header("⚙️️ Gelişmiş Ayarlar")

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

# Kasma yapmaması için slider sınırını ideal düzeyde tutuyoruz
secilen_uzunluk = st.sidebar.slider("Sayısal Ek Sınırı (0 ile X arası)", 10, 100, 30)
ozel_ek_giris = st.sidebar.text_input("Özel Eklerin (Virgülle ayır)", default_ekler)

konum_secimi = st.sidebar.radio(
    "📍 Kombinasyon Konumu",
    ["Tümü (Başa, Sona ve Ortaya)", "Sadece Kelimenin Başına", "Sadece Kelimenin Sonuna"]
)

# Kombinasyon Üreten Fonksiyon
def kombinasyon_uret(kelime, max_sayi, ek_listesi, konum):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    on_ekler = ["", "_", ".", "x", "z", "i", "real", "pro"]
    
    arka_ekler = [""]
    for i in range(max_sayi):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ekstra_ekler = [e.strip() for e in ek_listesi.split(",") if e.strip()]
    ozel_ekler = ["11", "34", "35", "52", "07", "61", "06", "99", "123", "tc", "bey", "pro", "store", "tv"] + ekstra_ekler
    arka_ekler.extend(ozel_ekler)
    
    kombinasyonlar = set()
    
    for on in on_ekler:
        for arka in arka_ekler:
            if konum == "Tümü (Başa, Sona ve Ortaya)":
                kombinasyonlar.add(f"{on}{temiz}{arka}")
                kombinasyonlar.add(f"{on}{temiz}_{arka}")
                kombinasyonlar.add(f"{arka}{temiz}{on}")
            elif konum == "Sadece Kelimenin Başına":
                kombinasyonlar.add(f"{arka}{temiz}")
                kombinasyonlar.add(f"{arka}_{temiz}")
            elif konum == "Sadece Kelimenin Sonuna":
                kombinasyonlar.add(f"{temiz}{arka}")
                kombinasyonlar.add(f"{temiz}_{arka}")

    return sorted(list(kombinasyonlar), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Varyasyonlar üretiliyor...'):
        adaylar = kombinasyon_uret(aranan, secilen_uzunluk, ozel_ek_giris, konum_secimi)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
    st.success(f"**'{aranan}'** için toplam **{len(sonuclar)}** varyasyon hızlıca hazırlandı!")
    
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
    
    # 3. Hafifletilmiş Önizleme Listesi (Kasma yapmaz)
    st.markdown("### 🔗 Profil Linkleri Önizlemesi (En Temizler)")
    for url in sonuclar[:150]:
        st.markdown(f"- [{url}]({url})")
        
    if len(sonuclar) > 150:
        st.info("💡 Telefonunun yağ gibi akması için ilk 150 sonuç gösteriliyor. Tüm arşivi indirmek için yukarıdaki **.TXT İndir** butonunu kullanabilirsin!")

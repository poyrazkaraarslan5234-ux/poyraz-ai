Kanka bahsettiğim bu harika özelliklerin arasından en kullanışlı ve siteyi en profesyonel gösterecek olanları — Hazır Kategori Butonları (Gamer, Müzisyen, Store vb.), Sadece Başa/Sona Ekleme Filtresi ve Favorilere Ekleme (Seçilenleri Kaydetme) sistemini doğrudan kodun içine entegre ettim!

Artık sol menüden kategorileri seçebilir, eklerin nereye geleceğini ayarlayabilir ve beğendiğin kullanıcı adlarını favorilere ekleyip sadece onları indirebilirsin.

İşte en güncel ve dolu dolu olan app.py kodun:

Python
import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# --- YAN MENÜ (ÖZELLEŞTİRME VE KATEGORİLER) ---
st.sidebar.header("⚙️ Gelişmiş Ayarlar")

# 1. Hazır Kategori Seçimi
kategori = st.sidebar.selectbox(
    "🎯 Hazır Kategori Seç (Özel Ekler Otomatik Eklenir)",
    ["Özel / Manuel", "🎮 Oyuncu (Gamer)", "🎵 Müzisyen / Sanatçı", "💼 İşletme / Store", "🔥 Popüler / Global"]
)

# Kategoriye göre otomatik özel ekler belirleyelim
default_ekler = "official, real, tr, 34, 52"
if kategori == "🎮 Oyuncu (Gamer)":
    default_ekler = "gaming, esports, 777, tv, twitch, nrg, pro, x"
elif kategori == "🎵 Müzisyen / Sanatçı":
    default_ekler = "music, sound, beat, prod, live, official, art"
elif kategori == "💼 İşletme / Store":
    default_ekler = "store, shop, global, tr, official, corp, market"
elif kategori == "🔥 Popüler / Global":
    default_ekler = "real, official, 99, 07, 35, x, z, the, style"

secilen_uzunluk = st.sidebar.slider("Sayısal Ek Sınırı (0 ile X arası)", 10, 300, 50)
ozel_ek_giris = st.sidebar.text_input("Özel Eklerin (Virgülle ayır)", default_ekler)

# 2. Ekleme Konumu Filtresi
konum_secimi = st.sidebar.radio(
    "📍 Kombinasyon Konumu",
    ["Tümü (Başa, Sona ve Ortaya)", "Sadece Kelimenin Başına", "Sadece Kelimenin Sonuna"]
)

# Kombinasyon Üreten Fonksiyon
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
    sirali_liste = sorted(list(kombinasyonlar), key=len)
    return sirali_liste

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Varyasyonlar üretiliyor ve sıralanıyor...'):
        adaylar = kombinasyon_uret(aranan, secilen_uzunluk, ozel_ek_giris, konum_secimi)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
    st.success(f"**'{aranan}'** için toplam **{len(sonuclar)}** varyasyon oluşturuldu!")
    
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
    st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=150)
    
    # 3. Favorilere Ekleme ve Link Listesi
    st.markdown("### 🔗 Profil Linkleri ve Favoriler")
    st.info("💡 Beğendiğin linkleri seçerek kendine özel favori listesi oluşturabilirsin.")

    # Session state ile favorileri hafızada tutalım
    if "favoriler" not in st.session_state:
        st.session_state.favoriler = []

    # Her link için bir checkbox (favori ekleme) koyalım
    secilenler = []
    for url in sonuclar:
        col1, col2 = st.columns([0.1, 0.9])
        with col1:
            is_fav = st.checkbox("⭐", key=f"fav_{url}", label_visibility="collapsed")
            if is_fav and url not in st.session_state.favoriler:
                st.session_state.favoriler.append(url)
        with col2:
            st.markdown(f"[{url}]({url})")

    # Eğer favoriye eklenenler varsa alt tarafta gösterelim ve ayrı indirelim
    if st.session_state.favoriler:
        st.markdown("---")
        st.markdown(f"### ⭐ Favori Listem ({len(st.session_state.favoriler)} Seçildi)")
        fav_icerigi = "\n".join(st.session_state.favoriler)
        st.text_area("Seçtiğin favori linkler:", fav_icerigi, height=100)
        st.download_button(
            label="📥 Favorileri .TXT Olarak İndir",
            data=fav_icerigi,
            file_name=f"poyraz_ai_favoriler.txt",
            mime="text/plain"
        )

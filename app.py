import streamlit as st
import requests

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Boşta Kullanıcı Adı Bulucu")

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

secilen_uzunluk = st.sidebar.slider("Sayısal Ek Sınırı (0 ile X arası)", 10, 80, 25)
ozel_ek_giris = st.sidebar.text_input("Özel Eklerin (Virgülle ayır)", default_ekler)

konum_secimi = st.sidebar.radio(
    "📍 Kombinasyon Konumu",
    ["Tümü (Başa, Sona ve Ortaya)", "Sadece Kelimenin Başına", "Sadece Kelimenin Sonuna"]
)

# Sadece boşta olanları tarama seçeneği
sadece_bostan_sec = st.sidebar.checkbox("🟢 Sadece Boşta Olanları Tara (Müsait Hesaplar)", value=False)

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

# Instagram Hesap Müsaitlik Kontrol Fonksiyonu
def hesap_bosta_mi(kullanici_adi):
    url = f"https://www.instagram.com/{kullanici_adi}/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        response = requests.get(url, headers=headers, timeout=3)
        # Eğer sayfa 404 dönüyorsa o kullanıcı adı Instagram'da yoktur (yani boştadır!)
        if response.status_code == 404:
            return True
    except:
        pass
    return False

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Varyasyonlar üretiliyor...'):
        adaylar = kombinasyon_uret(aranan, secilen_uzunluk, ozel_ek_giris, konum_secimi)
        
    # Eğer kullanıcı "Sadece Boşta Olanları Tara" seçeneğini seçtiyse filtreleyelim
    if sadece_bostan_sec:
        st.warning("⚠️ Canlı tarama modu aktif! Müsait hesaplar kontrol ediliyor, bu işlem birkaç saniye sürebilir...")
        bos_olanlar = []
        progress_bar = st.progress(0)
        total = len(adaylar)
        
        for idx, k in enumerate(adaylar[:50]): # Performans için ilk 50 adayı tarayalım
            if hesap_bosta_mi(k):
                bos_olanlar.append(k)
            progress_bar.progress((idx + 1) / min(total, 50))
            
        adaylar = bos_olanlar
        st.success(f"🎯 Tarama tamamlandı! Boşta olan toplam **{len(adaylar)}** hesap bulundu.")
    else:
        st.success(f"**'{aranan}'** için toplam **{len(adaylar)}** varyasyon hazırlandı!")

    sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
    
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

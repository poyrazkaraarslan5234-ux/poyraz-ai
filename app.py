import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# --- YAN MENÜ (ÖZELLEŞTİRME AYARLARI) ---
st.sidebar.header("⚙️ Gelişmiş Ayarlar")
secilen_uzunluk = st.sidebar.slider("Sayısal Ek Sınırı (0 ile X arası)", 10, 500, 100)
ozel_ek_giris = st.sidebar.text_input("Özel Eklerin (Virgülle ayır)", "official, real, tr, 34, 52")

# Kombinasyon Üreten Fonksiyon
def kombinasyon_uret(kelime, max_sayi, ek_listesi):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    on_ekler = ["", "_", ".", "__", "._", "_.", "x", "z", "i", "the", "real", "official", "pro", "m"]
    
    arka_ekler = [""]
    for i in range(max_sayi):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    # Kullanıcının sidebar'dan girdiği özel ekleri de listeye ekleyelim
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
            kombinasyonlar.add(f"{on}{temiz}{arka}")
            kombinasyonlar.add(f"{on}{temiz}_{arka}")
            kombinasyonlar.add(f"{on}{temiz}.{arka}")
            kombinasyonlar.add(f"{on}{temiz}__{arka}")
            kombinasyonlar.add(f"{arka}{temiz}{on}")
            kombinasyonlar.add(f"{arka}_{temiz}{on}")
            kombinasyonlar.add(f"{arka}.{temiz}{on}")

    return sorted(list(kombinasyonlar))

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Varyasyonlar üretiliyor...'):
        adaylar = kombinasyon_uret(aranan, secilen_uzunluk, ozel_ek_giris)
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

    # 2. Tek Tuşla Kopyalanabilir Metin Kutusu
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Aşağıdaki kutudan tüm sonuçları tek hareketle kopyalayabilirsin:", txt_icerigi, height=150)
    
    # Sonuçları Link Olarak Gösterme
    st.markdown("### 🔗 Profil Linkleri Önizlemesi")
    for url in sonuclar:
        st.markdown(f"- [{url}]({url})")

import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# Kombinasyon Üreten Fonksiyon (Optimize Edilmiş Versiyon)
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    # Önekler
    on_ekler = ["", "_", ".", "x", "z", "i", "the", "real", "official", "pro"]
    
    # Sonekler ve Sayılar (0-200 arası - performans için ideal)
    arka_ekler = [""]
    for i in range(200):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    # Soyisim ve Popüler Ekler
    ekler = [
        "yilmaz", "kaya", "demir", "celik", "yildiz", "yildirim", "ozturk", "aydin", "ozdemir",
        "34", "35", "52", "06", "07", "61", "99",
        "2024", "2025", "2026",
        "tc", "bey", "hanim", "pro", "x", "z", "insta", "gram", "store", "tv", "official", "real", "tr"
    ]
    arka_ekler.extend(ekler)
    
    kombinasyonlar = set()
    
    for on in on_ekler:
        for arka in arka_ekler:
            if not on and not arka:
                continue
            kombinasyonlar.add(f"{on}{temiz}{arka}")
            kombinasyonlar.add(f"{on}{temiz}_{arka}")
            kombinasyonlar.add(f"{on}{temiz}.{arka}")
            kombinasyonlar.add(f"{arka}{temiz}{on}")
            kombinasyonlar.add(f"{arka}_{temiz}{on}")

    return sorted(list(kombinasyonlar), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Varyasyonlar hızla hazırlanıyor...'):
        adaylar = kombinasyon_uret(aranan)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
    st.success(f"**'{aranan}'** için toplam **{len(sonuclar)}** adet varyasyon başarıyla listelendi!")
    
    # 1. Dosya İndirme Butonu (.txt olarak)
    txt_icerigi = "\n".join(sonuclar)
    st.download_button(
        label="📥 Tüm Linkleri .TXT Olarak İndir",
        data=txt_icerigi,
        file_name=f"poyraz_ai_{aranan}_varyasyonlar.txt",
        mime="text/plain"
    )

    # 2. Toplu Kopyalama Alanı
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
    
    # 3. Önizleme Listesi
    st.markdown(f"### 🔗 Profil Linkleri ({len(sonuclar)} Adet)")
    for url in sonuclar:
        st.markdown(f"- [{url}]({url})")

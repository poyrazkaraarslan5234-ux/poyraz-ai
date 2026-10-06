import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu (Tam Otomatik)")

# Kombinasyon Üreten Fonksiyon (Tüm olası varyasyonlar)
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    # Genişletilmiş Önekler (Başa gelebilecekler)
    on_ekler = [
        "", "_", ".", "__", "._", "_.", "x", "z", "i", "the", "real", 
        "official", "pro", "m", "mr", "mrs", "dr", "the_", "i_", "my"
    ]
    
    # Genişletilmiş Sonekler ve Sayılar (Sona gelebilecekler)
    arka_ekler = [""]
    
    # 0'dan 999'a kadar tüm sayılar ve varyasyonları
    for i in range(1000):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        arka_ekler.append(f"__{i}")
        
    # Özel ve Popüler Ekler Listesi
    ozel_ekler = [
        # Şehir / Bölge kodları
        "01", "06", "07", "10", "16", "21", "26", "34", "35", "38", "41", "42", "52", "53", "54", "55", "61", "67", "77", "99",
        # Yıllar
        "2000", "2001", "2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", 
        "2010", "2011", "2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", 
        "2020", "2021", "2022", "2023", "2024", "2025", "2026",
        # Unvanlar, takılar ve kelimeler
        "tc", "bey", "hanim", "hs", "s", "pro", "x", "z", "b", "jr", "sr",
        "insta", "gram", "profil", "hesap", "corp", "store", "tv", "official", 
        "real", "tr", "turkey", "az", "global", "net", "com", "hq", "xx", "zz",
        "gaming", "esports", "music", "sound", "beat", "prod", "live", "art",
        "team", "cl", "club", "fan", "fc", "original", "vip", "sec", "private"
    ]
    
    arka_ekler.extend(ozel_ekler)
    
    kombinasyonlar = set()
    
    for on in on_ekler:
        for arka in arka_ekler:
            # Sadece tek başına boş olmasınlar diye kontrol
            if not on and not arka:
                continue
                
            kombinasyonlar.add(f"{on}{temiz}{arka}")
            kombinasyonlar.add(f"{on}{temiz}_{arka}")
            kombinasyonlar.add(f"{on}{temiz}.{arka}")
            kombinasyonlar.add(f"{on}{temiz}__{arka}")
            kombinasyonlar.add(f"{arka}{temiz}{on}")
            kombinasyonlar.add(f"{arka}_{temiz}{on}")
            kombinasyonlar.add(f"{arka}.{temiz}{on}")

    # En kısa ve en mantıklı olanlardan, en uzunlara doğru sıralama
    return sorted(list(kombinasyonlar), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    with st.spinner('Yüz binlerce olası varyasyon hesaplanıyor ve sıralanıyor...'):
        adaylar = kombinasyon_uret(aranan)
        sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
        
    st.success(f"**'{aranan}'** için **{len(sonuclar)}** adet olası varyasyon başarıyla üretildi!")
    
    # 1. Dosya İndirme Butonu (.txt olarak)
    txt_icerigi = "\n".join(sonuclar)
    st.download_button(
        label="📥 Tüm Linkleri .TXT Olarak İndir",
        data=txt_icerigi,
        file_name=f"poyraz_ai_{aranan}_tum_varyasyonlar.txt",
        mime="text/plain"
    )

    # 2. Toplu Kopyalama Alanı
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Tüm sonuçları buradan tek hareketle kopyalayabilirsin:", txt_icerigi, height=150)
    
    # 3. Önizleme Listesi
    st.markdown("### 🔗 Profil Linkleri Önizlemesi (İlk 100 Tane)")
    for url in sonuclar[:100]:
        st.markdown(f"- [{url}]({url})")
        
    if len(sonuclar) > 100:
        st.info(f"Performans için ilk 100 tanesi gösteriliyor. Kalan {len(sonuclar) - 100} varyasyonu .TXT olarak indirebilir veya toplu kopyalama alanından alabilirsin.")

import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu (Gelişmiş Sürüm)")

# Kombinasyon Üreten Fonksiyon (Filtreler ve Leet Speak Dahil)
@st.cache_data
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    kombinasyonlar = set()
    
    # 1. Ek almamış ham ve saf hali
    kombinasyonlar.add(temiz)
    
    # 2. Leet Speak / Harf Çarpıtma (Örn: a->4/@, e->3, i->1, o->0, s->5)
    def leet_yap(text):
        cevirim = text.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '5')
        return cevirim
    
    if leet_yap(temiz) != temiz:
        kombinasyonlar.add(leet_yap(temiz))

    # 3. Harf Ekleme / Çoğaltma
    if len(temiz) > 0:
        ilk_harf = temiz[0]
        son_harf = temiz[-1]
        kombinasyonlar.add(ilk_harf + temiz)          
        kombinasyonlar.add(temiz + son_harf)          
        kombinasyonlar.add(ilk_harf + ilk_harf + temiz[1:]) 
        kombinasyonlar.add(temiz[:-1] + son_harf + son_harf) 
        
        for i in range(len(temiz)):
            eklenmis = temiz[:i] + temiz[i] + temiz[i:]
            kombinasyonlar.add(eklenmis)

    # 4. Harf Eksiltme
    if len(temiz) > 2:
        for i in range(len(temiz)):
            eksik_kelime = temiz[:i] + temiz[i+1:]
            kombinasyonlar.add(eksik_kelime)

    # 5. Harf aralarına alttan çizgi
    if len(temiz) > 1:
        for i in range(1, len(temiz)):
            harf_aralari_alt = temiz[:i] + "_" + temiz[i:]
            kombinasyonlar.add(harf_aralari_alt)
        
        tam_cizgili = "_".join(list(temiz))
        kombinasyonlar.add(tam_cizgili)

    on_ekler = ["", "_", ".", "x", "z", "real", "official"]
    
    arka_ekler = [""]
    for i in range(100):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ekler = [
        "yilmaz", "kaya", "demir", "celik", "yildiz", "ozturk", "aydin",
        "34", "35", "52", "06", "07", "61", "99",
        "2025", "2026", "tc", "bey", "pro", "x", "z", "insta", "store", "tv"
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

    # Instagram 30 karakter sınırı filtresi (30 karakterden uzunları eler)
    gecerli_kombinasyonlar = [k for k in kombinasyonlar if len(k) <= 30]

    return sorted(list(set(gecerli_kombinasyonlar)), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    adaylar = kombinasyon_uret(aranan)
    
    # 3. Kategori Filtreleme Menüsü
    st.markdown("### 🎛️ Filtreleme Seçenekleri")
    filtre_tipi = st.radio(
        "Görmek istediğin kategoriyi seç:",
        ["Tümü", "Sadece Alttan Çizgili / Noktalı", "Sadece Sayılı / Yılllı", "Sadece Ham ve Temiz Haller"],
        horizontal=True
    )
    
    # Filtreleme Mantığı
    filtrelenmis_adaylar = []
    for k in adaylar:
        if filtre_tipi == "Sadece Alttan Çizgili / Noktalı":
            if "_" in k or "." in k:
                filtrelenmis_adaylar.append(k)
        elif filtre_tipi == "Sadece Sayılı / Yılllı":
            if any(char.isdigit() for char in k):
                filtrelenmis_adaylar.append(k)
        elif filtre_tipi == "Sadece Ham ve Temiz Haller":
            if k == aranan.lower().strip().replace(" ", "") or len(k) <= len(aranan) + 2:
                filtrelenmis_adaylar.append(k)
        else:
            filtrelenmis_adaylar.append(k)
            
    sonuclar = [f"https://www.instagram.com/{k}/" for k in filtrelenmis_adaylar]
    
    st.success(f"**'{aranan}'** için seçilen filtreye göre toplam **{len(sonuclar)}** adet hesap hazırlandı!")
    
    # 1. Dosya İndirme Butonu (.txt olarak)
    txt_icerigi = "\n".join(sonuclar)
    st.download_button(
        label="📥 Bu Listeyi .TXT Olarak İndir",
        data=txt_icerigi,
        file_name=f"poyraz_ai_{aranan}_varyasyonlar.txt",
        mime="text/plain"
    )

    # 4. Favori / Beğenilenleri Seçme Paneli
    st.markdown("### ⭐ Favori Adayları Seç")
    secilenler = st.multiselect("Gözüne kestirdiğin kullanıcı adlarını buradan işaretle:", filtrelenmis_adaylar)
    
    if secilenler:
        st.info("Seçtiğin favori hesaplar:")
        for secim in secilenler:
            st.markdown(f"- [https://www.instagram.com/{secim}/](https://www.instagram.com/{secim}/)")

    # 2. Toplu Kopyalama Alanı
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
    
    # 3. Önizleme Listesi
    st.markdown(f"### 🔗 Profil Linkleri ({len(sonuclar)} Adet)")
    with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=False):
        for url in sonuclar:
            st.markdown(f"- [{url}]({url})")

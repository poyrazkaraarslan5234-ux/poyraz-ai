import streamlit as st

# Sayfa Ayarları
st.set_page_config(page_title="Poyraz AI - Instagram Hesap Bulucu", page_icon="🔍", layout="centered")

# Arayüz Tasarımı
st.title("🚀 Poyraz AI")
st.subheader("Instagram Akıllı Hesap ve Varyasyon Bulucu")

# Kombinasyon Üreten Fonksiyon
@st.cache_data
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    kombinasyonlar = set()
    
    # 1. Ek almamış ham ve saf hali
    kombinasyonlar.add(temiz)
    
    # 2. Herhangi bir harfi eksik yazma / harf düşürme varyasyonları (örn: poyraz yerine poyaz vb.)
    if len(temiz) > 2:
        for i in range(len(temiz)):
            eksik_kelime = temiz[:i] + temiz[i+1:]
            kombinasyonlar.add(eksik_kelime)

    # 3. Harf Tekrarları ve İkilemeler (örn: ppoyraz, poyrazz, ppoyrazkaraarslann)
    if len(temiz) > 0:
        ilk_harf = temiz[0]
        son_harf = temiz[-1]
        kombinasyonlar.add(ilk_harf + temiz)          
        kombinasyonlar.add(temiz + son_harf)          
        kombinasyonlar.add(ilk_harf + ilk_harf + temiz[1:]) 
        kombinasyonlar.add(temiz[:-1] + son_harf + son_harf) 

    # 4. Harflerin arasına tek tek alttan çizgi koyma (örn: p_o_y_r_a_z)
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

    return sorted(list(kombinasyonlar), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    adaylar = kombinasyon_uret(aranan)
    sonuclar = [f"https://www.instagram.com/{k}/" for k in adaylar]
    
    st.success(f"**'{aranan}'** için eksik harf varyasyonları, tekrarlar ve çizgiler dahil toplam **{len(sonuclar)}** adet hesap hazırlandı!")
    
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

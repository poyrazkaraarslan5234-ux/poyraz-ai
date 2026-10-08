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
    
    # 1. Ham ve saf hali
    kombinasyonlar.add(temiz)
    
    # 2. Leet Speak (Örn: a->4, e->3, i->1, o->0, s->5)
    leet = temiz.replace('a', '4').replace('e', '3').replace('i', '1').replace('o', '0').replace('s', '5')
    if leet != temiz:
        kombinasyonlar.add(leet)

    # 3. Harf Ekleme / Çoğaltma
    if len(temiz) > 0:
        ilk = temiz[0]
        son = temiz[-1]
        kombinasyonlar.add(ilk + temiz)          
        kombinasyonlar.add(temiz + son)          
        kombinasyonlar.add(ilk + ilk + temiz[1:]) 
        kombinasyonlar.add(temiz[:-1] + son + son) 
        
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i] + temiz[i:])

    # 4. Harf Eksiltme
    if len(temiz) > 2:
        for i in range(len(temiz)):
            kombinasyonlar.add(temiz[:i] + temiz[i+1:])

    # 5. Alttan çizgi ve noktalı ara geçişler
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

    # 30 Karakter Instagram Sınırı ve Sıralama
    gecerli = [k for k in kombinasyonlar if len(k) <= 30]
    return sorted(list(set(gecerli)), key=len)

# Ana Arama Alanı
aranan = st.text_input("Aranacak kelimeyi veya ismi girin:")

if aranan:
    adaylar = kombinasyon_uret(aranan)
    
    # Filtreleme Seçeneği
    st.markdown("### 🎛️ Filtreleme")
    filtre = st.radio("Görünüm Seç:", ["Tümü", "Sadece Çizgili/Noktalı", "Sadece Sayılı"], horizontal=True)
    
    filtrelenmis = []
    for k in adaylar:
        if filtre == "Sadece Çizgili/Noktalı" and ("_" in k or "." in k):
            filtrelenmis.append(k)
        elif filtre == "Sadece Sayılı" and any(c.isdigit() for c in k):
            filtrelenmis.append(k)
        elif filtre == "Tümü":
            filtrelenmis.append(k)
            
    if not filtrelenmis:
        filtrelenmis = adaylar
        
    sonuclar = [f"https://www.instagram.com/{k}/" for k in filtrelenmis]
    
    st.success(f"**'{aranan}'** için toplam **{len(sonuclar)}** adet hesap hazırlandı!")
    
    # Dosya İndirme Butonu
    txt_icerigi = "\n".join(sonuclar)
    st.download_button(
        label="📥 Tüm Linkleri .TXT Olarak İndir",
        data=txt_icerigi,
        file_name=f"poyraz_ai_{aranan}_varyasyonlar.txt",
        mime="text/plain"
    )

    # Toplu Kopyalama Alanı
    st.markdown("### 📋 Toplu Kopyalama Alanı")
    st.text_area("Tüm sonuçları buradan kopyalayabilirsin:", txt_icerigi, height=200)
    
    # Önizleme Listesi (Profil İkonlu Kart Görünümü)
    st.markdown(f"### 🔗 Profil Linkleri ve Avatar Kartları ({len(sonuclar)} Adet)")
    with st.expander("Tüm Listeyi Ekranda Gör (Tıkla Aç)", expanded=False):
        for k, url in zip(filtrelenmis, sonuclar):
            st.markdown(f"👤 **{k}** $\rightarrow$ [Profili Ziyaret Et]({url})")

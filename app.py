from flask import Flask, render_template_string, request

app = Flask(__name__)

# Kombinasyon üreten fonksiyonumuz
def kombinasyon_uret(kelime):
    temiz = kelime.lower().strip().replace(" ", "")
    if not temiz:
        return []
        
    on_ekler = ["", "_", ".", "__", "._", "_.", "x", "z", "i", "the", "real", "official", "pro", "m"]
    
    arka_ekler = [""]
    for i in range(100):
        arka_ekler.append(str(i))
        arka_ekler.append(f"_{i}")
        arka_ekler.append(f".{i}")
        
    ozel_ekler = [
        "11", "21", "34", "35", "52", "07", "53", "61", "06", "99", 
        "123", "333", "007", "1903", "1905", "1907", "2023", "2024", "2025", "2026",
        "tc", "official", "off", "real", "bey", "hanim", "s", "pro", "x", "z", "b", "jr",
        "insta", "gram", "profil", "hesap", "original", "corp", "store", "tv"
    ]
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

# HTML Arayüzü (Telefona ve Bilgisayara %100 Uyumlu Modern Tasarım)
HTML_SABLONU = """
<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Poyraz AI - Instagram Hesap Bulucu</title>
    <style>
        body {
            background-color: #121212;
            color: #ffffff;
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .container {
            width: 100%;
            max-width: 600px;
            background: #1e1e1e;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        }
        h1 {
            color: #0095f6;
            text-align: center;
            font-size: 24px;
            margin-bottom: 5px;
        }
        p.subtitle {
            text-align: center;
            color: #888;
            font-size: 14px;
            margin-bottom: 20px;
        }
        .form-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px;
            font-size: 16px;
            background: #2d2d2d;
            border: 1px solid #444;
            color: #white;
            border-radius: 8px;
            outline: none;
        }
        input[type="text"]:focus {
            border-color: #0095f6;
        }
        button {
            padding: 12px 20px;
            font-size: 16px;
            background: #0095f6;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background: #0077c2;
        }
        .results-box {
            background: #2d2d2d;
            border-radius: 8px;
            max-height: 400px;
            overflow-y: auto;
            padding: 10px;
        }
        .result-item {
            padding: 10px;
            border-bottom: 1px solid #3d3d3d;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .result-item:last-child {
            border-bottom: none;
        }
        a.link {
            color: #4cb5ff;
            text-decoration: none;
            word-break: break-all;
            font-family: monospace;
            font-size: 14px;
        }
        a.link:hover {
            text-decoration: underline;
        }
        .count-info {
            color: #aaa;
            font-size: 13px;
            margin-bottom: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Poyraz AI</h1>
        <p class="subtitle">Instagram Akıllı Hesap ve Varyasyon Bulucu</p>
        
        <form method="POST" class="form-group">
            <input type="text" name="kelime" placeholder="Aranacak kelimeyi veya ismi girin..." value="{{ aranan }}" required>
            <button type="submit">Ara</button>
        </form>

        {% if aranan %}
            <div class="count-info"><b>'{{ aranan }}'</b> için <b>{{ toplam }}</b> varyasyon bulundu:</div>
            <div class="results-box">
                {% for url in sonuclar %}
                    <div class="result-item">
                        <a href="{{ url }}" target="_blank" class="link">{{ url }}</a>
                    </div>
                {% endfor %}
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    sonuclar = []
    aranan = ""
    if request.method == "POST":
        aranan = request.form.get("kelime", "").strip()
        if aranan:
            adaylar = kombinasyon_uret(aranan)
            sonuclar = [f"https://www.instagram.com/{kullanici}/" for kullanici in adaylar]
            
    return render_template_string(HTML_SABLONU, sonuclar=sonuclar, aranan=aranan, toplam=len(sonuclar))

if __name__ == "__main__":
    # Yerel ağa açıyoruz ki telefonundan da bağlanabilesin!
    app.run(host="0.0.0.0", port=5000, debug=True)
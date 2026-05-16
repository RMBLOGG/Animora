# Animora Flask Website

Website anime berbasis Flask yang mengambil data dari API Animora (via Sanka Vollerei).

## Fitur
- Halaman terbaru / home
- Daftar semua anime (A–Z) dengan filter alphabet
- Pencarian anime
- Filter berdasarkan genre
- Filter berdasarkan musim
- Halaman detail anime dengan info lengkap + link download

## Cara Menjalankan

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan server
```bash
python app.py
```

### 3. Buka browser
```
http://localhost:5000
```

## Struktur Project
```
animora_flask/
├── app.py               # Flask app utama
├── requirements.txt
├── templates/
│   ├── base.html        # Layout dasar (header, footer)
│   ├── index.html       # Halaman home (terbaru)
│   ├── all_anime.html   # Semua anime A-Z
│   ├── search.html      # Halaman pencarian
│   ├── genre_list.html  # Daftar semua genre
│   ├── genre_detail.html# Anime per genre
│   ├── season_list.html # Daftar semua musim
│   ├── season_detail.html# Anime per musim
│   └── anime_detail.html# Detail + download
└── static/
    ├── css/main.css     # Stylesheet utama
    └── js/main.js       # JavaScript utama
```

## API Source
- Base URL: `https://www.sankavollerei.com/anime`
- Creator: Sanka Vollerei
- Source: Animora

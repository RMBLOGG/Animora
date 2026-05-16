from flask import Flask, render_template, request, jsonify
import requests, math

app = Flask(__name__)
BASE_URL = "https://www.sankavollerei.com/anime"
PER_PAGE = 10

def fetch(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=10)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


@app.route("/")
def index():
    import random
    data       = fetch("/kusonime/latest")
    anime_list = data.get("anime_list", [])
    rekomendasi = random.sample(anime_list, min(6, len(anime_list))) if anime_list else []
    sdata   = fetch("/kusonime/all-seasons")
    seasons = sdata.get("seasons", [])
    special_slugs = {'anime-movie','anime-ona','anime-ova','anime-special','drama'}
    regulars = [s for s in seasons if s.get("slug","") not in special_slugs][:12]
    return render_template("index.html",
        anime_list=anime_list,
        rekomendasi=rekomendasi,
        seasons=regulars,
        page_name="home")


@app.route("/all-anime")
def all_anime():
    data = fetch("/kusonime/all-anime")
    anime_list = data.get("anime_list", [])
    return render_template("all_anime.html", anime_list=anime_list, page_name="all")


@app.route("/search")
def search():
    query   = request.args.get("q", "").strip()
    page    = max(1, int(request.args.get("page", 1)))
    results = []
    total   = 0
    if query:
        data    = fetch(f"/kusonime/search/{query}")
        all_res = data.get("anime_list", [])
        total   = len(all_res)
        start   = (page - 1) * PER_PAGE
        results = all_res[start:start + PER_PAGE]
    total_pages = math.ceil(total / PER_PAGE) if total else 1
    return render_template("search.html", results=results, query=query,
                           page=page, total_pages=total_pages, total=total,
                           page_name="search")


@app.route("/genre")
def genre_list():
    data = fetch("/kusonime/all-genres")
    genres = data.get("genres", [])
    return render_template("genre_list.html", genres=genres, page_name="genre")


@app.route("/genre/<slug>")
def genre_detail(slug):
    page       = max(1, int(request.args.get("page", 1)))
    data       = fetch(f"/kusonime/genre/{slug}")
    all_anime  = data.get("anime_list", [])
    total      = len(all_anime)
    start      = (page - 1) * PER_PAGE
    anime_list = all_anime[start:start + PER_PAGE]
    total_pages = math.ceil(total / PER_PAGE) if total else 1
    genre_name  = slug.replace("-", " ").title()
    return render_template("genre_detail.html", anime_list=anime_list,
                           genre_name=genre_name, slug=slug,
                           page=page, total_pages=total_pages, total=total,
                           page_name="genre")


@app.route("/season")
def season_list():
    data = fetch("/kusonime/all-seasons")
    seasons = data.get("seasons", [])
    return render_template("season_list.html", seasons=seasons, page_name="season")


@app.route("/season/<season>/<year>")
def season_detail(season, year):
    page       = max(1, int(request.args.get("page", 1)))
    data       = fetch(f"/kusonime/season/{season}/{year}")
    all_anime  = data.get("anime_list", [])
    total      = len(all_anime)
    start      = (page - 1) * PER_PAGE
    anime_list = all_anime[start:start + PER_PAGE]
    total_pages = math.ceil(total / PER_PAGE) if total else 1
    season_name = f"{season.title()} {year}"
    return render_template("season_detail.html", anime_list=anime_list,
                           season_name=season_name,
                           page=page, total_pages=total_pages, total=total,
                           page_name="season")


@app.route("/anime/<slug>")
def anime_detail(slug):
    import random
    data    = fetch(f"/kusonime/detail/{slug}")
    detail  = data.get("detail", {})
    latest  = fetch("/kusonime/latest")
    all_new = latest.get("anime_list", [])
    new_series   = all_new[:6]
    rekomendasi  = random.sample(all_new, min(6, len(all_new)))
    return render_template("anime_detail.html", detail=detail, slug=slug,
                           new_series=new_series, rekomendasi=rekomendasi, page_name="detail")


@app.route("/tentang")
def tentang():
    return render_template("tentang.html", page_name="tentang")


@app.route("/privasi")
def privasi():
    return render_template("privasi.html", page_name="privasi")


@app.route("/disclaimer")
def disclaimer():
    return render_template("disclaimer.html", page_name="disclaimer")


@app.route("/kontak")
def kontak():
    return render_template("kontak.html", page_name="kontak")


if __name__ == "__main__":
    app.run(debug=True)

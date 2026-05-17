from flask import Flask, render_template, request
import requests, math, random

app = Flask(__name__)
BASE_URL = "https://animora-api2.vercel.app"
PER_PAGE = 10

def fetch(path):
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}


def normalize_anime_list(anime_list):
    """Normalisasi genres dari list string ke list dict {name, slug}"""
    for anime in anime_list:
        if anime.get("genres") and isinstance(anime["genres"][0], str):
            anime["genres"] = [
                {"name": g, "slug": g.lower().replace(" ", "-")}
                for g in anime["genres"]
            ]
    return anime_list

def get_page_range(page, total_pages):
    pages = []
    for p in range(1, total_pages + 1):
        if p == 1 or p == total_pages or (p >= page - 2 and p <= page + 2):
            if pages and pages[-1] != -1 and p - pages[-1] > 1:
                pages.append(-1)
            pages.append(p)
    return pages


@app.route("/")
def index():
    home_data   = fetch("/anime/home")
    anime_list  = normalize_anime_list(home_data.get("data", []))
    rekomendasi = random.sample(anime_list, min(6, len(anime_list))) if anime_list else []
    return render_template("index.html",
        anime_list=anime_list,
        rekomendasi=rekomendasi,
        page=1, total_pages=1, total=len(anime_list),
        page_range=[1],
        page_name="home")


@app.route("/all-anime")
def all_anime():
    page = max(1, request.args.get("page", 1, type=int))
    data = fetch(f"/anime/all?page={page}")
    anime_list  = normalize_anime_list(data.get("data", []))
    next_page   = data.get("next_page")
    total_pages = 4
    page_range  = get_page_range(page, total_pages)
    return render_template("all_anime.html",
        anime_list=anime_list,
        page=page, total_pages=total_pages,
        next_page=next_page,
        page_range=page_range,
        page_name="all")


@app.route("/search")
def search():
    query   = request.args.get("q", "").strip()
    page    = max(1, request.args.get("page", 1, type=int))
    results = []
    total   = 0
    total_pages = 1
    next_page   = None
    page_range  = [1]
    if query:
        data      = fetch(f"/anime/search/{query}?page={page}")
        results   = normalize_anime_list(data.get("data", []))
        next_page = data.get("next_page")
        total     = len(results)
        total_pages = page + 1 if next_page else page
        page_range  = get_page_range(page, total_pages)
    return render_template("search.html",
        results=results, query=query,
        page=page, total_pages=total_pages,
        next_page=next_page, total=total,
        page_range=page_range,
        page_name="search")


@app.route("/genre")
def genre_list():
    data   = fetch("/anime/genre-list")
    genres = data.get("data", [])
    return render_template("genre_list.html", genres=genres, page_name="genre")


@app.route("/genre/<slug>")
def genre_detail(slug):
    page        = max(1, request.args.get("page", 1, type=int))
    data        = fetch(f"/anime/genre/{slug}?page={page}")
    anime_list  = normalize_anime_list(data.get("data", []))
    next_page   = data.get("next_page")
    genre_name  = slug.replace("-", " ").title()
    total_pages = page + 1 if next_page else page
    page_range  = get_page_range(page, total_pages)
    return render_template("genre_detail.html",
        anime_list=anime_list,
        genre_name=genre_name, slug=slug,
        page=page, total_pages=total_pages,
        next_page=next_page, total=len(anime_list),
        page_range=page_range,
        page_name="genre")


@app.route("/season")
def season_list():
    data    = fetch("/anime/season-list")
    seasons = data.get("data", [])
    return render_template("season_list.html", seasons=seasons, page_name="season")


@app.route("/season/<slug>")
def season_detail(slug):
    page        = max(1, request.args.get("page", 1, type=int))
    data        = fetch(f"/anime/season/{slug}?page={page}")
    anime_list  = normalize_anime_list(data.get("data", []))
    next_page   = data.get("next_page")
    season_name = slug.replace("-", " ").title()
    total_pages = page + 1 if next_page else page
    page_range  = get_page_range(page, total_pages)
    return render_template("season_detail.html",
        anime_list=anime_list,
        season_name=season_name, slug=slug,
        page=page, total_pages=total_pages,
        next_page=next_page, total=len(anime_list),
        page_range=page_range,
        page_name="season")


@app.route("/anime/<slug>")
def anime_detail(slug):
    data   = fetch(f"/anime/detail/{slug}")
    detail = data.get("data", {})

    if detail and isinstance(detail.get("info", {}).get("genre"), str):
        genre_str = detail["info"]["genre"]
        detail["genres"] = [
            {"name": g.strip(), "slug": g.strip().lower().replace(" ", "-")}
            for g in genre_str.split(",") if g.strip()
        ]
    else:
        detail["genres"] = []

    if detail.get("info", {}).get("released_on"):
        detail["info"]["released"] = detail["info"]["released_on"]

    raw_dl = detail.get("downloads", [])
    download_links = []
    for dl in raw_dl:
        download_links.append({
            "quality": dl.get("resolution", ""),
            "links":   dl.get("links", [])
        })
    detail["download_links"] = download_links

    home_data   = fetch("/anime/home")
    all_new     = home_data.get("data", [])
    new_series  = all_new[:6]
    rekomendasi = random.sample(all_new, min(6, len(all_new)))

    for anime in all_new:
        if "genres" not in anime:
            anime["genres"] = []
        anime["genres"] = [{"name": g, "slug": g.lower().replace(" ", "-")}
                           for g in anime.get("genres", [])]

    return render_template("anime_detail.html",
        detail=detail, slug=slug,
        new_series=new_series,
        rekomendasi=rekomendasi,
        page_name="detail")


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

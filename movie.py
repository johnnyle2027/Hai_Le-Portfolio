from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "46d6370ebbec4f9a91cdfcbb9f060f5c"
BASE_URL = "https://api.themoviedb.org/3"

def get_genre_mapping():
    """Fetches the list of genres and returns a mapping of genre name to genre ID."""
    url = f"{BASE_URL}/genre/movie/list"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        genres = response.json().get("genres", [])
        return {genre["name"]: genre["id"] for genre in genres}
    return {}

def search_movies_by_genre(genre_ids):
    """Fetches movies for selected genres and returns JSON data."""
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": ",".join(map(str, genre_ids)),
        "sort_by": "popularity.desc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route("/", methods=["GET", "POST"])
def genre_page():
    genre_mapping = get_genre_mapping()
    selected_movies = []

    if request.method == "POST":
        selected_genres = request.form.getlist("genre")
        genre_ids = [genre_mapping[genre] for genre in selected_genres if genre in genre_mapping]

        if genre_ids:
            selected_movies = search_movies_by_genre(genre_ids)

    return render_template("genre.html", genres=genre_mapping.keys(), movies=selected_movies)

if __name__ == "__main__":
    app.run(debug=True)


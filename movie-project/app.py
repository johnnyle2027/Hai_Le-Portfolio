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

def search_movies_by_name(movie_name):
    """Fetches movies by name and returns JSON data."""
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": API_KEY,
        "query": movie_name,
        "sort_by": "popularity.desc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route("/genre", methods=["GET", "POST"])
def genre_page():
    genre_mapping = get_genre_mapping()
    selected_movies = []

    if request.method == "POST":
        # Get selected genres from the form
        selected_genres = request.form.getlist("genre")
        
        # Map the genre names to genre IDs
        genre_ids = [genre_mapping[genre] for genre in selected_genres if genre in genre_mapping]

        # If genre IDs are valid, fetch the movies
        if genre_ids:
            selected_movies = search_movies_by_genre(genre_ids)

    return render_template("genre.html", movies=selected_movies, genres=genres)

@app.route('/name', methods=['GET', 'POST'])
def search_by_name():
    """Handles movie name search and displays results."""
    movies = []
    
    if request.method == 'POST':
        movie_name = request.form.get('movie_name')
        if movie_name:
            movies = search_movies_by_name(movie_name)  # Fetch movies from TMDb

    return render_template('name.html', movies=movies)

def get_trending_movies():
    """Trending movies function from TMDB"""
    url=f"{BASE_URL}/trending/movie/week"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

def get_trending_shows():
    """Trending shows function from TMDB"""
    url=f"{BASE_URL}/trending/tv/week"
    params = {"api_key": API_KEY}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    return []

@app.route("/")
def index():
    movies = get_trending_movies()
    shows = get_trending_shows()
    return render_template("index.html", movies=movies, shows=shows)

genres = [
    "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime",
    "Documentary", "Drama", "Family", "Fantasy", "History", "Horror",
    "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller",
    "War", "Western", "Film-Noir", "Short", "Reality-TV"
]

if __name__ == "__main__":
    app.run(debug=True)

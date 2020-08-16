import requests
import shutil
import os.path
import pathlib
from pathlib import Path
import tkinter
from tkinter import filedialog
import time
from progress.bar import ChargingBar

BASE_IMAGE_LINK = "https://image.tmdb.org/t/p/original"
API_KEY = "4bbd5cbd9da6580bf6bda048d43d8338"
LIST_ID = "7054979"

root = tkinter.Tk()
root.withdraw()
p = Path(tkinter.filedialog.askdirectory())


def get_movies():
    url = (
        "https://api.themoviedb.org/3/list/"
        + LIST_ID
        + "?api_key="
        + API_KEY
        + "&language=en-US"
    )

    response = requests.get(url)
    list = response.json()
    movies = []
    for movie in list["items"]:
        movies.append((movie["id"], movie["title"]))

    return movies


def get_poster_links():
    movies = get_movies()
    bar = ChargingBar("Replacing movie ids with poster urls", max=len(movies))
    poster_links = []
    for movie in movies:
        url = (
            "https://api.themoviedb.org/3/movie/"
            + str(movie[0])
            + "/images?api_key="
            + API_KEY
            + "&language=en-US&include_image_language=en%2Cnull"
        )
        response = requests.get(url)
        image_links = response.json()
        poster_link = image_links["posters"][0]["file_path"]
        poster_link = BASE_IMAGE_LINK + poster_link
        poster_links.append((poster_link, movie[1].replace(":", " -")))
        bar.next()

    bar.finish()
    return poster_links


def download_posters():
    poster_links = get_poster_links()
    bar = ChargingBar("Downloading posters", max=len(poster_links))
    for poster in poster_links:
        poster_filepath = p.joinpath(poster[1] + ".jpg")
        if not os.path.isfile(poster_filepath):
            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(poster[0], stream=True)

            # Check if the image was retrieved successfully
            if r.status_code == 200:
                # Open a local file with wb ( write binary ) permission.
                with open(poster_filepath, "wb") as f:
                    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        bar.next()

    bar.finish()


download_posters()

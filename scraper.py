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
MOVIE_LIST_ID = "7054979"
TV_LIST_ID = "7054980"

root = tkinter.Tk()
root.withdraw()
p = Path(tkinter.filedialog.askdirectory())


def get_poster_links(list_id):
    url = (
        "https://api.themoviedb.org/3/list/"
        + list_id
        + "?api_key="
        + API_KEY
        + "&language=en-US"
    )

    response = requests.get(url)
    list = response.json()

    media = []
    for item in list["items"]:
        media.append(
            (BASE_IMAGE_LINK + item["poster_path"], item["title"].replace(":", " -"))
        )

    return media


def download_posters():
    poster_links = get_poster_links(TV_LIST_ID)
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

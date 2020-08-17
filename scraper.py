import requests
import shutil
import os.path
import pathlib
from pathlib import Path
import tkinter
from tkinter import filedialog
from progress.bar import ChargingBar


API_KEY = "4bbd5cbd9da6580bf6bda048d43d8338"
MOVIE_LIST_ID = "7054979"
TV_LIST_ID = "7054980"


# list_id = input("List ID: ")


class Media:
    def __init__(self, type):
        if type == "movie":
            self.title = "title"
            self.folder = "Movies"
        elif type == "tv":
            self.title = "name"
            self.folder = "TV Shows"


root = tkinter.Tk()
root.withdraw()
p = Path(tkinter.filedialog.askdirectory())


def get_media_info(list_id):
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
        info = (
            item["id"],
            item["media_type"],
            item[Media(item["media_type"]).title].replace(":", " -"),
        )
        if item["media_type"] == "movie":
            info = info + (item["poster_path"],)

        media.append(info)

    # media[0] = id
    # media[1] = movie or tv
    # media[2] = media name
    # media[3] = if movie, poster link
    return media


def download_posters():
    media_info = get_media_info(MOVIE_LIST_ID)
    bar = ChargingBar("Downloading posters", max=len(media_info))
    for media in media_info:
        poster_filepath = p / Media(media[1]).folder / (media[2] + ".jpg")
        print(poster_filepath)
        if not os.path.isfile(poster_filepath):
            # Open the url image, set stream to True, this will return the stream content.
            r = requests.get(media[3], stream=True)

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

import csv
import requests
import shutil
import os.path
import tkinter
from tkinter import filedialog
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_LINK = "https://www.themoviedb.org/movie/"

options = Options()
options.headless = True

root = tkinter.Tk()
root.withdraw()
path = tkinter.filedialog.askdirectory()

with open("movie_ids.csv") as ids:
    reader = csv.reader(ids)
    data = list(reader)

# data[n][0] = id
# data[n][1] = name

driver = webdriver.Firefox()
driver.wait = WebDriverWait(driver, 10)

for movie in data:
    poster_filepath = path + "/" + movie[1] + ".jpg"
    if not os.path.isfile(poster_filepath):
        driver.get(BASE_LINK + str(movie[0]))
        poster_popup = driver.wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/div[1]/main/section/div[2]/div/div/section/div[1]/div[1]",
                )
            )
        )
        poster_popup.click()
        poster_popup.click()
        poster_url = driver.wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[10]/div/section/div/div/div/form/p[2]/a",)
            )
        ).get_attribute("href")

        # Open the url image, set stream to True, this will return the stream content.
        r = requests.get(poster_url, stream=True)

        # Check if the image was retrieved successfully
        if r.status_code == 200:
            # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
            r.raw.decode_content = True

            # Open a local file with wb ( write binary ) permission.
            with open(poster_filepath, "wb") as f:
                shutil.copyfileobj(r.raw, f)

            print("Image sucessfully Downloaded: ", movie[1])
        else:
            print("Couldn't be retreived - ", movie[1])

quit()

import csv
import requests
import shutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# options = Options()
# options.headless = True


BASE_LINK = "https://www.themoviedb.org/movie/"

with open("movie_ids.csv") as ids:
    reader = csv.reader(ids)
    data = list(reader)

# data[n][0] = id
# data[n][1] = name

driver = webdriver.Firefox()
driver.wait = WebDriverWait(driver, 10)

for movie in data:
    driver.get(BASE_LINK + str(movie[0]))
    poster_popup = driver.find_element_by_xpath(
        "/html/body/div[1]/main/section/div[2]/div/div/section/div[1]/div[1]"
    )
    poster_popup.click()
    poster_popup.click()
    link = driver.wait.until(
        EC.presence_of_element_located(
            (By.XPATH, "/html/body/div[10]/div/section/div/div/div/form/p[2]/a",)
        )
    ).get_attribute("href")

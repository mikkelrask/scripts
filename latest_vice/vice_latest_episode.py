#!/usr/bin/env python3

"""
This webscraper opens a headless chrome window and seaches for line in the
tingfinder.csv file on the danish trading platforms dba.dk, gulgratis.dk and
auction house Lauritz.com (experimental)
"""

import pickle # Pickle is a simple database, to store the number of ads
import traceback
from selenium import webdriver # Selenium is what opens up the browser, and does the stuff
from selenium.webdriver.chrome.options import Options # Options are passed to the Chrome browser
from selenium.common.exceptions import NoSuchElementException

# Rich console for extra flavor

# Chrome settings
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless")

#Initialize the browser and declare where to go
driver = webdriver.Chrome(options=chrome_options)

def get_latest_url():
    """
    Opens up vice.com and fetches the latest episodes URL
    """
    url = "https://www.vicetv.com/en_us/show/vice-news-tonight-1-507"

    try:
        # Check if the latest episode URL is present
        db_url = pickle.load(open("/home/raske/.cache/vice/URLS.dat", "rb"))
    except Exception as error:
        print("No saved URLS. Starting from scratch...")
        db_url = ""
        print(error)
        traceback_str = traceback.format_exc()
        print(traceback_str)

    driver.get(url)
    driver.implicitly_wait(5)

    try:
        latest_url = driver.find_element_by_class_name("grid__wrapper__card").get_attribute("href")
        pickle.dump(latest_url, open("/home/raske/.cache/vice/URLS.dat", "wb"))

        if latest_url != db_url:
            print(latest_url)
        else:
            print("File has already been downloaded.")
    except NoSuchElementException:
        print("ERR: Could not locate URL.")

if __name__ == '__main__':
    get_latest_url()
    driver.quit()

#!/usr/bin/env python
"""
This script will open dba.dk in a headless Chrome browser, and search the
products within a certain pricerange, saved in an excel sheet or CSV file.
"""

import time # We use time to do waits between pages
import pickle # Pickle is a simple database, to store the number of ads
import csv # CSV is the fileformat of the product sheet.
from notify import notification # we use notify to send notifications to the user
from selenium import webdriver # Selenium is what opens up the browser, and does the stuff
from selenium.webdriver.chrome.options import Options # Options are passed to the Chrome browser
from selenium.webdriver.common.keys import Keys # Keys is so we can send keys to inputs.

# Chrome settings
chrome_options = Options()
chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")

#Initialize the browser and declare where to go
driver = webdriver.Chrome(options=chrome_options)
DBA = "https://dba.dk"
GG = "https://guloggratis.dk"
PRICE = 0
MAXPRICE = 0
PRODUCT = ""
driver.implicitly_wait(5)

def den_blaa_avis():
    """
    Search dba.dk for instances of each line in the CSV file.
    If we got any hits, show a link to the user
    """
    def remove(string): #remove spaces from PRODUCT to create individual .dat filename
        return string.replace(" ","")

    # See if we have any data on the given product else db antal is 0
    try:
        db_antal = pickle.load(open(remove(PRODUCT) + ".dat", "rb"))
    except:
        db_antal = 0

    driver.get(DBA) # Get DBA.dk in the browser
    time.sleep(2) # Wait just a sec
    search = driver.find_element_by_id("searchField")
    print("-------------------------------")

    print("Produkt: " + PRODUCT)
    search.send_keys(PRODUCT) # send search term / product name
    search.send_keys(Keys.RETURN)
    time.sleep(2)

    driver.find_element_by_xpath("//h4[contains(text(), 'Pris')]").click() # Set our price wishes
    print("Pris: " + str(PRICE)+"-"+str(MAXPRICE))
    price = driver.find_element_by_class_name("rangeFrom") # Min
    price.send_keys(PRICE)
    price = driver.find_element_by_class_name("rangeTo") # Max
    price.send_keys(MAXPRICE)
    price.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        #if driver.find_element_by_xpath("//td[contains(text(),'annoncer')]"):
        antal_annoncer_string = driver.find_element_by_xpath("//td[contains(text(),\
                    'annoncer')]").get_attribute("innerHTML").strip()
        antal = [int(i) for i in antal_annoncer_string.split() if i.isdigit()] # Get only the integer
        diff = int(antal[0]) - db_antal
        if diff > 0:
            string = str(antal[0]) + ' annoncer fundet. ' + str(diff) + '+ ift forrige søgning.'
            print(str(antal[0]) + ' annoncer fundet. ' + str(diff) + '+ ift forrige søgning.')
            print("URL: " + driver.current_url)
            print("-------------------------------")
            pickle.dump(int(antal[0]), open(remove(PRODUCT) + ".dat", "wb")) # Dump the new number of items into the database
            notification(string,title=PRODUCT)
        elif diff == 0:
            print ("Ingen nye annoncer.")
            print("-------------------------------")
        else:
            print(str(diff) + " ift. sidst søgning")
            pickle.dump(int(antal[0]), open(remove(PRODUCT) + ".dat", "wb")) # Dump the new number of items into the database
    except:
        print(PRODUCT + " ikke fundet i prisklassen.")
        print("-------------------------------")

# Check the same on GulGratis
def gul_og_gratis():
    driver.get(GG)
    time.sleep(2)
    search = driver.find_element_by_id("searchField")
    search.send_keys(PRODUCT)
    search.send_keys(Keys.RETURN)
    time.sleep(2)
    driver.find_element_by_xpath("//h4[contains(text(), 'Pris')]").click()
    print("Searching...")
    price = driver.find_element_by_class_name("rangeFrom")
    price.send_keys(PRICE)
    price = driver.find_element_by_class_name("rangeTo")
    price.send_keys(MAXPRICE)
    price.send_keys(Keys.RETURN)
    time.sleep(2)
    print("Produkt: " + PRODUCT)
    print(driver.find_element_by_xpath("//td[contains(text(),'annoncer')]").get_attribute("innerHTML").strip() + " i prisklassen " + str(PRICE) + " - " + str(MAXPRICE))
    print("URL:" + driver.current_url)

filename = "search_agent.csv"

print("Søger...")
with open(filename, "r") as csvfile:
    datareader = csv.reader(csvfile)
    for row in datareader:
        PRODUCT = row[0]
        PRICE = row[1]
        MAXPRICE = row[2]
        den_blaa_avis()

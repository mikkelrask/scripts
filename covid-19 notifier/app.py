# Script i run at boot to notify me of the current total number of COVID-19 cases in Denmark
# It utilizes the BeautifulSoup (bs4) library to parse the data from the link and
# the plyer lib to show the notification natively on my linux laptop.
# You can run the script however you like, and whenever you like, but the numbers are only updated daily. 
# I simply run it through my I3WM config, thats being run at boot with `exec --no-startup-id python /PATH/TO/app.py`
# Requirements can be installed with `pip install -r requirements.txt`

import requests
from bs4 import BeautifulSoup
from plyer import notification
import time

res = requests.get('https://worldometers.info/coronavirus/country/denmark').text
soup = BeautifulSoup(res,'html.parser')
soup.encode('utf-8')
cases = soup.find("div", {"class": "maincounter-number"}).get_text().strip()

def notifyMe(title,message):
    notification.notify(
        title = title,
        message = message,
        timeout = 5 )
        

notifyMe('Covid-19 sager i DK',cases)

import logging
import os
import requests
import time

from selenium.common.exceptions import WebDriverException
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from urllib.parse import urlencode, quote_plus
from pathlib import Path
#from pprint import pprint


logger = logging.getLogger("postbank")
logger.setLevel(logging.INFO)
fh = logging.StreamHandler()
fh.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

opts = Options()
opts.headless = True
logger.info("Starte FireFox")
browser = Firefox(options=opts)

#Setzen der Variablen
postbankurl = os.environ.get('POSTBANKURL')
picturepath = os.environ.get('PICTUREPATH', '/tmp/home')
username = os.environ.get('USERNAME')
password = os.environ.get('PASSWORD')
telegrambotkey = os.environ.get('TELEGRAMBOTKEY')
chatid = os.environ.get('CHATID')

logger.info("Öffne Startseite")

# Startseite
browser.get(postbankurl)
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/1.png")
except WebDriverException:
    logger.warning("Bild 1 konnte nicht gespeichert werden.")
browser.find_element_by_id('username').send_keys(username)
browser.find_element_by_id('password').send_keys(password)

# Seite nach Login
browser.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div/form/div[2]/div[3]/button').submit()
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/2.png")
except WebDriverException:
    logger.warning("Bild 2 konnte nicht gespeichert werden.")
balance = browser.find_element_by_xpath('/html/body/div[1]/div/main/div[2]/div[1]/div/div[2]/div/div/table/tbody/tr[1]/td[3]/span/span/span').text

logger.info(balance)

# Logout
browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/header/div/div/div').click()
time.sleep(10)
browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/nav[2]/div[2]/div[2]/ul/li[6]/a').click()
time.sleep(30)
try:
    browser.get_screenshot_as_file(picturepath + "/3.png")
except WebDriverException:
    logger.warning("Bild 3 konnte nicht gespeichert werden.")

browser.quit()

# Balance Behandlung
balancezahl = balance[:len(balance)-2]
balancezahl = str(balancezahl).replace(".", "").replace(",", ".")

# Alten Wert aus Datei lesen und vergleichen
my_file = Path(picturepath + "/balance.txt")
if not my_file.exists():
    filestore = open(picturepath + "/balance.txt", "w")
    filestore.write("0.0")
    filestore.close()

filestore = open(picturepath + "/balance.txt", "r")
oldbalance = filestore.read()
filestore.close()

text = ""
if balancezahl != oldbalance:
    text = "Postbank: Neue Kontobewegung - Änderung von " + oldbalance + "€ auf " + balancezahl + "€"
    payload = {'chat_id': chatid, 'text': text}
    result = urlencode(payload, quote_via=quote_plus)
    r = requests.get("https://api.telegram.org/" + telegrambotkey + "/sendMessage?" + result)
    #pprint(r.json())
    logger.info(r.json())
    filestore = open(picturepath + "/balance.txt", "w")
    filestore.write(balancezahl)
    filestore.close()


exit(0)
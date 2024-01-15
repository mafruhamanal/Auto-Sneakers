from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import time
import pywhatkit as kit
import datetime

list_data = []


def initial_browser(link):
    s = Service(ChromeDriverManager().install())
    chromeOptions = Options()
    chromeOptions.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=s,options=chromeOptions)
    driver.get(link)
    print("starting driver")
    time.sleep(20)
    click_button = driver.find_element(by=By.CLASS_NAME, value="ux-call-to-action__text")
    time.sleep(20)
    click_button.click()
    time.sleep(20)
    click_button = driver.find_element(by=By.CLASS_NAME, value="ux-bin-nudge__guestCheckOut")
    time.sleep(20)
    click_button.click()
    time.sleep(60)



initial = []
links = []
trainers = []
urls = []


def limited_edition():
    url = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1312&_nkw=limited+edition+trainers&_sacat=0"
    website = requests.get(url)
    website_text = website.text
    soup = BeautifulSoup(website_text, features="html.parser")
    for link in soup.find_all('a'):
        initial.append(link.get('href'))

    for link in initial:
        if type(link) == type("str"):
            if "itm" in link:
                links.append(link)

    for link in links:
        url = link
        website = requests.get(url)
        website_text = website.text
        soup = BeautifulSoup(website_text, features="html.parser")
        for tag in soup.find_all("meta"):
            if tag.get("property", None) == "og:title":
                title = tag.get("content", None)
                if "8" in title and title not in trainers:
                    trainers.append(title)
                    urls.append(url)
                    message = f"Found you a limited edition pair of trainers! : {title}:{url}"
                    phone_number = "+123456789"  # input phone number here
                    current_time = datetime.datetime.now()
                    scheduled_time = current_time + datetime.timedelta(minutes=4)
                    kit.sendwhatmsg(phone_number, message, scheduled_time.hour, scheduled_time.minute)
                    initial_browser(url)


if __name__ == "__main__":
    while True:
       limited_edition()
       time.sleep(100)

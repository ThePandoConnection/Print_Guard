from selenium import webdriver
from PIL import Image

def get_image():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=640x480')
    chrome_options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    # URL of website
    url = "http://172.20.10.2"

    # Opening the website
    driver.get(url)

    driver.save_screenshot("image.png")

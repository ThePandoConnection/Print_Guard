from selenium import webdriver
from PIL import Image
import os


def get_image():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=640x480')
    chrome_options.add_argument("disable-gpu")
    driver = webdriver.Chrome('chromedriver', chrome_options=chrome_options)

    try:
        os.remove('./camera/image.png')
    except FileNotFoundError:
        None
    try:
        os.remove('./camera/corrected.jpg')
    except FileNotFoundError:
        None


    # URL of website
    url = "http://192.168.0.210"

    # Opening the website
    driver.get(url)

    driver.save_screenshot("./camera/image.png")
    im = Image.open('./camera/image.png')
    im = im.convert('RGB')
    out = im.rotate(180)
    out.save('./camera/image.jpg')

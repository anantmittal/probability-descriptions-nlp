from selenium import webdriver

import os.path
import random
import sys
import time
from bs4 import BeautifulSoup
import re

from selenium.webdriver import ActionChains

from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.webdriver.phantomjs.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from random import randint

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import os

DELAY = 0.5

webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.Accept-Language'] = 'en-US,en;q=0.8'
webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.User-Agent'] = \
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')

driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", chrome_options=chrome_options)

driver.set_window_size(1280, 720)


def check_exists_by_class(cls):
    try:
        driver.find_element_by_class_name(cls)
    except NoSuchElementException:
        return False
    return True


def main():
    infile = open(sys.argv[1])
    rcnt_out = sys.argv[2]
    xpdopen_out = sys.argv[3]

    driver.get('http://www.google.com')

    # Tell below how many times you want to go down. Don't be dirty, we mean in the google autocomplete
    N = 10
    file_name = 1
    for search_string in infile:
        print(search_string)
        for i in range(1, int(N + 1)):
            print(file_name)
            actions = ActionChains(driver)
            actions.move_to_element(driver.find_element_by_id('lst-ib')) \
                .send_keys(str(search_string[:-1])) \
                .pause(1) \
                .send_keys(Keys.DOWN * int(i)) \
                .send_keys(Keys.RETURN) \
                .perform()

            # Below two lines get the complete html of the page
            el = driver.find_element_by_id('rcnt')
            page_html = el.get_attribute('innerHTML')

            file = open(rcnt_out+"/"+str(file_name)+".txt","w")
            file.write(page_html)
            file.close()

            # Below lines get the xpdopen class box text
            if check_exists_by_class('xpdopen'):
                xpdopen_el = driver.find_element_by_class_name('xpdopen')
                xpdopen_text = xpdopen_el.text
                file = open(xpdopen_out + "/" + str(file_name) + ".txt", "w")
                file.write(xpdopen_text)
                file.close()

            driver.back()
            file_name += 1
    try:
        driver.close()
        driver.quit()
    except BaseException as e:
        print(repr(e))  # YOLO


if __name__ == "__main__":
    main()

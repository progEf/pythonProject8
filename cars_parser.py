import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import pickle

import pandas as pd

PATH_name = input("Укажите папку: ")

item_url_list = []
profile_url_list = []



rating_list = []
products_url_list = []
profile_url_list = []

options = webdriver.FirefoxOptions()
options.set_preference("disable-blink-features", "AutomationControlled")
options.add_argument('--log-level=3')
# proxy = f"172.67.70.229:80"
# options.add_argument('--proxy-server=%s' % proxy)
options.set_preference("network.proxy.type", 1)
options.set_preference("network.proxy.http", "117.160.250.132")
options.set_preference("network.proxy.http_port", 8899)

ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36"
options.add_argument(f"user-agent={ua}")

driver = webdriver.Firefox(options=options)

driver.set_window_size(1900, 1000)
url = 'https://www.avito.ru/tver/avtomobili/haval-ASgBAgICAUTgtg2umCg?cd=1&radius=200&searchRadius=200'
driver.get(url)
a = input('Нажмите любую клавишу на клавиатуре!!! Для завершение скрипта.')
driver.refresh()
cookies = driver.get_cookies()
with open(f'{PATH_name}/files/cookies2.pkl', 'wb') as file:
    pickle.dump(cookies, file)
driver.quit()
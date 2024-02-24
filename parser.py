import random
import time
from telnetlib import EC

from selenium import webdriver
from selenium.webdriver.common.by import By

import pickle
from faker import Faker
from selenium.webdriver.support import expected_conditions as Eq
import pandas as pd
from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from selenium.webdriver.support.wait import WebDriverWait

n = 0


# options = webdriver.ChromeOptions()
# options.add_argument("--disable-blink-features=AutomationControlled")
# options.add_argument('--log-level=3')
# options.add_argument('--proxy-server=http://%s:%s' % ('117.160.250.132', '8899'))


def parsing(url, file_name) -> None:
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

    driver.get(url)

    with open(f'{PATH_name}/cookies2.pkl', 'rb') as file:
        cookies = pickle.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(4)
    driver.refresh()
    now = time.time()
    n = 0
    while int(time.time() - now) <= pars_time * 60:
        n += 1

        time.sleep(5)
        #driver.switch_to.window(driver.window_handles[0])

        #items = driver.find_element(By.XPATH, f"(//div[@data-marker='item-photo'])[{n}]")
        lists1 = driver.find_elements(By.XPATH, f"(//div[@class='iva-item-root-_lk9K photo-slider-slider-S15A_ iva-item-list-rfgcH iva-item-redesign-rop6P iva-item-responsive-_lbhG items-item-My3ih items-listItem-Gd1jN js-catalog-item-enum'])")
        for i in lists1:
            BlockAll = i.find_element(By.XPATH, ".//div[@class='styles-module-theme-CRreZ']")
            BlockUrlAds = BlockAll.find_element(By.XPATH, ".//a[@class='styles-module-root-QmppR styles-module-root_noVisited-aFA10']").get_attribute("href")

            BlockUrlUser = BlockAll.find_element(By.XPATH, ".//a[@class='styles-module-root-QmppR styles-module-root_noVisited-aFA10 styles-module-root_preset_black-JkIdG']").get_attribute("href")
            try:
                BlockRight = BlockAll.find_element(By.XPATH, ".//span[@data-marker='seller-rating/score']").text.replace(',', '.')
                if float(BlockRight) >= rating_from and float(BlockRight) <= rating_to:
                    rating_list.append(BlockRight)
                    products_url_list.append(BlockUrlAds)
                    profile_url_list.append(BlockUrlUser)
            except:
                pass
        try:
            driver.find_element(By.XPATH, f"(//a[@data-marker='pagination-button/nextPage'])").click()

            print(rating_list)
            print(products_url_list)
            print(profile_url_list)
            print('-------')
        except:
            print('Скрипт достиг максимальное кол-во страниц')
            break




    df = pd.DataFrame(
        {'Рейтинг': rating_list,
         'Ссылка на товар': products_url_list,
         'Ссылка на профиль продавца': profile_url_list}
    )

    df.to_excel(f'{PATH_name}/files/{file_name}.xlsx', index=False)
    driver.quit()


if __name__ == '__main__':
    url = ''
    file_name = ''
    urls_list = []
    name_list = []
    args = []

    PATH_name = input("Укажите папку: ")

    print('Рейтинг')
    rating_from = float(input('От: '))
    rating_to = float(input('До: '))

    pars_time = float(input("Время парсинга: "))

    while True:
        url = input("Ссылка Авито: ")
        file_name = input("Название файла excel: ")
        if url != '0':
            urls_list.append(url)
            name_list.append(file_name)

        else:
            break

    for i, url_ in enumerate(urls_list):
        print(i, url_)
        print(f'{i}, {url_}')
        parsing(urls_list[i], name_list[i])

        time.sleep(2)

import time

from selenium import webdriver
from selenium.webdriver.common.by import By

import pickle

import pandas as pd


item_url_list = []
profile_url_list = []

options = webdriver.ChromeOptions()

options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument('--log-level=3')


def parsing(url) -> None:

    global profile_url_list

    # driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver", options=options)
    driver = webdriver.Chrome("./chromedriver.exe", options=options)

    driver.get(url)

    n=0

    try:
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)

    except:

        pass

    time.sleep(1)

    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

    time.sleep(1)

    driver.refresh()


    while True:
        try:
            n+=1

            item_url = driver.find_element(By.XPATH, f"(//a[@class='link-link-MbQDP link-design-default-_nSbv title-root-zZCwT body-title-drnL0 title-root_maxHeight-X6PsH'])[{n}]").get_attribute("href")

            item_url_list.append(item_url)

        except:
            try:
                driver.find_element(By.XPATH, f"(//a[@class='Tabs-nav-tab-link-ooeMr'])").click()

                n = 0

                while True:
                    try:
                        n+=1

                        item_url = driver.find_element(By.XPATH, f"(//a[@class='title-root-zZCwT body-title-drnL0 title-root_maxHeight-X6PsH text-text-LurtD text-size-s-BxGpL text-bold-SinUO'])[{n}]").get_attribute("href")

                        item_url_list.append(item_url)

                    except:
                        break

            except:
                break

            break

    subs = '/avtomobili/'
 
    res = [i for i in item_url_list if subs in i]

    if len(res) >= 2:
        profile_url_list.append(url)

    driver.quit()


if __name__ == '__main__':

    file_name = input('Название файла: ')

    excel_data_df = pd.read_excel(f'{file_name}.xlsx', sheet_name='Sheet1')

    excel_data_df = excel_data_df['Ссылка на профиль продавца'].tolist()

    for i, url_ in enumerate(excel_data_df):

        parsing(excel_data_df[i])
        time.sleep(2)

    df = pd.DataFrame(
            {'Ссылка на профиль продавца': profile_url_list}
            )

    df.to_excel(f'./{file_name}_cars.xlsx', index=False)
# maps_scraper.py（Step 2：Googleマップから企業情報を取得）

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd


def get_google_maps_data(keyword, max_scrolls=10):
    # --- Chrome起動設定（ヘッドレス） ---
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        # Google Mapsへアクセス
        driver.get("https://www.google.com/maps")
        time.sleep(2)

        # 検索ボックスにキーワード入力
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)

        data = []
        scrollable_div_xpath = '//div[contains(@aria-label, "リスト")]'
        last_height = 0

        for _ in range(max_scrolls):
            # 企業リストを取得
            items = driver.find_elements(By.CSS_SELECTOR, 'div.section-result')
            for item in items:
                try:
                    name = item.find_element(By.CSS_SELECTOR, 'h3 span').text
                except:
                    name = ""
                try:
                    category = item.find_element(By.CSS_SELECTOR, 'span.section-result-details').text
                except:
                    category = ""
                try:
                    address = item.find_element(By.CSS_SELECTOR, 'span.section-result-location').text
                except:
                    address = ""
                try:
                    phone = item.find_element(By.CSS_SELECTOR, 'span.section-result-phone-number').text
                except:
                    phone = ""

                row = {
                    "企業名": name,
                    "業種": category,
                    "住所": address,
                    "電話番号": phone
                }

                if row not in data:
                    data.append(row)

            # スクロール操作
            try:
                scrollable = driver.find_element(By.XPATH, scrollable_div_xpath)
                driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', scrollable)
                time.sleep(2)
            except:
                break

        df = pd.DataFrame(data)
        return df

    finally:
        driver.quit()
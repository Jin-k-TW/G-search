import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_google_maps_data(keyword):
    base_url = "https://www.google.com/search"
    params = {"q": f"{keyword} 会社", "hl": "ja"}
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    response = requests.get(base_url, params=params, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    cards = soup.select("div.VkpGBb")

    for card in cards:
        name = card.select_one(".dbg0pd")
        category = card.select_one(".rllt__details span")
        address = card.select_one(".rllt__details div")
        phone = card.select_one(".rllt__details span:nth-of-type(2)")

        results.append({
            "企業名": name.text.strip() if name else "",
            "業種": category.text.strip() if category else "",
            "住所": address.text.strip() if address else "",
            "電話番号": phone.text.strip() if phone else ""
        })

    return pd.DataFrame(results)

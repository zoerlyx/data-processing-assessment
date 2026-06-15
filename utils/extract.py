
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

BASE_URL = "https://fashion-studio.dicoding.dev/"

def extract_product_data(card):
    try:
        title = card.find("h3", class_="product-title").text.strip()
        price = card.find("span", class_="price").text.strip()
        details = card.find_all("p")

        rating = details[0].text.strip() if len(details) > 0 else None
        colors = details[1].text.strip() if len(details) > 1 else None
        size = details[2].text.strip() if len(details) > 2 else None
        gender = details[3].text.strip() if len(details) > 3 else None

        return {
            "title": title,
            "price": price,
            "rating": rating,
            "colors": colors,
            "size": size,
            "gender": gender,
        }
    except Exception as e:
        print("Error di card:", e)
        return None


def scrape_page(page_number):
    url = BASE_URL if page_number == 1 else f"{BASE_URL}page{page_number}"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error saat mengambil halaman {page_number}: {e}")
        return []

    cards = soup.find_all("div", class_="collection-card")
    data = []

    for card in cards:
        product = extract_product_data(card)
        if product:
            data.append(product)

    return data


def scrape_main():
    all_products = []

    for page in range(1, 51):
        print(f"Scraping halaman {page}...")
        all_products.extend(scrape_page(page))

    return pd.DataFrame(all_products)

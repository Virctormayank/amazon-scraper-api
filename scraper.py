# scraper.py

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

def scrape_amazon_products(query="laptop", num_pages=1):
    base_url = "https://www.amazon.in/s"
    ua = UserAgent()
    headers = {
        "User-Agent": ua.random,
        "Accept-Language": "en-US,en;q=0.9"
    }

    all_products = []

    for page in range(1, num_pages + 1):
        params = {"k": query, "page": page}
        response = requests.get(base_url, headers=headers, params=params)
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in results:
            name_tag = item.select_one("h2 span")
            name = name_tag.text.strip() if name_tag else "N/A"

            price_tag = item.find("span", class_="a-price-whole")
            price = price_tag.text.strip().replace(",", "") if price_tag else "N/A"

            rating_tag = item.find("span", class_="a-icon-alt")
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            all_products.append({
                "Name": name,
                "Price (₹)": price,
                "Rating": rating
            })

    return all_products

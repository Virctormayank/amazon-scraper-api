# Updated scraper.py with proxy and image/link support
import requests
from bs4 import BeautifulSoup

SCRAPER_API_KEY = "5aafa3e416a809f9637e22b86e577e3d"

def scrape_amazon_products(query="laptop", num_pages=1):
    base_url = "https://www.amazon.in/s"
    all_products = []

    for page in range(1, num_pages + 1):
        amazon_url = f"{base_url}?k={query}&page={page}"

        proxy_url = "http://api.scraperapi.com"
        params = {
            "api_key": SCRAPER_API_KEY,
            "url": amazon_url,
            "render": "false",
        }

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9"
        }

        response = requests.get(proxy_url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"[!] Error: Status code {response.status_code}")
            continue

        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find_all("div", {"data-component-type": "s-search-result"})

        for item in results:
            name_tag = item.select_one("h2 span")
            name = name_tag.text.strip() if name_tag else "N/A"

            price_tag = item.find("span", class_="a-price-whole")
            price = price_tag.text.strip().replace(",", "") if price_tag else "N/A"

            rating_tag = item.find("span", class_="a-icon-alt")
            rating = rating_tag.text.strip() if rating_tag else "N/A"

            link_tag = item.select_one("a.a-link-normal")
            link = "https://amazon.in" + link_tag['href'] if link_tag and 'href' in link_tag.attrs else ""

            img_tag = item.select_one("img.s-image")
            image = img_tag['src'] if img_tag and 'src' in img_tag.attrs else ""

            all_products.append({
                "title": name,
                "price": price,
                "rating": rating,
                "link": link,
                "image": image
            })

    return all_products

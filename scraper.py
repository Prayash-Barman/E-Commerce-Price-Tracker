import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

def get_price(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, "html.parser")

        # Get product name
        name = soup.find("span", id="productTitle")
        if name:
            name = name.text.strip()
        else:
            name = "Unknown Product"

        # Get price
        price = soup.find("span", class_="a-price-whole")
        if price:
            price = float(price.text.replace(",", "").replace(".", ""))
            return name, price
        else:
            return name, None

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None
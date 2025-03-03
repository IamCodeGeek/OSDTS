import requests as r
import bs4
import time
import schedule
from datetime import datetime

# List of Amazon product ASINs
product_list = ['B0C2CVS7LP', 'B0C9YMVX2C', 'B0C75J66C8', 'B0C93KV2W8']
base_url = 'https://www.amazon.in/dp/'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9'
}

def track_price():
    """Fetches product prices from Amazon and prints them."""
    print("\nRunning price tracker at:", datetime.now())

    # Fetch cookies from base URL
    base_response = r.get("https://www.amazon.in", headers=headers)
    cookies = base_response.cookies

    for prod in product_list:
        product_url = base_url + prod
        product_response = r.get(product_url, headers=headers, cookies=cookies)
        soup = bs4.BeautifulSoup(product_response.text, features='lxml')

        # Try finding price in multiple locations
        price = None
        try:
            if soup.find('span', class_="a-price-whole"):
                price = soup.find('span', class_="a-price-whole").text.strip()
            elif soup.find('span', class_="a-offscreen"):
                price = soup.find('span', class_="a-offscreen").text.strip()  # Hidden price
            elif soup.find('span', class_="a-price"):
                price = soup.find('span', class_="a-price").text.strip()
        except Exception as e:
            print(f"Error fetching price for {product_url}: {e}")

        final_price = price if price else "Price not found"
        print(product_url, final_price)

        time.sleep(2)  # Delay to avoid bot detection

# Schedule the script to run every 1 minute
schedule.every(1).minutes.do(track_price)

# Run the scheduled task continuously
while True:
    schedule.run_pending()
    time.sleep(1)

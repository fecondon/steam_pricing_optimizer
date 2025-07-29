import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import html

BASE_URL = 'https://store.steampowered.com/search/'
PARAMS = {
    'specials': 1,
    'page': 1,
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15'
}

games = []

# Scrape first 100 pages of Steam specials
for page in range(1, 101):
    PARAMS['page'] = page
    response = requests.get(BASE_URL, params=PARAMS, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    rows = soup.find_all('a', class_='search_result_row')
    for row in rows:
        title = row.find('span', class_='title').text.strip()
        release = row.find('div', class_='search_released').text.strip()

        try:
            review = html.escape(
                row.find('span', {'data-tooltip-html': True})['data-tooltip-html']
            )
        except TypeError:
            print(f'{title} has no reviews!')
            review = None

        try:
            discount_block = row.find('div', class_='search_price_discount_combined')
            discount_percent = int(discount_block.find('div', class_='discount_pct').text.strip().split('%')[0])

            prices = discount_block.find('div', class_='discount_prices').text.strip().split('$') if discount_block else ['']
            prices = [p for p in prices if p]

            original_price = float(prices[0].replace(',', '')) if len(prices) == 2 else None
            discounted_price = float(prices[1].replace(',', '')) if len(prices) == 2 else float(prices[0].replace(',', '')) if prices else None
        except AttributeError:
            print(f'{title} has no price information')
            original_price = None
            discounted_price = None

        tags = row.get('data-ds-tagids')

        games.append({
            'title': title,
            'release_date': release,
            'review': review,
            'original_price': original_price,
            'discount_percent': discount_percent,
            'discounted_price': discounted_price,
            'tag_ids': tags
        })

    print(f'Scraped page {page} with {len(rows)} games.')
    time.sleep(1.5)

# Save to CSV
steam_df = pd.DataFrame(games)
steam_df.to_csv('steam_specials.csv', index=False)
print(f'Saved steam_specials.csv with {len(steam_df)} records')
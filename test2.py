import requests
from bs4 import BeautifulSoup

def scrape_flipkart(product):
    url = f"https://www.flipkart.com/search?q={product}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')
        results = []
        for item in soup.find_all('div', class_='tUxRFH'):
            try:
                name = item.find('div', class_='KzDlHZ').text.strip()
                price = item.find('div', class_='Nx9bqj _4b5DiR').text.strip()
                results.append({'name': name, 'price': price})
            except Exception as e:
                print("Error scraping product details:", e)
        return results
    except requests.RequestException as e:
        print("Error making request to Flipkart:", e)
        return []

if __name__ == "__main__":
    product_name = input("Enter the product you want to search for: ")
    search_results = scrape_flipkart(product_name)
    if search_results:
        print("Search Results:")
        for result in search_results:
            print(f"Name: {result['name']}, Price: {result['price']}")
    else:
        print("No results found.")

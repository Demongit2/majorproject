import requests
from bs4 import BeautifulSoup

def scrape_flipkart_search_results(search_url):
    # Send a GET request to the search URL
    response = requests.get(search_url)
    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all product containers on the page
        product_containers = soup.find_all('div', class_='tUxRFH')

        # Iterate through each product container
        for container in product_containers:
            # Find the product name
            product_name = container.find('div', class_='KzDlHZ').text.strip()

            # Find the product price
            product_price = container.find('div', class_='Nx9bqj _4b5DiR').text.strip()

            # Print the product name and price
            print("Product Name:", product_name)
            print("Product Price:", product_price)
            print("---------------------------------------------")
    else:
        print("Failed to retrieve data. Status code:", response.status_code)

if __name__ == "__main__":
    # URL of the search results page on Flipkart (replace with your search URL)
    search_url = "https://www.flipkart.com/search?q=laptops"

    # Call the function to scrape the search results
    scrape_flipkart_search_results(search_url)

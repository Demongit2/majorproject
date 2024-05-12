from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import re


app = Flask(__name__)

def scrape_flipkart(product):
    url = f"https://www.flipkart.com/search?q={product}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    results = []
    for item in soup.find_all('div', class_='tUxRFH')[:5]:  # Limit to top 5 results
        try:
            name = item.find('div', class_='KzDlHZ').text.strip()
            price = item.find('div', class_='Nx9bqj _4b5DiR').text.strip()
            rating = item.find('div', class_='XQDdHH').text.strip()  # Get the rating
            image = item.find('img', class_='DByuf4')['src']
            link = item.find('a', class_='CGtC98')['href']  # Get the product link
            results.append({'name': name, 'price': price, 'rating': rating, 'image': image, 'link': link})
        except Exception as e:
            print("Error scraping Flipkart:", e)
    return results

def scrape_amazon(product):
    url = f"https://www.amazon.in/s?k={product}"
    response = requests.get(url, headers={"User-Agent":"Defined"})
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []
    for item in soup.find_all('div', class_='s-result-item')[:7]:
        try:
            name = item.find('span', class_='a-size-medium').text.strip()
            price = item.find('span', class_='a-price-whole').text.strip()
            rating = item.find('span',class_= 'a-icon-alt').text.strip()
            image = item.find('img')['src']
            link = item.find('a')['href']  # Get the product link
            results.append({'name': name, 'price': price, 'image': image, 'rating' : rating, 'link': link})
        except:
            pass
    return results

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    product = request.form['product']

    flipkart_results = scrape_flipkart(product)
    amazon_results = scrape_amazon(product)

    return render_template('compare.html', 
                           product=product, 
                           flipkart_results=flipkart_results,
                           amazon_results=amazon_results)

if __name__ == "__main__":
    app.run(debug=True)

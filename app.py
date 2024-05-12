from flask import Flask, render_template, request, redirect, url_for, session
import requests
from bs4 import BeautifulSoup
import re
from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask import jsonify

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # Change this to a secret key of your choice

# User database (just a simple dictionary for demonstration purposes)
users = {"user1": "password1", "user2": "password2"}

# MySQL configurations
app.config["MYSQL_HOST"] = "sunnyvm.mysql.pythonanywhere-services.com"
app.config["MYSQL_USER"] = "sunnyvm"
app.config["MYSQL_PASSWORD"] = "mysqldatabase"
app.config["MYSQL_DB"] = "sunnyvm$default"
mysql = MySQL(app)

bcrypt = Bcrypt(app)


def scrape_flipkart(product):

    url = f"https://www.flipkart.com/search?q={product}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
    }
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    results = []
    for item in soup.find_all("div", class_="tUxRFH")[:15]:  # Limit to top 5 results
        try:
            name = item.find("div", class_="KzDlHZ").text.strip()
            price = item.find("div", class_="Nx9bqj _4b5DiR").text.strip()
            rating = item.find("div", class_="XQDdHH").text.strip()  # Get the rating
            image = item.find("img", class_="DByuf4")["src"]
            link = item.find("a", class_="CGtC98")["href"]  # Get the product link
            results.append(
                {
                    "name": name,
                    "price": price,
                    "rating": rating,
                    "image": image,
                    "link": link,
                }
            )
        except Exception as e:
            print("Error scraping Flipkart:", e)
    return results


def scrape_amazon(product):
    url = f"https://www.amazon.in/s?k={product}"
    response = requests.get(url, headers={"User-Agent": "Defined"})
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    for item in soup.find_all("div", class_="s-result-item")[:15]:
        try:
            name = item.find("span", class_="a-size-medium").text.strip()
            price = item.find("span", class_="a-price-whole").text.strip()
            rating = item.find("span", class_="a-icon-alt").text.strip()
            image = item.find("img")["src"]
            link = item.find("a")["href"]  # Get the product link
            results.append(
                {
                    "name": name,
                    "price": price,
                    "image": image,
                    "rating": rating,
                    "link": link,
                }
            )
        except:
            pass
    return results


@app.route("/")
def index():
    if "username" in session:
        return redirect(url_for("homepage"))
    return render_template("login_signup.html")


@app.route("/homepage")
def homepage():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("final.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()

    if user and bcrypt.check_password_hash(user[0], password):
        session["username"] = username
        return jsonify({"success": True})

    return jsonify(
        {"success": False, "message": "Invalid username/password combination"}
    )


from flask import jsonify


@app.route("/signup", methods=["POST"])
def signup():
    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]
    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    cursor = mysql.connection.cursor()
    cursor.execute(
        "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
        (username, email, hashed_password),
    )
    mysql.connection.commit()

    # Return JSON response indicating successful signup
    return jsonify({"success": True})


@app.route("/compare", methods=["GET", "POST"])
def compare():
    if "username" not in session:
        return redirect(url_for("index"))
    if request.method == "POST":
        product = request.form["product"]
        flipkart_results = scrape_flipkart(product)
        amazon_results = scrape_amazon(product)
        return render_template(
            "final.html",
            product=product,
            flipkart_results=flipkart_results,
            amazon_results=amazon_results,
        )
    return render_template("compare.html")


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))


@app.route("/final")
def final():
    return render_template("final.html")


if __name__ == "__main__":
    app.run(debug=True)

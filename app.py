from flask import Flask, render_template
from classes.product import Product

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/author")
def index():
    return render_template('author.html')

@app.route("/extraction")
def index():
    return render_template('extraction.html')

@app.route("/products")
def index():
    return render_template('products.html')

app.run(host="0.0.0.0", port=80, debug=True)
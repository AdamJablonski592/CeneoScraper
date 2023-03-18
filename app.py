from flask import Flask, render_template, request
from classes.product import Product

app = Flask(__name__)

def generate_product(id):
    new_product = Product(id)
    soup = new_product.get_product_website()
    amount = new_product.get_page_number(soup)
    opinions = new_product.get_opinions(amount)
    product_data = new_product.return_credentials(opinions, soup)
    return opinions, product_data

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/author")
def author():
    return render_template('author.html')

@app.route("/extraction")
def extraction():
    return render_template('extraction.html')

@app.route("/products")
def products():
    return render_template('products.html')

@app.route('/product_site', methods = ['POST'])
def fetch_data():
    if request.method == 'POST':
        for key, val in request.form.items():
            product_id = val
        product_data = generate_product(product_id)
        return render_template('product_site.html', opinions = product_data[0], product_cred = product_data[1])


app.run(host="0.0.0.0", port=80, debug=True)
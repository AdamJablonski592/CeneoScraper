from flask import Flask, render_template, request
from classes.product import Product

app = Flask(__name__)

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
        new_product = Product(product_id)
        soup = new_product.get_product_website()
        amount = new_product.get_page_number(soup)
        opinions = new_product.get_opinions(amount)
        return render_template('product_site.html', opinions = opinions)


app.run(host="0.0.0.0", port=80, debug=True)
from flask import Flask, render_template, request
from classes.product import Product
import json
import csv
import pandas as pd

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

@app.route('/download_json/<string:id>', methods = ['GET'])
def download_json(id):
    if request.method == 'GET':
        product_data = generate_product(id)
        with open(f'{id}.json', 'w', encoding='utf8') as fp:
            json.dump(product_data[0], fp, ensure_ascii=False)
        return render_template('download.html')
    
@app.route('/download_csv/<string:id>', methods = ['GET'])
def download_csv(id):
    if request.method == 'GET':
        opinions = generate_product(id)[0]
        with open('ttest.csv', 'w', encoding='utf8') as f:    
            writer = csv.writer(f)
            writer.writerow(['review_id', 'author_name', 'recommendation', 'stars_given', 'verification', 'helpful', 'unhelpful', 'review_content', 'review_date', 'buy_date', 'list_of_pros', 'list_of_cons'])
            for dict in opinions:
                writer.writerow(dict.values())
        return render_template('download.html')

@app.route('/download_xlsx/<string:id>', methods = ['GET'])
def download_xlsx(id):
    if request.method == 'GET':
        opinions = generate_product(id)[0]
        df = pd.DataFrame.from_dict(opinions)
        df.to_excel('opinions.xlsx')
        return render_template('download.html')
    
app.run(host="0.0.0.0", port=80, debug=True)
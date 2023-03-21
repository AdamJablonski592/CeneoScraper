from flask import Flask, render_template, request
from classes.product import Product
import json
import csv
import pandas as pd
import os
from operator import itemgetter

app = Flask(__name__, static_folder="C:\\Users\\AdamJ\\Desktop\\CeneoScraper\\charts_folder")

id_array = []

def generate_product(id):
    new_product = Product(id)
    new_product.new_product_directory()
    soup = new_product.get_product_website()
    amount = new_product.get_page_number(soup)
    opinions = new_product.get_opinions(amount)
    new_product.generate_bar_chart()
    new_product.generate_pie_chart()
    product_data = new_product.return_credentials(opinions, soup)
    return opinions, product_data

def generate_opinion_path(id):
    dirname = os.path.dirname(__file__)
    new_dir = os.path.join(dirname, f"product_data/{id}/opinions")
    return new_dir

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/author")
def author():
    return render_template('author.html')

@app.route("/extraction")
def extraction():
    return render_template('extraction.html')


@app.route('/product_site', methods = ['POST'])
def fetch_data():
    if request.method == 'POST':
        try:
            for key, val in request.form.items():
                product_id = val
            product_data = generate_product(product_id)
            if product_id not in id_array:
                id_array.append(product_id)
            else:
                pass
            return render_template('product_site.html', opinions = product_data[0], product_cred = product_data[1])
        except:
            return render_template('error.html')    
@app.route('/product_site/<string:id>', methods=['GET'])
def fetch_from_id(id):
    if request.method == 'GET':
        product_data = generate_product(id)
        return render_template('product_site.html', opinions = product_data[0], product_cred = product_data[1])
    
@app.route('/products')
def display_products():
    product_array = []
    for id in id_array:
        new_product = generate_product(id)
        product_array.append(new_product[1])
    return render_template('products.html', products=product_array)

@app.route('/download_json/<string:id>', methods = ['GET'])
def download_json(id):
    if request.method == 'GET':
        product_data = generate_product(id)
        with open(f'{generate_opinion_path(id)}/{id}.json', 'w', encoding='utf8') as fp:
            json.dump(product_data[0], fp, ensure_ascii=False)
        return render_template('download.html')
    
@app.route('/download_csv/<string:id>', methods = ['GET'])
def download_csv(id):
    if request.method == 'GET':
        opinions = generate_product(id)[0]
        with open(f'{generate_opinion_path(id)}/{id}.csv', 'w', encoding='utf8') as f:    
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
        df.to_excel(f'{generate_opinion_path(id)}/{id}.xlsx')
        return render_template('download.html')
    
@app.route('/charts/<string:id>', methods=['GET'])
def display_charts(id):
    if request.method == 'GET':
        return render_template('charts.html', id=id)

@app.route('/filter_recomendation', methods=["POST"])
def filter_recomendations():
    if request.method == 'POST':
        arr = []
        select_option = request.form.get('selector')
        product_id = request.form.get('product_id')
        product_data = generate_product(product_id)
        for item in product_data[0]:
            if item['recommendation'] == select_option:
                arr.append(item)
            else:
                pass
        return render_template('product_site.html', opinions = arr, product_cred = product_data[1])
    
@app.route('/filter_parameter', methods=["POST"])
def filter_parameter():
    if request.method == 'POST':
        arr = []
        select_option = request.form.get('selector')
        type = request.form.get('filter_type')
        product_id = request.form.get('product_id')
        product_data = generate_product(product_id)
        for item in product_data[0]:
            if item[f'{type}'] == select_option:
                arr.append(item)
            else:
                pass
        return render_template('product_site.html', opinions = arr, product_cred = product_data[1])

@app.route('/filter_asc_desc', methods=["POST"])
def filter_asc_desc():
    if request.method == 'POST':
        select_option = request.form.get('selector')
        product_id = request.form.get('product_id')
        type = request.form.get('filter_type')
        product_data = generate_product(product_id)
        if select_option == 'desc':
            new_list = sorted(product_data[0], key=itemgetter(f'{type}'), reverse=True)
        elif select_option == 'asc':
            new_list = sorted(product_data[0], key=itemgetter(f'{type}'))
        return render_template('product_site.html', opinions = new_list, product_cred = product_data[1])
    
app.run(host="0.0.0.0", port=80, debug=True)
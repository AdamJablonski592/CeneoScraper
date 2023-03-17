from flask import Flask, render_template
from .classes.product import Product

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')
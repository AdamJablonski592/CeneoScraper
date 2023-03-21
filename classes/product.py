import bs4, requests, re, math
from .extractor import Extractor
from .review import Review
from .charts import GenerateChart
import os

class Product():
    URL = "https://www.ceneo.pl/"
    
    def __init__(self, product_id):
        self.product_id = product_id
    
    def get_product_website(self):
        res = requests.get(self.URL + self.product_id)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        return soup
    
    def get_page_number(self, soup):
        review_amount = soup.find("div", class_="score-extend__review")
        amount = re.findall('\d+', review_amount.getText())
        num_of_pages = math.ceil(int(amount[0]) / 10)
        return num_of_pages
    
    def get_opinions(self, num_of_pages):
        product_reviews = []
        for i in range(1, num_of_pages + 1):
            res = requests.get(f"https://www.ceneo.pl/{self.product_id}/opinie-{i}")
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, 'html.parser')
            my_reviews = soup.find_all("div", class_="js_product-review")
            
            for review in my_reviews:
                review_id = Extractor.get_review_id(review)
                author_name = Extractor.get_review_author(review)
                recommendation = Extractor.get_review_recommendation(review)
                stars_given = Extractor.get_review_stars(review)
                verification = Extractor.get_review_verification(review)
                helpful = Extractor.get_review_helpful(review, review_id)
                unhelpful = Extractor.get_review_unhelpful(review, review_id)
                review_content = Extractor.get_review_content(review)
                review_date = Extractor.get_review_date(review)
                buy_date = Extractor.get_review_buydate(review)
                list_of_pros = Extractor.get_review_pros(review)
                list_of_cons = Extractor.get_review_cons(review)
                
                review_instance = Review(review_id, author_name, recommendation, stars_given, verification, helpful, unhelpful, review_content, review_date, buy_date, list_of_pros, list_of_cons)
                
                product_reviews.append(review_instance.return_data())
        return product_reviews
    
    #get product credentials
    def get_product_pros(self, opinions):
        pros = 0
        for item in opinions:
            for it in item['list_of_pros']:
                pros += 1
        return pros
    
    def get_product_cons(self, opinions):
        cons = 0
        for item in opinions:
            for it in item['list_of_cons']:
                cons += 1
        return cons
    
    def get_product_score(self, soup):
        tag = soup.find("div", class_="fl")
        product_score = Extractor.get_product_score(tag)
        return product_score
    
    def get_product_name(self, soup):
        product_name = Extractor.get_product_name(soup)
        return product_name
    
    
    def return_credentials(self, opinions, soup):
        credentials = {
            'product_id': self.product_id,
            'product_name': self.get_product_name(soup),
            'average_score': self.get_product_score(soup),
            'review_amount': len(opinions),
            'num_of_pros': self.get_product_pros(opinions),
            'num_of_cons': self.get_product_cons(opinions)
        }
        return credentials

    def new_product_directory(self):
        dirname = os.path.dirname(__file__)
        catalog_dir = os.path.join(dirname, "../product_data")
        if not os.path.exists(catalog_dir):
            os.makedirs(catalog_dir)
        new_dir = os.path.join(dirname, f"../product_data/{self.product_id}")
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
            os.makedirs(os.path.join(new_dir, './opinions'))
            os.makedirs(os.path.join(new_dir, './product'))
            
    def generate_bar_chart(self):
        soup = self.get_product_website()
        amount = self.get_page_number(soup)
        opinions = self.get_opinions(amount)
        raw_data = GenerateChart.get_stars_data(opinions)
        chart = GenerateChart.generate_bar_chart(raw_data, self.product_id)
        return chart
    
    def generate_pie_chart(self):
        soup = self.get_product_website()
        amount = self.get_page_number(soup)
        opinions = self.get_opinions(amount)
        raw_data = GenerateChart.get_recommendations_data(opinions)
        chart = GenerateChart.generate_pie_chart(raw_data, self.product_id)
        return chart
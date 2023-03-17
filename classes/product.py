import bs4, requests, re, math
from .extractor import Extractor
from .review import Review

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
            res = requests.get(
                f"https://www.ceneo.pl/{self.product_id}/opinie-{i}")
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
import bs4, requests, re, math
import extractor as ex
import review as rv
import charts as ch

class Product():
    URL = "https://www.ceneo.pl/"
    
    def __init__(self, product_id):
        self.product_id = product_id
    
    def get_product_website(self):
        res = requests.get(self.URL + self.product_id)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        return soup
    
    def get_review_pages(self, soup):
        amount_tag = soup.find("div", class_="score-extended__review")
        amount = re.findall('\d+', amount_tag.getText())
        num_of_pages = math.ceil(int(amount[0]) / 10)
        return num_of_pages
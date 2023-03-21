class Extractor():
    
    #extractor methods for review parameters
    @staticmethod
    def get_review_id(review):
        div_attributes = review.attrs
        review_id = div_attributes['data-entry-id']
        return review_id
    
    @staticmethod
    def get_review_author(review):
        author_name = review.find("span", class_="user-post__author-name").text
        return author_name.strip('\n')
    
    @staticmethod
    def get_review_recommendation(review):
        recommendation = review.find("span", class_="user-post__author-recomendation")
        if recommendation is not None:
            return (recommendation.text).strip('\n')
        else:
            return ""
    
    @staticmethod
    def get_review_stars(review):
        stars_given = review.find(
            "span", class_="user-post__score-count").text
        return stars_given
    
    @staticmethod
    def get_review_verification(review):
        verified = review.find("div", class_="review-pz")
        if verified is not None:
            return "Opinia zweryfikowana"
        else:
            return "Opinia niezweryfikowana"
        
    @staticmethod
    def get_review_helpful(review, review_id):
        helpful = review.find("span", {"id": f"votes-yes-{review_id}"}).text
        return helpful
    
    @staticmethod
    def get_review_unhelpful(review, review_id):
        unhelpful = review.find("span", {"id": f"votes-no-{review_id}"}).text
        return unhelpful
    
    @staticmethod
    def get_review_content(review):
        review_content = review.find("div", class_="user-post__text").text
        return review_content
    
    @staticmethod
    def get_review_date(review):
        timedates = review.find("span", class_="user-post__published").findAll("time")
        review_date = timedates[0].attrs["datetime"]
        return review_date
    
    @staticmethod
    def get_review_buydate(review):
        timedates = review.find("span", class_="user-post__published").findAll("time")
        if len(timedates) == 2:
            buy_date = timedates[1].attrs['datetime']
        else:
            buy_date = ""
        return buy_date
    
    @staticmethod
    def get_review_pros(review):
        list_of_pros = []
        review_feature = review.find("div", class_="review-feature")
        if review_feature is not None:
            all_tags = review_feature.findAll("div", class_="review-feature__col")
            for item in all_tags:
                review_tag = item.find("div", class_="review-feature__title--positives")
                if review_tag is not None:
                    review_items = item.findAll("div", class_="review-feature__item")
                    for r_item in review_items:
                        list_of_pros.append(r_item.text)
                else:
                    pass
        else:
            list_of_pros = []
        return list_of_pros
    
    @staticmethod
    def get_review_cons(review):
        list_of_cons = []
        review_feature = review.find("div", class_="review-feature")
        if review_feature is not None:
            all_tags = review_feature.findAll("div", class_="review-feature__col")
            for item in all_tags:
                review_tag = item.find("div", class_="review-feature__title--negatives")
                if review_tag is not None:
                    review_items = item.findAll("div", class_="review-feature__item")
                    for r_item in review_items:
                        list_of_cons.append(r_item.text)
                else:
                    pass
        else:
            list_of_cons = []
        return list_of_cons
    
    #extractor methods for product parameters
    @staticmethod
    def get_product_name(tag):
        product_name = tag.find("h1", class_="product-top__product-info__name").text
        return product_name
    
    @staticmethod
    def get_product_score(tag):
        average_score = tag.find("font").text
        return average_score
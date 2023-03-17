class Review():
    
    def __init__(self, review_id, author_name, recommendation, stars_given, verification, helpful, unhelpful, review_content, review_date, buy_date, list_of_pros, list_of_cons):
        self.review_id = review_id
        self.author_name = author_name
        self.recommendation = recommendation
        self.stars_given = stars_given
        self.verification = verification
        self.helpful = helpful
        self.unhelpful = unhelpful
        self.review_content = review_content
        self.review_date = review_date
        self.buy_date = buy_date
        self.list_of_pros = list_of_pros
        self.list_of_cons = list_of_cons
        
    def return_data(self):
        dict = {
            'review_id': self.review_id,
            'author_name': self.author_name,
            'recommendation': self.recommendation,
            'stars_given': self.stars_given,
            'verification': self.verification,
            'helpful': self.helpful,
            'unhelpful': self.unhelpful,
            'review_content': self.review_content,
            'review_date': self.review_date,
            'buy_date': self.buy_date,
            'list_of_pros': self.list_of_pros,
            'list_of_cons': self.list_of_cons
        }
        return dict
        
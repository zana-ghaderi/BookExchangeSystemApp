# Review and Rating System
from datetime import datetime


class Review:

    def __init__(self, review_id, reviewer, reviewee, rating, comment, exchange):
        self.review_id = review_id
        self.exchange = exchange
        self.rating = rating
        self.comment = comment
        self.reviewer = reviewer
        self.reviewee = reviewee
        self.created_at = datetime.now()


    def leave_review(self):
        # Code to leave a review for the exchange
        pass

    @staticmethod
    def get_reviews_for_user(user_id):
        # Code to get all reviews for a user
        pass
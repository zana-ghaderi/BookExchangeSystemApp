class ReviewService:
    def __init__(self):
        self.reviews = {}

    def add_review(self, review):
        self.reviews[review.review_id] = review
        return review

    def get_user_reviews(self, user_id):
        return [review.rating for review in self.reviews.values() if review.reviewee.user_id == user_id]

    def calculate_user_average_rating(self, user_id):
        user_ratings = self.get_user_reviews(user_id)
        if user_ratings:
            return sum(user_ratings) / len(user_ratings)
        return 0.0
from datetime import datetime

import requests
import dateutil.parser

from scripts.feedback import Feedback

#Get reviews from public airbnb api call and append them to list.

def get_airbnb_feedback(client_id, listing_id, number=100, offset=0):
    airbnb_listing = 'https://api.airbnb.com/v2/reviews?client_id=' + str(client_id) + '&listing_id=' + str(listing_id) + '&role=all&_limit=' + str(number) + '&_offset=' + str(offset)
    apartment_airbnb_reviews = requests.get(airbnb_listing).json()
    apartment_airbnb_reviews_list = apartment_airbnb_reviews['reviews']
    feedbacks = []
    for review in apartment_airbnb_reviews_list:
        feedback = Feedback(
            review['author']['first_name'], dateutil.parser.parse(review['created_at']), review['comments'], "apartment-airbnb")
        feedbacks.append(feedback)
    return feedbacks
#!/usr/bin/env python3
import scripts.guest_feedback
from datetime import datetime
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#*****Amount of airbnb reviews*************

client_id = "" #Client id from api url
listing_id = "" #Listing id from api url
number = 100 #max 100
offset = 0 #what number review to start from, for instance 2 will start from the second review


#******************************************



feedbacks = scripts.guest_feedback.get_airbnb_feedback(client_id, listing_id, number, offset)
now = datetime.now().strftime("%d-%m-%Y")
with open(os.path.join(__location__, "guest-feedback-{}".format(str(now))), "w+") as file:
    for feedback in feedbacks:
        file.write("{} \n \n".format(str(feedback)))
file.close()

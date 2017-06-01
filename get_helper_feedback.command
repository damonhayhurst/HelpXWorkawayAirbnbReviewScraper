#!/usr/bin/env python3
import scripts.helper_feedback
from datetime import datetime
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

#****HelpX login details**********


helpx_email = "" #Add helpx email login here
helpx_password = ""  #Add helpx password here
helpx_host_id = ""


#****Workaway host id**************

workaway_host_id = ""

#**********************************


feedbacks = scripts.helper_feedback.get_helper_feedback(helpx_email, helpx_password)
now = datetime.now().strftime("%d-%m-%Y")
with open(os.path.join(__location__, "helper-feedback-{}".format(str(now))), "w+") as file:
    for feedback in feedbacks:
        file.write("{} \n \n".format(str(feedback)))
file.close()
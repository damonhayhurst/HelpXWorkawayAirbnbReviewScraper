from datetime import datetime

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup

from scripts.feedback import Feedback

#Scrapes helpx site for reviews (login required)

def get_helpx_feedback(email, password, host_id):
    base_url = "https://www.helpx.net/sign-in.asp"
    browser = RoboBrowser(history=True)
    browser.open(base_url)
    form = browser.get_form(action="sign-in-host-st.asp")
    form["login_email"] = email
    form["login_pwd"] = password
    browser.submit_form(form)
    browser.open("http://www.helpx.net/host.asp?hostid=" + str(host_id))
    try:
        soup = BeautifulSoup(str(browser.select))
        reviewstop = soup.find_all(attrs={"name":"reviewstop"})
        reviewstopsoup = BeautifulSoup(str(reviewstop))
        tablerows = reviewstopsoup.find_all("tr")
        name = ""
        date = ""
        comment = ""
        feedbacks = []
        i = 0
        for row in tablerows:
            rowsoup = BeautifulSoup(str(row))
            if rowsoup.form == None:
                if i == 1:
                    rowsoup.span.decompose()
                    name = rowsoup.td.text
                if i == 2:
                    rowsoup.span.decompose()
                    columns = rowsoup.find_all("td")
                    date = columns[1].contents[2]
                if i == 3:
                    comment = rowsoup.text
                if i == 4:
                    date_object = datetime.strptime(date.strip(), '%B %d, %Y')
                    feedbacks.append(Feedback(name.strip(), date_object, comment.strip(), "HelpX"))
                    name = ""
                    date = ""
                    comment = ""
                    i = 0
            i = i + 1
        return feedbacks
    except (TypeError):
        print("Could not get helpx feedback. Maybe the login failed or the website layout has changed?")
        return []

#Scrapes workaway reviews from the site

def get_workaway_feedback(host_id):
    base_url = "https://www.workaway.info/"+ str(host_id) + "-en.html"
    browser = RoboBrowser(history=True)
    browser.open(base_url)
    try:
        soup = BeautifulSoup(str(browser.select))
        rows = soup.find_all("div", attrs={"class":"row"})
        feedbacks = []
        for row in rows:
            row_soup = BeautifulSoup(str(row))
            if row_soup.find(attrs={"class":"feedback_content_ww"}) != None:
                feedback_soup = BeautifulSoup(str(row_soup.find(attrs={"class":"feedback_content_ww"})))
                author = row_soup.find(attrs={"class":"feedback_left_by"})
                author_text = str(author.text).replace(" by ", "").strip()
                date = feedback_soup.find(attrs={"class":"small"})
                date_text = str(date.text).replace("[", "").replace("]", "").strip()
                date_object = datetime.strptime(str(date_text), '%d/%m/%Y')
                comment = feedback_soup.find(attrs={"class":"feedback_msg_ww"})
                comment_text = str(comment.text).strip()
                feedbacks.append(Feedback(str(author_text), date_object, comment_text, "Workaway"))
        return feedbacks
    except (TypeError):
        print("Could not get workaway feedback. Maybe the website layout has changed?")
        return []

#Gets reviews from helpx and workaway and sorts them

def get_helper_feedback(helpx_email, helpx_password, helpx_host_id, workaway_host_id):
    feedbacks = get_workaway_feedback(workaway_host_id) + get_helpx_feedback(helpx_email, helpx_password, helpx_host_id)
    sorted_feedbacks = sorted(feedbacks, key=lambda feedback:feedback.date, reverse=True)
    return sorted_feedbacks
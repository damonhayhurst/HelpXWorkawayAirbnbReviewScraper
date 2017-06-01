import textwrap

#Class for storing Feedbacks with date and source.

class Feedback(object):

    def __init__(self, name, date, comment, source):
        self.name = name
        self.date = date
        self.comment = comment
        self.source = source

    def __str__(self):
        return "{}\n{}\n{}\n{}".format(
            self.name, self.date.strftime('%B %d, %Y'), self.source, textwrap.fill(self.comment, 70))
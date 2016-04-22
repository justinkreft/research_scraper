__author__ = 'justinkreft'

import sqlite3


class Comment:
    def __init__(self, scraped_comment_url, project_title, comment_title, comment_date, comment_text):
        self.scraped_comment_url = scraped_comment_url
        self.project_title = project_title
        self.comment_title = comment_title
        self.comment_date = comment_date
        self.comment_text = comment_text


    def insert_into_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        print "Inserting record: " + self.scraped_comment_url[0:20] + "... " + self.project_title[0:20] + "... " + self.comment_text[0:20] + "... "
        conn.execute("INSERT INTO scraped_comments (scraped_comment_url, project_title, comment_title, comment_date, comment_text) VALUES (?, ?, ?, ?, ?);", (self.scraped_comment_url, self.project_title, self.comment_title, self.comment_date, self.comment_text))
        conn.commit()
        conn.close()


    def is_in_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        out_query = conn.execute("SELECT COUNT(*) FROM scraped_comments WHERE scraped_comment_url = (?) AND comment_date = (?);", (self.scraped_comment_url, self.comment_date))
        for row in out_query:
            count = int(row[0])
        if count > 0:
            check = True
        else:
            check = False
        conn.commit()
        conn.close()

        return check
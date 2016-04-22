__author__ = 'justinkreft'

import sqlite3


class Update:
    def __init__(self, scraped_update_url, project_title, update_title, update_date, update_text):
        self.scraped_update_url = scraped_update_url
        self.project_title = project_title
        self.update_title = update_title
        self.update_date = update_date
        self.update_text = update_text


    def insert_into_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        print "Inserting record: " + self.scraped_update_url[0:20] + "... " + self.project_title[0:20] + "... " + self.update_text[0:20] + "... "
        conn.execute("INSERT INTO scraped_updates (scraped_update_url, project_title, update_title, update_date, update_text) VALUES (?, ?, ?, ?, ?);", (self.scraped_update_url, self.project_title, self.update_title, self.update_date, self.update_text))
        conn.commit()
        conn.close()


    def is_in_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        out_query = conn.execute("SELECT COUNT(*) FROM scraped_updates WHERE scraped_update_url = (?) AND update_date = (?);", (self.scraped_update_url, self.update_date))
        for row in out_query:
            count = int(row[0])
        if count > 0:
            check = True
        else:
            check = False
        conn.commit()
        conn.close()

        return check
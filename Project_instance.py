__author__ = 'justinkreft'

import sqlite3


class Project_instance:
    def __init__(self, scraped_project_url, project_title, date_scraped, days_left, current_investors, current_raised, project_goal, location, category, phase, full_scraped_description, funded):
        self.scraped_project_url = scraped_project_url
        self.project_title = project_title
        self.date_scraped = date_scraped
        self.days_left = days_left
        self.current_investors = current_investors
        self.current_raised = current_raised
        self.project_goal = project_goal
        self.location = location
        self.category = category
        self.phase = phase
        self.full_scraped_description = full_scraped_description
        self.funded = funded


    def insert_into_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        print "Inserting record: " + self.scraped_project_url[0:20] + "... " + self.project_title[0:20] + "... "
        conn.execute("INSERT INTO scraped_projects_data (scraped_project_url, project_title, date_scraped, days_left, current_investors, current_raised, project_goal, location, category, phase, full_scraped_description, funded) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (self.scraped_project_url, self.project_title, self.date_scraped, self.days_left, self.current_investors, self.current_raised, self.project_goal, self.location, self.category, self.phase, self.full_scraped_description, self.funded))
        conn.commit()
        conn.close()


    def is_in_database(self):
        conn = sqlite3.connect("research_data.db")
        conn.text_factory = str
        out_query = conn.execute("SELECT COUNT(*) FROM scraped_projects_data WHERE scraped_project_url = (?) AND current_raised = (?) AND funded = 'Funded!';", (self.scraped_project_url, self.current_raised))
        for row in out_query:
            count = int(row[0])
        if count > 0:
            check = True
        else:
            check = False
        conn.commit()
        conn.close()

        return check
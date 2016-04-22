__author__ = 'justinkreft'

import urllib2
import time
import re
from BeautifulSoup import BeautifulSoup
from Comment import *
from Update import *
from Project_instance import *

#Test URLS
#URL1 = "http://www.citizinvestor.com/project/3-months-of-bicycle-sundays/"
#URL2 = "http://www.citizinvestor.com/project/3-months-of-bicycle-sundays/comments"
#URL3 = "http://www.citizinvestor.com/project/summer-heatwave-/updates"

def main():
    print
    print "Hello, Audrey. Would you like to:"
    print
    print "1) Print a list of Projects currently being tracked?"
    print "2) Add a new http/url to the list of tracked Projects?"
    print "3) Execute a daily scrape?"
    print
    choice = input("Enter 1, 2 or 3: ")
    if choice == 1:
        print
        print_tracked_projects()
    elif choice == 2:
        print
        insert_tracked_project()
    else:
        print
        run_scraper()
    print
    print "Process complete."
    print
    choice = input("1) Continue with another action, or 2) Exit program ")
    if choice == 1:
        print
        main()

def check_valid_url(url):
    if "http://www.citizinvestor.com/project/" in url:
        print
        print ("{0} is valid domain").format(url.strip())
        if "comment" in url or "update" in url:
            print ("{0} is a comments or update url, please enter in the project page url").format(url.strip())
            check = False
        else:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page)
            project_title = str(soup.find("div", { "class" : "container"}))
            project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
            project_title = text_stripper(project_title, project_title_strip)
            if project_title == "Project not found":
                print ("{0} returns a 'Project not found' error. Please check for valid project address").format(url.strip())
                check = False
            else:
                print ("{0} is valid project").format(url.strip())
                check = True
    else:
        print
        print ("{0} is an invalid domain").format(url.strip())
        print "Valid URL must begin with 'http://www.citizinvestor.com/project/' + the project page"
        print "For example 'http://www.citizinvestor.com/project/tyler-animal-care-facility/"
        check = False

    return check

def insert_tracked_project():
    project_url = raw_input("Please insert the full url of the new project you would like to track: ")
    project_url = project_url.strip("/")
    project_url = project_url + "/"
    check = check_valid_url(project_url)
    if check == False:
        print
        print "File not inserted"
    else:
        check = read_file("projects_list.txt")
        if project_url + "\n" in check:
            print "This Project is already being tracked"
        else:
            project_url = "\n" + project_url
            comment_url = project_url + "comments"
            update_url = project_url + "updates"
            update_file("projects_list.txt", project_url)
            update_file("comments_list.txt", comment_url)
            update_file("updates_list.txt", update_url)

def print_tracked_projects():
    projects_list = read_file("projects_list.txt")
    out_list = []
    for http in projects_list:
        out_project = http.replace("http://www.citizinvestor.com/project/","")
        out_project = out_project.strip()
        out_project = out_project.replace("/","")
        out_project = out_project.replace("-"," ")
        out_list.append(out_project)
    print "CURRENT PROJECTS BEING TRACKED"
    print
    out_list = sorted(out_list)
    for item in out_list:
        print item.title()

def run_scraper():
    #Scrape Project http list
    projects_list = read_file("projects_list.txt")
    project_total = 0
    for http in projects_list:
        count = scrape_project(http)
        project_total += count
    print
    print "{0} project records found and inserted.".format(project_total)
    #Scrape Comment http list
    comments_list = read_file("comments_list.txt")
    comment_total = 0
    for http in comments_list:
        count = scrape_comment(http)
        comment_total += count
    print
    print "{0} new comment records found and inserted.".format(comment_total)
    #Scrape Update http list
    updates_list = read_file("updates_list.txt")
    update_total = 0
    for http in updates_list:
        count = scrape_update(http)
        update_total += count
    print
    print "{0} project records found and inserted.".format(project_total)
    print "{0} new comment records found and inserted.".format(comment_total)
    print "{0} new update records found and inserted.".format(update_total)
    print
    print "The following pages returned 'Project Not Found'"
    list = read_file("page_not_found.txt")
    if len(list) > 0:
        for item in list:
            print item.strip()
        print
        choice = input("Would you like to 1) remove these from the que in the future (cannot be undone) or 2) keep them? ")
        print
        if choice == 1:
            for line in list:
                remove_line(line,"projects_list.txt")
                remove_line(line,"updates_list.txt")
                remove_line(line,"comments_list.txt")
            out_file = open("page_not_found.txt", "w")
            out_file.write("")
            out_file.close()
    else:
        print "None"



def scrape_update(url):
    print
    print ("Scraping {0}").format(url.strip())
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    scraped_update_url = url
    project_title = str(soup.find("div", { "class" : "container"}))
    project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
    project_title = text_stripper(project_title, project_title_strip)
    if project_title == "Project not found":
        out_url = url.strip() + "\n"
        print url.strip() + " is an invalid url or the project has been removed from the domain."
        insert_count = 0
        update_file("page_not_found.txt", out_url)
    else:
        project_title = str(soup.find("div", { "class" : "container"}))
        project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
        project_title = text_stripper(project_title, project_title_strip)
        project_title = regex_strip(project_title, r"(.*?)<.*")
        print "Project Title: " + project_title
        update_list = soup.findAll("div", { "class" : "update-box"})
        insert_count = 0
        for update in update_list:
            strip = ["\n"]
            strip_update = text_stripper(str(update), strip)
            strip = r".*?>.*?>(.*?)<.*"
            update_title = regex_strip(strip_update, strip)
            strip = r".*?>.*?>.*?>(.*?)<.*"
            update_date = regex_strip(strip_update, strip)
            update_strip = ["\n", "on"]
            update_date = text_stripper(update_date, update_strip)
            strip = r".*?>.*?>.*?>.*?>.*?>(.*)"
            update_text = regex_strip(strip_update, strip)
            update_text_strip = ['\n', "<br />", "<p>", "</p>", "</div>"]
            update_text = text_stripper(update_text, update_text_strip)
            out_update = Update(scraped_update_url, project_title, update_title, update_date, update_text)
            check = out_update.is_in_database()
            if check == False:
                print "Inserting {0} into database.".format(out_update.update_title)
                out_update.insert_into_database()
                insert_count += 1
            else:
                print "'{0}' update already in database.".format(out_update.update_title)
    return insert_count


def scrape_comment(url):
    print
    print ("scraping {0}").format(url.strip())
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    scraped_comment_url = url
    project_title = str(soup.find("div", { "class" : "container"}))
    project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
    project_title = text_stripper(project_title, project_title_strip)
    if project_title == "Project not found":
        out_url = url.strip() + "\n"
        print url.strip() + " is an invalid url or the project has been removed from the domain."
        insert_count = 0
        update_file("page_not_found.txt", out_url)
    else:
        project_title = str(soup.find("div", { "class" : "container"}))
        project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
        project_title = text_stripper(project_title, project_title_strip)
        project_title = regex_strip(project_title, r"(.*?)<.*")
        print "Project Title: " + project_title
        comment_list = soup.findAll("div", { "class" : "comment"})
        insert_count = 0
        for comment in comment_list:
            strip = ["\n"]
            strip_comment = text_stripper(str(comment), strip)
            if "img width=" in strip_comment:
                strip = r".*?>.*?>.*?>.*?>.*?>(.*?)<.*"
                comment_title = regex_strip(strip_comment, strip)
                strip = r".*?>.*?>.*?>.*?>.*?>.*?>.*?>(.*?)<.*"
                comment_date = regex_strip(strip_comment, strip)
                strip = r".*?>.*?>.*?>.*?>.*?>.*?>.*?>.*?>.*?>(.*)"
                comment_strip = ["\n", "on"]
                comment_date = text_stripper(comment_date, comment_strip)
                comment_text = regex_strip(strip_comment, strip)
                comment_text_strip = ['\n', "<br />", "<p>", "</p>", "</div>"]
                comment_text = text_stripper(comment_text, comment_text_strip)
                out_comment = Comment(scraped_comment_url, project_title, comment_title, comment_date, comment_text)
                check = out_comment.is_in_database()
                if check == False:
                    print "Inserting {0} into database.".format(out_comment.comment_title)
                    out_comment.insert_into_database()
                    insert_count += 1
                else:
                    print "'{0}' comment already in database.".format(out_comment.comment_title)
    return insert_count


def scrape_project(url):
    print
    print ("Scraping {0}").format(url.strip())
    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page)
    scraped_project_url = url
    project_title = str(soup.find("div", { "class" : "container"}))
    project_title_strip = ['\n', "<div class=\"container\"><h1>", "</h1></div>"]
    project_title = text_stripper(project_title, project_title_strip)
    print "Project Title: " + project_title
    if project_title == "Project not found":
        out_url = url.strip() + "\n"
        print url.strip() + " is an invalid url or the project has been removed from the domain."
        insert_count = 0
        update_file("page_not_found.txt", out_url)
    else:
        date_scraped = time.strftime("%Y-%m-%d")
        days_left = str(soup.find("div", { "class" : "days-left"}))
        days_left_strip = ['\n', "<div class=\"days-left\"><span class=\"number\">", "</span><span class=\"text\">Days Left</span></div>"]
        days_left = text_stripper(days_left, days_left_strip)
        current_investors = str(soup.find("div", { "class" : "number-of-investors"}))
        current_investors_strip = ['\n', "<div class=\"number-of-investors\"><span class=\"number\">", "</span><span class=\"text\">citizinvestors</span></div>"]
        current_investors = text_stripper(current_investors, current_investors_strip)
        current_raised_and_project_goal = str(soup.find("div", { "class" : "amount"}))
        current_raised_and_project_goal = BeautifulSoup(current_raised_and_project_goal)
        current_raised = str(current_raised_and_project_goal.find("span", { "class" : "number"}))
        current_raised_strip = ['\n', "<span class=\"number\">$", "</span>", ","]
        current_raised = text_stripper(current_raised, current_raised_strip)
        project_goal = str(current_raised_and_project_goal.find("span", { "class" : "text"}))
        project_goal_strip = ['\n', "<span class=\"text\">out of $", "required</span>", ","]
        project_goal = text_stripper(project_goal, project_goal_strip)
        location = str(soup.find("h4", { "class" : "location-span"}))
        location_strip = ['\n']
        location = text_stripper(location, location_strip)
        strip = r".*?>.*?>(.*?)<.*"
        location = regex_strip(location, strip)
        category = str(soup.find("h5", { "class" : "category-span"}))
        category_strip = ['\n']
        category = text_stripper(category, category_strip)
        strip = ".*?>.*?>.*?>.*?>(.*?)<.*"
        category = regex_strip(category, strip)
        phase = str(soup.find("h4", { "class" : "project_type-span"}))
        phase_strip = ['\n', "<h4 class=\"project_type-span\">", "</h4>"]
        phase = text_stripper(phase, phase_strip)
        full_scraped_description = str(soup.find("div", { "style" : "margin-bottom: 10px;"}))
        full_scraped_description_strip = ['\n', "<div style=\"margin-bottom: 10px;\">", "<p>", "</p>", "</div>"]
        full_scraped_description = text_stripper(full_scraped_description, full_scraped_description_strip)
        funded = str(soup.find("div", { "class" : "funded"}))
        funded_strip = ['\n', "<div class=\"funded\"><span>", "</span></div>"]
        funded = text_stripper(funded, funded_strip)
        project = Project_instance(scraped_project_url, project_title, date_scraped, days_left, current_investors, current_raised, project_goal, location, category, phase, full_scraped_description, funded)
        insert_count = 0
        check = project.is_in_database()
        if check == False:
            print "{0} is active. Inserting capture record into database.".format(project_title)
            project.insert_into_database()
            insert_count += 1
        else:
            print "'{0}' project is 'Funded' and no changes were detected.".format(project.project_title)

    return insert_count

def regex_strip(string, regex):
    match = re.search(regex, string)
    out_string = match.group(1)
    return out_string


def text_stripper(string, list):
    if string == "None":
        string = ''
    for item in list:
        string = string.replace(item,'')
    string = string.strip()
    if string == "None":
        string = ''
    return string

def update_file(file, url):
    output_file = open(file, "a")
    write_url = url.strip()
    output_file.write(write_url + "\n")
    output_file.close()

def read_file(filename):
    in_file = open(filename, "r")
    file_contents = in_file.readlines()
    in_file.close()
    return file_contents

def print_file(filename):
    in_file = read_file(filename, "r")
    for line in in_file:
        print line.strip()

def remove_line(line, filename):
    in_file = open(filename, "r")
    file_contents = in_file.read()
    in_file.close()
    if line in file_contents:
        file_contents = file_contents.replace(line, "")
        print "Printing current scrape que for " + filename
        print file_contents
    out_file = open(filename, "w")
    out_file.write(file_contents)
    out_file.close()

main()
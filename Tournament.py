import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from Team import *
import random
import gspread
import csv
from datetime import date

class Tournament():
    def __init__(self,URL,event,googleSheetLink,sheetTabName):
        self.url = URL

        if(event == 'CX'):
            self.wiki = "https://opencaselist.com/hspolicy24"
        if(event == 'LD'):
            self.wiki = "https://opencaselist.com/hsld24"
        self.teams = []

        gc = gspread.service_account()
        sh = gc.open_by_url(googleSheetLink)
        self.worksheet = sh.worksheet(sheetTabName)
    
    def findTeams(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")
        table = soup.find("table", id="fieldsort")

        names = []
        schools = []
        codes = []
        links = []

        for a in table.find_all("tr"):
            i = 0
            school = ""
            for b in a.find_all("td"):
                if(i == 0):
                    school = b.text.strip()
                    schools.append(school)
                if(i == 2):
                    name = b.text.strip()
                    names.append(name)
                if(i == 3):
                    code = b.text.strip()
                    if code == "TBA":
                        codes.append(school + " TBA")
                    else:
                        codes.append(code)
                if i == 4:
                    # Extract the <a> tag and get its href attribute
                    link_tag = b.find("a")
                    if link_tag and link_tag.has_attr("href"):
                        link = link_tag["href"]
                        links.append("www.tabroom.com"+link)
                    else:
                        links.append("")
                i = i + 1

        schoolFixer = {"Poly Prep Country Day":"Poly Prep Country Day School",
                    "Poly Prep":"Poly Prep Country Day School",
                    "Barstow":"Barstow School",
                    "NSU":"NSU University School",
                    "Quarry Lane":"The Quarry Lane School",
                    "Greenhill":"Greenhill School",
                    "Northside College Prep":"Northside College Preparatory",
                    "Pace":"Pace Academy",
                    "Thomas Kelly":"Thomas Kelly College Prep",
                    "Univ Of Chicago Lab":"Univ Of Chicago Lab School",
                    "Baltimore City": "BCC",
                    "Baltimore City College":"BCC",
                    "Banneker": "Benjamin Banneker",
                    "Boston Latin": "Boston Latin Academy",
                    "Bronx Science": "Bronx Science",
                    "Brooklyn Technical HS Independent": "Brooklyn Technical",
                    "Calvert Hall": "Calvert Hall College",
                    "Collegiate": "Collegiate School",
                    "Duke Ellington": "Duke Ellington School of the Arts",
                    "Eleanor Roosevelt": "Eleanor Roosevelt",
                    "Fenway": "Fenway",
                    "Georgetown Day": "Georgetown Day School",
                    "Lexington": "Lexington",
                    "McDonogh": "McDonogh",
                    "Newark Science": "Newark Science",
                    "Newark Tech": "Newark Tech",
                    "Northstar Academy HS - Newark": "Northstar Academy High School - Newark",
                    "Somerville": "Somerville",
                    "Success Academy HSLA - MANHATTAN": "Success Academy",
                    "SWW": "School Without Walls",
                    "Unionville": "Unionville",
                    "Alpharetta": "Alpharetta",
                    "Avery Coonley":"The Avery Coonley School",
                    "Bronx Science": "Bronx Science",
                    "Brophy": "Brophy College Prep",
                    "Caddo Magnet": "Caddo Magnet",
                    "Canyon Crest": "Canyon Crest Academy",
                    "Carrollton School of the Sacred Heart": "Carrollton Sacred Heart",
                    "Chicago Bulls":"Chicago Bulls College Prep",
                    "College Prep": "College Prep",
                    "Collegiate": "Collegiate School",
                    "Coppell": "Coppell",
                    "Dallas Highland Park": "Dallas Highland Park",
                    "Damien-St.Lucy's": "Damien - St Lucys",
                    "Decatur": "Decatur",
                    "Denmark Independent": "Denmark",
                    "Eastside": "Eastside",
                    "Galloway": "Galloway",
                    "Georgetown Day": "Georgetown Day",
                    "Glenbrook North": "Glenbrook North",
                    "Glenbrook South": "Glenbrook South",
                    "Greenhill": "Greenhill School",
                    "Head-Royce": "Head-Royce",
                    "Isidore Newman": "Isidore Newman School",
                    "Jesuit": "Jesuit Dallas",
                    "Johns Creek": "Johns Creek",
                    "Kenwood": "Kenwood Academy",
                    "Lexington": "Lexington",
                    "Liberal Arts and Science": "Liberal Arts and Science Academy",
                    "Marist": "Marist School",
                    "Montgomery Bell": "Montgomery Bell Academy",
                    "Northside College Prep": "Northside College Preparatory",
                    "NSU": "NSU University School",
                    "Pace": "Pace Academy",
                    "Sonoma": "Sonoma Academy",
                    "St Andrew's Episcopal": "St Andrews Episcopal School",
                    "Taipei American": "Taipei American School",
                    }
        tabSchools = schoolFixer.keys()
        for n in range(len(schools)):
            school = schools[n]
            if school in tabSchools:
                schools[n] = schoolFixer[school]

        for n in range(len(names)):
            team = names[n].replace(" &","")
            space = team.index(" ")
            code = team[:2]+team[space+1:space+3]
            school = schools[n].replace(" ","")
            print(str(n) + ": " + school + " " + code)
            target_url = f"{self.wiki}/{school}/{code}"
            newTeam = Team(codes[n],school + " " + code,names[n],target_url,links[n])
            self.teams.append(newTeam)
    
    def loadTeamsCSV(self,dir):
        data_list = []
        try:
            with open(dir, 'r') as file:
                csv_reader = csv.reader(file)
                for row in csv_reader:
                    try:
                        data_list.append(row[0])
                    except IndexError:
                        print("IndexError: Column index out of range")
                        return []
        except FileNotFoundError:
            print(f"FileNotFoundError: The file '{dir}' was not found.")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
        for name in data_list:
            print(name)
            args = name.split(" ")
            team = args[1]+" "+args[2]
            code = team[:2]+args[2][:2]
            school = args[0]
            target_url = f"{self.wiki}/{school}/{code}"
            newTeam = Team(school+" "+args[1][0]+args[2][0],school + " " + code,args[1]+" & "+args[2],target_url," ")
            self.teams.append(newTeam)
    
    def pushTeams(self):
        n = 3
        i = 0
        for team in self.teams:
            if(n==32):
                n = 0
                i+=1
                time.sleep(60)
            self.worksheet.update_acell(f"A{str((i*32) + n)}",f'=HYPERLINK("{team.tab}", "{team.name}")')
            self.worksheet.update_acell(f"B{str((i*32) + n)}",f'=HYPERLINK("{team.wikiLink}", "Wiki")')
            n = n+1
    
    def findArgs(self,*args):
        
        args = list(args)
        if(len(args) == 0):
            start = 0
            stop = len(self.teams) - 1
        elif(len(args) == 1):
            start = 0
            stop = args[0]
        elif(args[1] == "END"):
            start = args[0]
            stop = len(self.teams) - 1
        else:
            start = args[0]
            stop = args[1]
        
        # Set up Selenium WebDriver (Chrome here)
        driver = webdriver.Chrome()  # Make sure ChromeDriver is installed

        # Navigate to login page
        driver.get(self.wiki)

        # Locate and fill the login form fields
        driver.find_element(By.NAME, "username").send_keys("batliz27@polyprep.org")  # Update with the actual field name and your username
        driver.find_element(By.NAME, "password").send_keys("password")  # Update with the actual field name and your password)
        driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)  # Submit the form

        # Allow time for the page to load
        time.sleep(2)  # Adjust sleep duration as needed
        for team in self.teams[start:stop]:
            fromFile = loadTeam(team.wiki)
            if(fromFile == None):
                team.parseWiki(driver)
            #elif(abs(datetime.strptime((date.today().strftime("%m %d %Y"), "%m %d %Y") - team.lastUpdated).days) > 14):
                #team.parseWiki(driver)
            else:
                team.importArgs(fromFile)
        # Close the browser
        driver.quit()

    def pushArgs(self, *args):

        args = list(args)
        if(len(args) == 0):
            start = 0
            stop = len(self.teams) - 1
        elif(len(args) == 1):
            start = 0
            stop = args[0]
        elif(args[1] == "END"):
            start = args[0]
            stop = len(self.teams) - 1
        else:
            start = args[0]
            stop = args[1]

        all = []
        for team in self.teams[start:stop]:
            team.sort()
            team.printInfo()
            row = []

            if(len(team.aff)>0):
                for n in range(4):
                    if(n<len(team.aff)):
                        row.append(team.aff[n])
                    else:
                        row.append("")
                if(len(team.aff)>4):
                    row.append("\n".join(team.aff[4:]))
                else:
                    row.append("")
                row.append("")
                row.append("")
                members = ["Zahaan","Eric","Ava","Sasha"]
                row.append(random.choice(members[1:]))
            else:
                for n in range(5):
                    row.append("")
                row.append("No Disclo")
                row.append("")
                row.append("")
            row.append("")
            row.append("")
            row.append("")
            

            if(len(team.neg)>0):
                for n in range(4):
                    if(n<len(team.neg)):
                        row.append(team.neg[n])
                    else:
                        row.append("")
                if(len(team.neg)>4):
                    row.append("\n".join(team.neg[4:]))
                else:
                    row.append("")
                row.append("\n".join(team.negCol))
            else:
                for n in range(5):
                    row.append("")
                row.append("No Disclo")

            all.append(row)
        
        if(len(self.teams[start:stop]) > 0):
            self.worksheet.update(all,f"C{start+3}:S{stop+3}")


    def printArgs(self, *args):

        args = list(args)
        if(len(args) == 0):
            start = 0
            stop = len(self.teams) - 1
        elif(len(args) == 1):
            start = 0
            stop = args[0]
        elif(args[1] == "END"):
            start = args[0]
            stop = len(self.teams) - 1
        else:
            start = args[0]
            stop = args[1]

        all = []
        for team in self.teams[start:stop]:
            team.sort()
            team.printInfo()
    
    def save(self):
        for team in self.teams:
            team.save()
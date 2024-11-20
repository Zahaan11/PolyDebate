import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re
from Team import Team
import random
import gspread

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
                if i == 5:
                    # Extract the <a> tag and get its href attribute
                    link_tag = b.find("a")
                    if link_tag and link_tag.has_attr("href"):
                        link = link_tag["href"]
                        links.append("www.tabroom.com"+link)
                    else:
                        links.append("")
                i = i + 1

        schoolFixer = {"Poly Prep Country Day":"Poly Prep Country Day School",
                    "Barstow":"Barstow School",
                    "NSU":"NSU University School",
                    "Quarry Lane":"The Quarry Lane School",
                    "Greenhill":"Greenhill School",
                    "Northside College Prep":"Northside College Preparatory",
                    "Pace":"Pace Academy",
                    "Thomas Kelly":"Thomas Kelly College Prep",
                    "Univ Of Chicago Lab":"Univ Of Chicago Lab School"
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
            newTeam = Team(codes[n],school + " " + code,names[n],target_url,links[n],n+3)
            self.teams.append(newTeam)
    
    def pushTeams(self):
        n = 0
        for team in self.teams:
            if(n==30):
                n = 0
                time.sleep(60)
            self.worksheet.update_acell(f"A{str(team.row)}",f'=HYPERLINK("{team.tab}", "{team.name}")')
            self.worksheet.update_acell(f"B{str(team.row)}",f'=HYPERLINK("{team.wikiLink}", "Wiki")')
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
            driver.get(team.wikiLink)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            while(soup.find("tbody",role="rowgroup") is None):
                time.sleep(0.1)
                soup = BeautifulSoup(driver.page_source, "html.parser")

            time.sleep(0.2)
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # Get the page content
            row = soup.find("tbody",role="rowgroup")
            # print(row.prettify())
            negargs = []
            affargs = []
            for round in row.find_all("tr"):
                n = 0
                side = ""
                rr = ""
                date_created = ""
                for box in round.find_all("td"):
                    if(n==1):
                        date_created = box.find("span")["title"][8:]
                    if(n==2):
                        side = box.find("span").text.strip()
                    if(n==5):
                        rrdiv = box.find("div", class_=re.compile("report"))
                        rr = rrdiv.find("div").text.strip()
                    if(n==6):
                        #THIS IS WHERE FILE DOWNLOADS ARE
                        pass
                    n = n + 1
                team.addRR(rr,side == "Aff",date_created,False)

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
            self.worksheet.update(all,f"C{start+3}:R{stop+3}")

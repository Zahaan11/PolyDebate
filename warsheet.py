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

gc = gspread.service_account()
sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730')
worksheet = sh.worksheet("test")

URL = "https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31289&event_id=291334"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")
table = soup.find("table", id="fieldsort")
teams = []
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
            names = b.text.strip()
            teams.append(names)
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

print(schools)
print(teams)

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

# schools = ["Poly Prep Country Day School"]
# teams = ["Batliboi & Londoner"]

# Set up Selenium WebDriver (Chrome here)
driver = webdriver.Chrome()  # Make sure ChromeDriver is installed

# Navigate to login page
driver.get("https://opencaselist.com/hspolicy24")

# Locate and fill the login form fields
driver.find_element(By.NAME, "username").send_keys("batliz27@polyprep.org")  # Update with the actual field name and your username
driver.find_element(By.NAME, "password").send_keys("password")  # Update with the actual field name and your password)
driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)  # Submit the form

# Allow time for the page to load
time.sleep(2)  # Adjust sleep duration as needed

main=[]
for n in range(len(teams)):
    team = teams[n].replace(" &","")
    space = team.index(" ")
    code = team[:2]+team[space+1:space+3]
    school = schools[n].replace(" ","")
    print(school + " " + code)

    target_url = f"https://opencaselist.com/hspolicy24/{school}/{code}"

    tempTeam = Team(codes[n],school + " " + code,teams[n],target_url,links[n],n+3)

    # Navigate to the target page after login
    driver.get(target_url)

    time.sleep(2)

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
                print(box)
                date_created = box.find("span")["title"][8:]
                print(date_created)
            if(n==2):
                side = box.find("span").text.strip()
            if(n==5):
                rrdiv = box.find("div", class_=re.compile("report"))
                rr = rrdiv.find("div").text.strip()
            if(n==6):
                print(box)
            n = n + 1
        tempTeam.addRR(rr,side == "Aff",date_created,False)
    
    main.append(tempTeam)

# Close the browser
driver.quit()

all = []
for team in main:
    team.sort()
    team.printInfo()
    row = []

    # Update column A with the team name
    worksheet.update_acell(f"A{str(team.row)}",f'=HYPERLINK("{team.tab}", "{team.name}")')
    worksheet.update_acell(f"B{str(team.row)}",f'=HYPERLINK("{team.wikiLink}", "Wiki")')
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
worksheet.update(all,f"C3:R{main[-1].row}")

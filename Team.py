import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from datetime import datetime, date
import json

class Team():
    def __init__(self,teamName,wikiName,partners,wikiLink,tabLink):
        self.name = teamName
        self.wiki = wikiName
        self.affDates = {}
        self.aff = []
        self.negTimes = {}
        self.neg = []
        self.negCol = []
        self.partners = partners
        self.wikiLink = wikiLink
        self.tab = tabLink
        self.lastUpdated = None

    def parseWiki(self,driver):

        driver.get(self.wikiLink)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        while(soup.find("tbody",role="rowgroup") is None and soup.find("div",class_="_error_fbh1a_1") is None):
            time.sleep(0.1)
            soup = BeautifulSoup(driver.page_source, "html.parser")
        
        time.sleep(0.4)

        if(soup.find("div",class_="_error_fbh1a_1") is not None):
            self.wikiLink = self.wikiLink[:-4] + self.wikiLink[-2:] + self.wikiLink[-4:-2]
            print(self.wikiLink)
            driver.get(self.wikiLink)

            soup = BeautifulSoup(driver.page_source, "html.parser")
            while(soup.find("tbody",role="rowgroup") is None and soup.find("div",class_="_error_fbh1a_1") is None):
                time.sleep(0.1)
                soup = BeautifulSoup(driver.page_source, "html.parser")
            time.sleep(0.4)

        if(soup.find("div",class_="_error_fbh1a_1") is None):
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
                self.addRR(rr,side == "Aff",date_created,False)

        self.lastUpdated = date.today().strftime("%m %d %Y"), "%m %d %Y"
        self.save()

    def addRR(self,rr,side,date,final):
        if("@" in rr):
            return
        if(date.strip() != ""):
            # print(date)
            # dateList = "/".split(date.strip())
            # print(dateList)
            # dateObj = datetime(int(dateList[2]), int(dateList[0]), int(dateList[1]))
            dateObj = datetime.strptime(date.replace("/"," ").strip(), "%m %d %Y")

        speech = ""

        if("\n" in rr):
            speeches = rr.split("\n")
            if(side):
                speech = speeches[0]
            else:
                negIndex = 1
                while True:
                    if(speeches[negIndex].strip() != ""):
                        break
                    negIndex+=1
                speech = speeches[negIndex]
        else:
            speech = rr
        
        if("-" in speech):
            labelEnd = 0
            if("---" in speech):
                labelEnd = speech.find("---") + 2
            elif("--" in speech):
                labelEnd = speech.find("--") + 1
            else:
                labelEnd = speech.find("-")
            speech = speech[labelEnd+1:].strip()
        elif(":" in speech):
            speech = speech[speech.find(":")+1:].strip()
        else:
            speech = speech.strip()

        if(speech != "" and speech != None):
            if(side):
                if(speech not in self.affDates or (speech in self.affDates and dateObj > self.affDates[speech])):
                    self.affDates[speech] = dateObj
            else:
                nargs = re.split(",|and|;",speech)
                for arg in nargs:
                    arg2 = arg.strip()
                    if(arg2 not in self.negTimes and not final):
                        self.negTimes[arg2] = 1
                    elif(arg2 in self.negTimes and not final):
                        self.negTimes[arg2] += 1
                    elif(final and arg2 not in self.negCol):
                        self.negCol.append(arg2)
        
        if((not side) and ("\n" in rr)):
            NR2 = rr.split("\n")[-1]
            self.addRR(NR2,False,date,True)

    def sort(self):
        if(len(self.affDates)>0):
            sorted_by_values = dict(sorted(self.affDates.items(), key=lambda item: item[1]))
            self.aff = list(sorted_by_values.keys())
            if(len(self.aff) > 1):
                self.aff.reverse()

        if(len(self.negTimes) > 0):
            sorted_by_values = dict(sorted(self.negTimes.items(), key=lambda item: item[1]))
            for arg in sorted_by_values.keys():
                self.neg.append(arg + " x" + str(self.negTimes[arg]))
            if(len(self.neg) > 1):
                self.neg.reverse()

    def printInfo(self):
        if(len(self.aff) == 0 and len(self.neg) == 0):
            print(self.name + " doesn't disclose")
        elif(len(self.neg) == 0):
            print(self.name + " reads ", *self.aff, " on aff, and doesn't disclose negs")
        elif(len(self.aff) > 0 and len(self.neg) > 0):
            print(self.name + " reads", *self.aff, "on aff, and reads", *self.neg, "on neg ")

    def save(self):
        with open(f"Teams/{self.wiki}.txt", "w", encoding="utf-8") as f:
            f.write(f"{self.name}|{self.wiki}|{self.partners}|{self.wikiLink}|{self.tab}|{self.lastUpdated}\n")
            f.write(str(self.affDates)+"\n")
            f.write(str(self.negTimes)+"\n")
            f.write("|".join(self.negCol)+"\n")

    def importArgs(self,a):
        self.aff = a.aff
        self.neg = a.neg
        self.affDates = a.affDates
        self.negTimes = a.negTimes
        self.negCol = a.negCol

def loadTeam(name):
    try:
        f = open(f"Teams/{name}.txt", "r", encoding="utf-8")
        row = 0
        fields=[]
        aff = {}
        neg = {}
        negCol = []
        for line in f:
            if(row==0):
                fields = line.split("|")
            if(row==1):
                aff = eval(line)
            if(row==2):
                neg = eval(line)
            if(row==3):
                negCol = line.split("|")
            row+=1
        team = Team(fields[0],fields[1],fields[2],fields[3],fields[4])
        team.lastUpdated = fields[5]
        team.affDates = aff
        team.negTimes = neg
        team.negCol = negCol
        team.sort()
        return team

    except:
        return None
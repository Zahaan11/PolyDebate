import re
from datetime import datetime

class Team():
    def __init__(self,teamName,wikiName,partners,wikiLink,tabLink,row):
        self.name = teamName
        self.wiki = wikiName
        self.affDates = {}
        self.aff = []
        self.negTimes = {}
        self.neg = []
        self.negCol = []
        self.row = row
        self.partners = partners
        self.wikiLink = wikiLink
        self.tab = tabLink

    def addRR(self,rr,side,date,final):
        if(date.strip() != ""):
            # print(date)
            # dateList = "/".split(date.strip())
            # print(dateList)
            # dateObj = datetime(int(dateList[2]), int(dateList[0]), int(dateList[1]))
            dateObj = datetime.strptime(date.strip(), "%m/%d/%Y")

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
            print(self.affDates)
            sorted_by_values = dict(sorted(self.affDates.items(), key=lambda item: item[1]))
            self.aff = list(sorted_by_values.keys())
            if(len(self.aff) > 1):
                self.aff.reverse()
            print(self.aff)

        if(len(self.negTimes) > 0):
            sorted_by_values = dict(sorted(self.negTimes.items(), key=lambda item: item[1]))
            for arg in sorted_by_values.keys():
                self.neg.append(arg + " x" + str(self.negTimes[arg]))

    def printInfo(self):
        if(len(self.aff) == 0 and len(self.neg) == 0):
            print(self.name + " doesn't disclose")
        elif(len(self.neg) == 0):
            print(self.name + " reads ", *self.aff, " on aff, and doesn't disclose negs")
        elif(len(self.aff) > 0 and len(self.neg) > 0):
            print(self.name + " reads", *self.aff, "on aff, and reads", *self.neg, "on neg ")

            
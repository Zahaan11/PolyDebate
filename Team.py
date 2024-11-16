import re

class Team():
    def __init__(self,teamName,wikiName,):
        self.name = teamName
        self.wiki = wikiName
        self.aff = []
        self.neg = []

    def addRR(self,rr,side):

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
                if(speech not in self.aff):
                    self.aff.append(speech)
            else:
                args = re.split(",|and|;",speech)
                for arg in args:
                    if(arg not in self.neg):
                        self.neg.append(arg)

    def printInfo(self):
        if(len(self.aff) == 0 and len(self.neg) == 0):
            print(self.name + " doesn't disclose")
        elif(len(self.neg) == 0):
            print(self.name + " reads ", *self.aff, " on aff, and doesn't disclose negs")
        elif(len(self.aff) > 0 and len(self.neg) > 0):
            print(self.name + " reads ", *self.aff, " on aff, and reads ", *self.neg, " on neg ")
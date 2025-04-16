from Tournament import Tournament
import os.path
import time

# GlenbrooksJV = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31289&event_id=291334",
#                           'CX',
#                           'https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730',
#                           'test')
# GlenbrooksJV.findTeams()
# GlenbrooksJV.findArgs()
# # GlenbrooksJV.pushTeams()
# GlenbrooksJV.pushArgs()
# GlenbrooksVLD = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31289&event_id=291338",
#                           'LD',
#                           'https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730',
#                           'Glenbrooks VLD')
# GlenbrooksVLD.findTeams()
# GlenbrooksVLD.pushTeams()

# file = open(os.path.join("Tournaments","GlenbrooksVLD.txt"),'w')
# file.write('Hello')
# file.close

# MamaroneckOpenCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31898&event_id=296161",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "Mamaroneck Open")
# MamaroneckOpenCX.findTeams()
# MamaroneckOpenCX.findArgs()
# MamaroneckOpenCX.pushArgs()
# MamaroneckOpenCX.pushTeams()

# LexOpenCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=33640&event_id=315026",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "Lex Open")
# LexOpenCX.findTeams()
# # LexOpenCX.findArgs()
# # LexOpenCX.pushArgs()
# LexOpenCX.pushTeams()

# EmoryCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31084&event_id=289943",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "Emory Open")
# EmoryCX.findTeams()
# EmoryCX.findArgs()
# EmoryCX.pushArgs()
# EmoryCX.pushTeams()


# HarvardCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31548&event_id=293150",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "Harvard Open")
# HarvardCX.findTeams()
# # HarvardCX.findArgs(51)
# # HarvardCX.pushArgs(51)
# HarvardCX.findArgs(51,"END")
# HarvardCX.pushArgs(51,"END")
# HarvardCX.pushTeams()

# UPennCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=34220&event_id=321555",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "UPenn Open")
# UPennCX.findTeams()
# UPennCX.findArgs()
# UPennCX.pushArgs()
# UPennCX.pushTeams()


# HarvardCX = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31548&event_id=293148",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "Harvard Novice")
# HarvardCX.findTeams()
# # HarvardCX.findArgs(40)
# # HarvardCX.pushArgs(40)
# HarvardCX.findArgs(40,"END")
# HarvardCX.pushArgs(40,"END")
# HarvardCX.pushTeams()

# DS2 = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=32876&event_id=317800",
#                               "CX",
#                               "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
#                               "TOCDS2")
# DS2.findTeams()
# # DS2.findArgs(43)
# # DS2.pushArgs(43)
# DS2.findArgs(43,"END")
# # DS2.pushArgs(43,"END")
# # DS2.pushTeams()
# DS2.printArgs(43,"END")

NDCA =  Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=34485&event_id=324531",
                   "CX",
                   "https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730",
                   "NDCA CX",)
NDCA.findTeams()
NDCA.findArgs()
NDCA.pushArgs()
NDCA.pushTeams()
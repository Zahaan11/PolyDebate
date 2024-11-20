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
GlenbrooksVLD = Tournament("https://www.tabroom.com/index/tourn/fields.mhtml?tourn_id=31289&event_id=291338",
                          'LD',
                          'https://docs.google.com/spreadsheets/d/1cUCMW0j14FFdMlPwb0UwvOMTaxOQ4dv0ipCWCEvJObA/edit?gid=97192730#gid=97192730',
                          'Glenbrooks VLD')
GlenbrooksVLD.findTeams()
GlenbrooksVLD.pushTeams()

# file = open(os.path.join("Tournaments","GlenbrooksVLD.txt"),'w')
# file.write('Hello')
# file.close
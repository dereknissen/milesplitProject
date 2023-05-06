from bs4 import BeautifulSoup
import requests
import json

url = "https://mo.milesplit.com/"

seasons = ["/cross-country", "/outdoor-track-and-field"]
event = ["/5000m?year=", "/100m?year=", "/200m?year=", "/400m?year=",
         "/800m?year=", "/1600m?year=", "/3200m?year=", "/100mH?year=",
         "/110mH?year=", "/300mH?year=", "/HJ?year=", "/LJ?year=", "/TJ?year=",
         "/PV?year=", "/SP?year=", "/DT?year="]

page = ['1','2','3','4','5','6','7','8','9','10',
        '11','12','13','14','15','16','17','18','19','20']

# Raypec ID is 10686
# Rockhurst ID is 10692
def addRosterToTeams(teamID):
    scrapeURL = url + "teams/" + str(teamID) + "/roster"
    page = requests.get(scrapeURL)
    soup = BeautifulSoup(page.text, "html.parser")
    athletes = soup.find_all("div", attrs={"class":"data-point w-30 w-md-50 d-flex align-items-center"})
    teamName = soup.find_all("h1")[0].text

    print("------------------ BREAK -----------------")


    for i, athlete in enumerate(athletes):
        athleteLink = str(athlete.a).split("\"")[1]
        athleteName = (athlete.text).strip() # Strip new line characters
        athleteWords = athleteName.split(", ")
        # Associate link
        athletes[i] = [athleteName, athleteLink]

    
    # Update json file
    teamDict = {teamName: athletes}
    oldJsonFile = open("teams.JSON", "r") # Opens file for editing
    oldJsonDict = json.load(oldJsonFile) # Gets a copy of old dictionary
    jsonFile = open("teams.JSON", "w")

    #print(type(oldJsonDict))
    #print(oldJsonDict)
    #print(type(teamDict))
    #print(teamDict)

    teamDict.update(oldJsonDict)

    json.dump(teamDict, jsonFile, indent = 6,)


    


addRosterToTeams(10686)
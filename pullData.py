# Derek Nissen
# 5/6/2023
# Scrape data from mo.milesplit webpage

from bs4 import BeautifulSoup
import requests
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

seasons = ["/cross-country", "/outdoor-track-and-field"]
event = ["/5000m?year=", "/100m?year=", "/200m?year=", "/400m?year=",
         "/800m?year=", "/1600m?year=", "/3200m?year=", "/100mH?year=",
         "/110mH?year=", "/300mH?year=", "/HJ?year=", "/LJ?year=", "/TJ?year=",
         "/PV?year=", "/SP?year=", "/DT?year="]

page = ['1','2','3','4','5','6','7','8','9','10',
        '11','12','13','14','15','16','17','18','19','20']

def milesplitLogin():
    chromePath = "/Applications/Google Chrome.app"
    browserDriver = Service(chromePath)
    pageToScrape = webdriver.Chrome(service=browserDriver)
    pageToScrape.get("https://mo.milesplit.com/")

    pageToScrape.find_element(By.LINK_TEXT, "Login").click()
    print("clicked login")
    time.sleep(3) # Wait for page to load
    pageToScrape.find_element(By.LINK_TEXT, "Login").click()
    print("trying to log in again")
    time.sleep(3)
    username = pageToScrape.find_element(By.ID, "email")
    password = pageToScrape.find_element(By.ID, "password")
    username.send_keys("dcyounger@gmail.com")
    password.send_keys("YoungerFam01")
    pageToScrape.find_element(By.ID, "frmSubmit").click()
    time.sleep(3)
    




def addRosterToTeams(teamID):
    url = "https://mo.milesplit.com/"
    scrapeURL = url + "teams/" + str(teamID) + "/roster"
    page = requests.get(scrapeURL) # Retrieve webpage response
    soup = BeautifulSoup(page.text, "html.parser") # Gets soup tool
    athletes = soup.find_all("div", attrs={"class":"data-point w-30 w-md-50 d-flex align-items-center"}) # Gets each athlete object
    teamName = soup.find_all("h1")[0].text # Gets the team name (header)

    for i, athlete in enumerate(athletes):
        athleteLink = str(athlete.a).split("\"")[1]
        athleteName = (athlete.text).strip() # Strip new line characters
        athleteWords = athleteName.split(", ") # First and last names are separated with a comma
        # Associate link
        athletes[i] = [athleteName, athleteLink] # Attach athlete link

    # Update json file
    teamDict = {teamName: athletes}
    oldJsonFile = open("teams.JSON", "r") # Opens file for editing
    oldJsonDict = json.load(oldJsonFile) # Gets a copy of old dictionary
    jsonFile = open("teams.JSON", "w")
    print("Added " + teamName + " to JSON.")

    teamDict.update(oldJsonDict) # Merge the new team with old teams

    json.dump(teamDict, jsonFile, indent = 6) # Save to file
    jsonFile.close()

def getRunnerEventData(runnerName, event = "None"):
    milesplitLogin()

    # Get athlete id
    teamJSON = open("teams.JSON", "r")
    teamDicts = json.load(teamJSON)
    firstNameInput, lastNameInput = runnerName.split(" ")[0], runnerName.split(" ")[1]
    athleteLink = ""
    for team in teamDicts:
        for athlete in teamDicts[team]:
            names = athlete[0].split(", ")
            firstName, lastName = (names[1]).upper(), (names[0]).upper()
            if firstNameInput.upper() == firstName and lastNameInput.upper() == lastName:
                athleteLink = athlete[1]
                break

    scrapeURL = athleteLink
    page = requests.get(scrapeURL) # Retrieve webpage response
    soup = BeautifulSoup(page.text, "html.parser") # Gets soup tool
    xcData = soup.find_all("div", attrs={"class":"record row"})

    for div in xcData:
        print(div.text) # Date
        otherStuff = div.find_all("div")
        print(otherStuff)
        for stuff in otherStuff:
            print(div.find_all("div"))
    

    



    
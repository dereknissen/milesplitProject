# Derek Nissen
# 5/6/2023
# Scrape data from mo.milesplit webpage

# Utility dependencies
import time
import json
from itertools import islice
import pprint
pp = pprint.PrettyPrinter(indent = 4)

# Dependencies for team roster
from bs4 import BeautifulSoup
import requests

# Dependencies for athlete information
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

def login():
    chromePath = "/Applications/Google Chrome.app"
    browserDriver = Service(chromePath)
    pageToScrape = webdriver.Chrome(service=browserDriver)

    # Login to milesplit
    pageToScrape.get("https://mo.milesplit.com/")
    pageToScrape.find_element(By.LINK_TEXT, "Login").click()
    print("clicked login")
    time.sleep(.5) # Wait for page to load
    pageToScrape.find_element(By.LINK_TEXT, "Login").click()
    print("trying to log in again")
    time.sleep(.5)
    username = pageToScrape.find_element(By.ID, "email")
    password = pageToScrape.find_element(By.ID, "password")
    username.send_keys("dcyounger@gmail.com")
    password.send_keys("YoungerFam01")
    pageToScrape.find_element(By.ID, "frmSubmit").click()
    time.sleep(2)
    return pageToScrape

def getRunnerData(runnerName, newData = False):
    results = {}
    if newData == True:
        # Login
        pageToScrape = login()

        # Search for runner
        pageToScrape.find_element(By.LINK_TEXT, 'Search').click()
        time.sleep(.5)
        searchBox = pageToScrape.find_element(By.ID, "postHeaderSearch")
        searchBox.send_keys(runnerName)
        pageToScrape.find_element(By.XPATH, '/html/body/div[5]/div/div/div/form/div/div[2]/button').click()
        time.sleep(.5) # Load page

        # Get runner name and high school
        jsonFile = open("teams.JSON", "r")
        # Format runner name
        words = runnerName.split(" ")
        formattedRunnerName = words[1].upper() + ", " + words[0].upper() # LAST NAME, FIRSTNAME
        runnerTeam = ""
        realRunnerName = ""
        teamDict = json.load(jsonFile) # Returns the team dictionary
        for teamName in teamDict:
            for athlete in teamDict[teamName]:
                if athlete[0].upper() == formattedRunnerName:
                    realRunnerName = athlete[0]
                    runnerTeam = teamName
                    break
            if runnerTeam != "":
                break
        
        # Check to see if the correct runner is in the results (same name and school)
        athleteResults = pageToScrape.find_elements(By.CLASS_NAME, 'result-info')
        runnerObject = None
        for athleteObject in athleteResults:
            name = athleteObject.find_element(By.CLASS_NAME, 'result-title').text
            desc = athleteObject.find_element(By.CLASS_NAME, 'result-description').text
            if runnerTeam in desc:
                runnerObject = athleteObject # Found the correct runner
        runnerObject.find_element(By.CLASS_NAME, 'result-title').click() # Click on correct runner
        time.sleep(.5) # Load page

        # Retrieve result data
        seasons = pageToScrape.find_elements(By.CLASS_NAME, 'season')
        for season in seasons:
            for event in season.find_elements(By.CLASS_NAME, 'event'):
                eventName = event.find_element(By.CLASS_NAME, 'event-heading')
                performanceContainerText = event.find_element(By.CLASS_NAME, 'container').text
                performanceList = performanceContainerText.split("\n")
                performanceList = [performanceList[i * 5:(i + 1) * 5] for i in range((len(performanceList) + 5 - 1) // 5 )] # Split into groups of 5
                for performance in performanceList:
                    # Performance is now a list and needs to be attached to the eventName key
                    if results.get(eventName.text) == None:
                        results[eventName.text] = [performance]
                    else:
                        oldList = results[eventName.text].copy()
                        oldList.append(performance)
                        results[eventName.text] = oldList
        
        # Ammend new data
        teamJSON = open("teams.JSON", "w")
        for team in teamDict:
            for athlete in teamDict[team]:
                if athlete[0].upper() == formattedRunnerName:
                    if len(athlete) < 3:
                        athlete.append(results)
                    else:
                        athlete[2] = results
        json.dump(teamDict, teamJSON, indent = 4)
        teamJSON.close()
    else:
        print("new data is false")
        words = runnerName.split(" ")
        formattedRunnerName = words[1] + ", " + words[0]
        teamDict = json.load(open("teams.JSON", "r"))
        print(formattedRunnerName)
        for team in teamDict:
            for athlete in teamDict[team]:
                if athlete[0].upper() == formattedRunnerName.upper():
                    try:
                        results = athlete[2]
                        print("found results")
                        print(results)
                    except:
                        print("Error! No data retrieved for this runner!")
    return results
            
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


    json.dump(teamDict, jsonFile, indent = 4) # Save to file
    jsonFile.close()
    

    



    
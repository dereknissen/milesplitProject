# Derek Nissen
# 5/6/2023
# Main file to utilize mo.milesplit data

import constants
import json
from pullData import *

def main(update = False):

    if update == True: # Get new data?
        # Clear json file
        teamsJson = open("teams.JSON", "w")
        json.dump({}, teamsJson, indent = 6,)
        teamsJson.close() # Close file as clean
        
        # Add current Milesplit data
        for team in constants.teamsToLoad:
            addRosterToTeams(team)
    
    # Testing
    getRunnerEventData("derek nissen")

main(False)
# Derek Nissen
# 5/6/2023
# Main file to utilize mo.milesplit data

import constants
import json
from pullData import *

def main(loadTeamData = False):

    if loadTeamData == True: # Get current team data from milesplit
        # Clear json file
        teamsJson = open("teams.JSON", "w")
        json.dump({}, teamsJson, indent = 4,)
        teamsJson.close() # Close file as clean

        # Add current Milesplit data
        for team in constants.teamsToLoad:
            addRosterToTeams(team)
    
    # Testing
    data = getRunnerData("ellie barker", newData = True) # Pull results


main(loadTeamData = False)
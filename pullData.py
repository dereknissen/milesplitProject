import requests

url = "http://api.milesplit.com/test/echo"

def pullData():
    response = requests.get(url)
    print(response)

pullData()
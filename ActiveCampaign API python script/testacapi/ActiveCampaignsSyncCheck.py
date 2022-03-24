import requests
import json
from pprint import pprint

# call AC api to get form name
url = "https://howtomanage.api-us1.com/api/3/forms/431"
headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
response = requests.request("GET", url, headers=headers)

if response.status_code == 200:
    string = str(response.text)
    json_obj = json.loads(string)
    formName = json_obj['form']['name']



current_id = "35985"

# API URL GET Request  TODO Enter API-Tokene below
#url = "https://howtomanage.api-us1.com/api/3/contacts/" + current_id + "/?include=forms"
url = "https://howtomanage.api-us1.com/api/3/contacts"
headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
querystring = {"formid":"35","limit":"1"}

response = requests.request("GET", url, headers=headers, params=querystring)

string = str(response.text)
json_obj = json.loads(string)


url = "https://howtomanage.api-us1.com/api/3/contacts"
headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
querystring = {"formid":"35","segmentid":"2735","limit":"1"}

response = requests.request("GET", url, headers=headers, params=querystring)

string = str(response.text)
json_obj = json.loads(string)





print("total: " + str(json_obj['meta']['total']))

#check list subscribed to
for item in json_obj['contactLists']:
    # pprint(item)
    #check Marketing Info List
    if item['list'] == '15':
        # pprint(item)
        print(item['sdate']) # start date of list subscription, there might be an udate for when it is updated and contact is unsubscribed

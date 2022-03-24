import requests
import json
from pprint import pprint

from csv import reader
import csv


with open('OUTPUT_FILE.csv', mode='w') as csv_file:
    writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # open file in read mode
    with open('206ContactsSubscribedToMarketingInfoList.csv', 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        for row in csv_reader:
            # row variable is a list that represents a row in csv
            print(row[0])
            print(row[1])
            print(row[2])
            print(row[3])
            print(row[4])

			# Get ActiveCampaigns Contact ID to be passed to API URL Request
            current_id = row[0]




			# API URL GET Request  TODO Enter API-Tokene below
            url = "https://howtomanage.api-us1.com/api/3/contacts/" + current_id
            headers = {"Accept": "application/json", "API-Token" : "<TODO:Active Campaigns API TOKEN HERE>"}
            response = requests.request("GET", url, headers=headers)



            string = str(response.text)
            json_obj = json.loads(string)




            #check list subscribed to
            for item in json_obj['contactLists']:
                # pprint(item)
                #check Marketing Info List
                if item['list'] == '207':
                    # pprint(item)
                    print(item['sdate']) # start date of list subscription, there might be an udate for when it is updated and contact is unsubscribed
                    row.append('List207')
                    row.append(item['sdate'])
                    row.append('subscribed to list due to automation:' + str(item['automation']))

                # Check BLAST list
                # if item['list'] == '31':
                #     # pprint(item)
                #     print(item['sdate'])
                #     row.append('List31')
                #     row.append(item['sdate'])
                #     row.append('subscribed to list due to automation:' + str(item['automation']))
                # Check Transactional Master List
                # if item['list'] == '208':
                #     # pprint(item)
                #     print(item['sdate'])
                #     row.append('List208')
                #     row.append(item['sdate'])
                #     row.append('subscribed to list due to automation:' + str(item['automation']))



            # To Write row
            writer.writerow(row)

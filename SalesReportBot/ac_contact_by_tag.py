import requests
from pprint import pprint

"""
Get contacts from ActiveCampaign account matching a set of tags by tag IDs.
Param: (array of ints) tag_id_list
"""
class AcContactByTag():

    def __init__(self, tagIdList):

        url = "https://howtomanage.api-us1.com/api/3/contacts/"
        headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
        tagId = str(tagIdList[0])
        limit = 100
        offset = 0
        querystring = {"tagid":tagId, "limit":str(limit), "offset":str(offset)}
        got_data = True
        self.contact_result = []

        # ActiveCampaign has a hard limit on returned data. Must make iterative calls to retrieve all matching results.
        while(got_data):
            response = requests.get(url, headers=headers, params={"tagid":tagId, "limit":str(limit), "offset":str(offset)})

            if (response and response.status_code == 200 and len(response.json()['contacts']) > 0):
                the_response = response.json()
                #pprint(the_response['meta']['total'])  # total available
                #pprint(str(len(the_response['contacts'])))         # returned in this call
                #pprint(the_response['contacts'][0]['email'])
                self.contact_result += the_response['contacts']
                offset += limit
            else:
                # got all the available records; time to exit the loop
                got_data = False


#test_tag_id = 724  # tag name "Test account to exclude from reports and leads"
#results = AcContactByTag([test_tag_id]).contact_result
#pprint(results[0]['email'])
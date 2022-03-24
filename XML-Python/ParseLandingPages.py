"""
Process list of landing pages exported from Wordpress.
The list was created by WP All Export plugin, and is stored in XML format.
--
Interrogate the page content looking for a specific string.
Output the XML data as a CSV for further reporting.

Author: Damian Davila
Create date: 31Aug2021
"""

#from pprint import pprint
import requests
import json

from csv import reader
import csv

import xml.etree.ElementTree as ET
import re


  
def loadRSS(theFile):
  
    # url of rss feed
    url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
  
    # creating HTTP response object from given url
    resp = requests.get(url)
  
    # saving the xml file
    with open(theFile, 'wb') as f:
        f.write(resp.content)
          
  
def parseXML(xmlfile):
  
    # create ElementTree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # hold landing page list
    lpages = []
  
    # iterate posts; ElementTree object uses XPATH notation (see https://www.datacamp.com/community/tutorials/python-xml-elementtree)
    for elem in root.findall('./post'):

        page = {}
  
        # iterate child elements of elem
        for child in elem:
  
            # Check for AC form in the page content
            if child.tag == 'Content':
                # AC forms can either be included as remote javascript, or be fully embedded in the page
                pattern = re.compile(r'howtomanage.activehosted.com/f/embed.php\?id=(\d+)"', re.IGNORECASE)
                patternEmbed = re.compile(r'form id="_form_(\d+)_".*action="https://howtomanage.activehosted.com/proc.php"')
                
                match = re.search(pattern, child.text) if child.text else None
                if match:
                    page['ACform'] = match.group()
                    page['Form ID'] = match.group(1)
                    page['Form Name'] = getAcFormName(match.group(1))
                    #page['Count of Members Who Submitted'] = getCountOfHtmMembersWithFormId(match.group(1))
                else:
                    match = re.search(patternEmbed, child.text) if child.text else None
                    if match:
                        page['ACform'] = match.group()
                        page['Form ID'] = match.group(1)
                        page['Form Name'] = getAcFormName(match.group(1))
                        #page['Count of Members Who Submitted'] = getCountOfHtmMembersWithFormId(match.group(1))
                    else:
                        page['ACform'] = ""
                        page['Form ID'] = ""
                        page['Form Name'] = ""
                        #page['Count of Members Who Submitted'] = ""

            else:
                page[child.tag] = child.text if child.text else ''
  
        # append page dictionary to page elems list
        lpages.append(page)
      
    # return page elems list
    return lpages

def getAcFormName(formId):
    # call AC api to get form name
    url = "https://howtomanage.api-us1.com/api/3/forms/" + formId
    headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
    response = requests.request("GET", url, headers=headers)
    print(url)

    formName = ""

    if response.status_code == 200:
        string = str(response.text)
        json_obj = json.loads(string)
        formName = json_obj['form']['name']

    return formName


def getCountOfHtmMembersWithFormId(formId):

    """
    Don't use as is. The API ignores the formid when you specify a segment.  It only returns the full segment list.
    TODO: Would need to pull member segment separately first (probably just once for the run), then pull the forms with this API, then match/exclude.
         BUT the API only returns maximum 100 records so this becomes untenable:  some forms have 1000's of submissions,
         so NNNN/100 * each form found * each contact being processed = way too many AC api calls
         Only way to limit it would be to do each found form only once, but even then it's a lot of api calls though order of magnitude better.
    """
    url = "https://howtomanage.api-us1.com/api/3/contacts"
    headers = {"Accept": "application/json", "API-Token" : "APIKEYHERE"}
    querystring = {"segmentid":"2735","limit":"1","formid":formId}

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        string = str(response.text)
        json_obj = json.loads(string)
        memberCount = str(json_obj['meta']['total'])

    return memberCount

  
def savetoCSV(pages, filename):
  
    # specifying the fields for csv file
    fields = ['id', 'Date', 'PostModifiedDate', 'Permalink', 'Status', 'AuthorUsername', 'Title', 'ACform', 'Form ID', 'Form Name', 'Count of Members Who Submitted']
  
    # writing to csv file
    with open(filename, 'w', newline="") as csvfile:
  
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields, quoting=csv.QUOTE_ALL)
  
        # writing headers (field names)
        writer.writeheader()
  
        # writing data rows
        writer.writerows(pages)
  

def main():

    # Load XML file containing an export of all pages on Wordpress site: produced by WP All Export plugin
    xmlFile= r'C:\Users\DamianD\Dropbox (HTM)\Projects\Reporting\RJon requests 27aug2021\Pages-Export-2021-August-31-756.xml'
    #loadRSS(xmlFile)
  
    # parse xml file
    landingPages = parseXML(xmlFile)
  
    # store landing page list in a csv file
    savetoCSV(landingPages, 'HTMASLF-landing-pages-AC-or-Acuity-09072021.csv')
      
      
if __name__ == "__main__":
  
    main()

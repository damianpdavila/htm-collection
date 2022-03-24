"""
Process list of pages exported from Wordpress.
The list was created by WP All Export plugin, and is stored in XML format.
--
Interrogate the page content looking for a specific string.
Output the XML data as a CSV for further reporting.

Author: Damian Davila
Create date: 10Sep2021
"""

#from pprint import pprint
import requests
import json

from csv import reader
import csv

import xml.etree.ElementTree as ET
import re
  
  
def parseXML(xmlfile):
  
    # create ElementTree object
    tree = ET.parse(xmlfile)
  
    # get root element
    root = tree.getroot()
  
    # hold landing page list
    lpages = []
    page_cnt = 0
  
    # iterate posts; ElementTree object uses XPATH notation (see https://www.datacamp.com/community/tutorials/python-xml-elementtree)
    for elem in root.findall('./post'):

        page = {}
        page_cnt += 1
  
        # iterate child elements of elem
        for child in elem:

            if child.tag == 'Permalink':
                page['permalink'] = child.text
  
            # Check for INC5000 image in the page content
            if child.tag == 'Content':
                #pattern = re.compile(r'\<img .*src=.*/inc.*500.*(jpg|png).*\>', re.IGNORECASE)
                pattern = re.compile(r'img .*src=.*inc.*500.*\>', re.IGNORECASE)
                pattern_avia = re.compile(r'\[av_image .*src=.*inc.*500.*\]', re.IGNORECASE)
                
                match = re.search(pattern_avia, child.text) if child.text else None
                if match:
                    page['image'] = match.group()
                else:
                    match = re.search(pattern, child.text) if child.text else None
                    if match:
                        page['image'] = match.group()
                
                if page.get('image'):
                    # append page dictionary to page elems list
                    lpages.append(page)
                    # just do this once per page:  could be several images, but we only want to know if the page has any at all
                    continue
      
    print(f"Page count: {str(page_cnt)}")
    # return page elems list
    return lpages


  
def savetoCSV(pages, filename):
  
    # specifying the fields for csv file
    #fields = ['id', 'Date', 'PostModifiedDate', 'Permalink', 'Status', 'AuthorUsername', 'Title', 'ACform', 'Form ID', 'Form Name', 'Count of Members Who Submitted']
    fields = ['permalink', 'image']
  
    # writing to csv file
    with open(filename, 'w', newline="", encoding='UTF-8') as csvfile:
  
        # creating a csv dict writer object
        writer = csv.DictWriter(csvfile, fieldnames = fields, quoting=csv.QUOTE_MINIMAL)
  
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
    savetoCSV(landingPages, r'HTMASLF-pages-w-inc5000-images.csv')
      
      
if __name__ == "__main__":
  
    main()

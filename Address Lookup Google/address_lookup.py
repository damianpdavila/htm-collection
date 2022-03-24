"""
Uses Google Places API to do address lookups.
Input is in CSV file with candidate business names and addresses.
Output is to a copy of CSV file with appended cols for suggested addresses.

"""
import googlemaps
from csv import reader
import csv


gmaps = googlemaps.Client(key='APIKEYHERE')
PLACES_FIND_FIELDS_BASIC = ["business_status",
        "formatted_address",
        "name",
        "permanently_closed",
        "place_id",
        "plus_code",
        "types"]

#targetName = "Zahn Law"
#targetAddress = "Oxnard, CA"

#targetName = "Michael E Stosic Law"
#targetAddress = "Philadelphia, PA"

def lookupAddress(targetName, targetAddress):

    target = targetName + " " + targetAddress

    places_result = gmaps.find_place(input=target, input_type='textquery', fields=PLACES_FIND_FIELDS_BASIC )
    #places_result = gmaps.find_place(input=target, input_type='textquery')

    potential_matches = []

    if places_result['status'] == 'OK':

        for candidate in places_result['candidates']:
            business_status = candidate.get('business_status', '')
            formatted_address = candidate.get('formatted_address', '')
            name =  candidate.get('name', '')
            potential_matches.append({'business_status':business_status, 'formatted_address':formatted_address, 'name':name})

    else:
        print(f"Places API error encountered.  Status:{places_result['status']} Error message:{places_result.get('error_message', '')}")

    return potential_matches

def main():

    with open('contacts-with-address-lookups.csv', mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # open file in read mode
        with open('lawfirm500-contacts-needing-lookups.csv', 'r') as read_obj:
            row_count = 0
            # pass the file object to reader() to get the reader object
            csv_reader = reader(read_obj)
            # Iterate over each row in the csv using reader object
            for row in csv_reader:
                row_count += 1

                if row_count == 1:
                    # write out the header
                    writer.writerow(row)
                    continue

                print(f"Row count: {str(row_count)}")
                # get the original row and append the lookup results
                output_row = row
                # row variable is a list that represents a row in csv (row of cols)
                lookup_name = row[0]
                lookup_address = row[4] + ", " + row[5]   # city state

                if lookup_name and lookup_address:
                    lookup_result_list = lookupAddress(lookup_name, lookup_address)
                    for lookup_result in lookup_result_list:
                        output_row.extend(['', lookup_result['business_status'], lookup_result['name'], lookup_result['formatted_address']])
                """
                ----------
                import re
                re.sub(r'[^\x00-\x7f]',r' ',output_row)
                ----------
                """
                writer.writerow(output_row)
      
if __name__ == "__main__":
  
    main()


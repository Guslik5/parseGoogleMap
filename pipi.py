import os
import serpapi
import pandas as pd
from dotenv import load_dotenv
#from sc_google_maps_api import ScrapeitCloudClient

load_dotenv()
api_key = os.getenv('4b6004436aa40defa1a4cc64fe00254c32a5c990a20835ff52f13303b2737821')
#client = ScrapeitCloudClient(api_key='6ee3658b-1453-40c2-97a7-c73c5eaa6e15')
client = serpapi.Client(api_key=api_key)
#start = 0

# Locations to search for real estate agencies
locations = {
    'UAE': '25.276987,55.296249',
    'Turkey': '38.963745,35.243322',
    'Cyprus': '35.126413,33.429859',
    'Thailand': '13.736717,100.523186'
}

# Initialize DataFrame to store results
all_results = pd.DataFrame(columns=["Title", "Address", "Phone Number", "Website", "Location"])
print(all_results)
for location_name in locations:
    #start = 0
    while True:
        results = client.search({
            'engine': 'google_maps',
            'q': 'real estate agency',
            'name': 'location_name',
            'type': 'search',
            #'start': start
        })

        if 'local_results' not in results or len(results['local_results']) == 0:
            print(f'No more local results for {location_name}')
            break

        #start += 20

        local_results = results['local_results']

        for result in local_results:
            title = result["title"]
            address = result["address"]
            phone = result["phone"] if "phone" in result else ""
            website = result["website"] if "website" in result else ""

            all_results = all_results.append({
                "Title": title,
                "Address": address,
                "Phone Number": phone,
                "Website": website,
                "Location": location_name
            }, ignore_index=True)

# Export DataFrame to Excel
excel_file_path = 'real_estate_agencies.xlsx'
all_results.to_excel(excel_file_path, index=False)
print(f'Data written to {excel_file_path}')

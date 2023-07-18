# Import python libraries
import requests
import pandas as pd
from pathlib import Path
import os
import config

# Get the current Windows user
# This is used to determine if the dataframes can be exported to the FP&A sharepoint file
user = os.getlogin()

# # Importing config with keys. See config example for details.
# export_path = Path("C:/",
#                    "Users",
#                    user,
#                    "BABDrive",
#                    "FP&A - Documents",
#                    "Private",
#                    "Spreadsheets for Qlik",
#                    "VOIP",
#                    "API Exports")

export_path = Path("/",
                   "var",
                   "www",
                   "html",
                   )

# API endpoints and keys
auth_url = "https://britishassessmentbureau.3cx.uk:8801/api/Authenticate"

api_url = "https://britishassessmentbureau.3cx.uk:8801/api/"
tables_url = "https://britishassessmentbureau.3cx.uk:8801/api/tables"

# Keys
public_key = config.publicKey
private_key = config.privateKey

# Send a POST request to the authentication endpoint with the keys in the request body
auth_payload = {"publicKey": public_key, "privateKey": private_key}
auth_headers = {"Content-Type": "application/json-patch+json", "accept": "*/*"}

auth_response = requests.post(auth_url, json=auth_payload, headers=auth_headers)

# Check if the authentication was successful and get the authentication token
if auth_response.status_code == 200:
    auth_token = auth_response.json()
    print("Authentication successful. Token:", auth_token, end='\n\n')
else:
    print("Authentication failed. Status code:", auth_response.status_code, end='\n\n')
    exit()

# Use the authentication token to make a GET request to the protected endpoint
table_headers = {"accept": "application/json", "Authorization": f"Bearer {auth_token}"}

records = [
    # {'url': ''}
    # {'url': 'eventlog', 'iterate': 0},
    # # {'url': 'users', 'iterate': 0},
        {'url': 'cl_calls', 'iterate': 1},
    {'url': 'cl_participants', 'iterate': 1},
    {'url': 'cl_segments', 'iterate': 1},
    {'url': 'cl_party_info', 'iterate': 1},
]
# Update tables that you want to pull

print("Running for loop.", end='\n\n')


for record in records:
    url = record['url']
    full_url = tables_url + "/" + url

    table_response = requests.get(full_url, headers=table_headers)

    last_response_length = len(table_response.json())
    table_data = table_response.json()
    if record['iterate'] == 1:
        print("Iterating to get more records, currently have", len(table_data))
        while last_response_length == 500:
            last_id = table_data[-1]["id"]
            next_url = full_url + "/" + str(last_id)
            table_response = requests.get(next_url, headers=table_headers)
            last_response_length = len(table_response.json())
            table_data = table_data + table_response.json()
            print("Got: ", last_response_length, " now have ", len(table_data))

    print("Finished iterating API")
    
    print("Total Records: ", len(table_data))
    df = pd.DataFrame(table_data)

    print("Table " + url + " complete.")
    print(df.head(10).to_markdown(), end='\n\n')

    # user_check = [
    #     "AntonyThornton",
    #     "JamesButler",
    #     "LanceBradley"
    # ]
    #
    # # Check if the user is one of those in user_check. If not then it does not export the dataframes
    # # Update after else if you need to store files locally
    # if user in user_check:
    file_name = url + ".csv"
    full_path = Path(export_path,
                     file_name)
    df.to_excel(full_path, index=False)
 #    else:
 #        print("Unable to print local access required. Please update path.")
 #        # Add export paths here
 #
import pandas as pd
import requests
import os
import json

import gspread
from oauth2client.service_account import ServiceAccountCredentials

URL = 'http://your-api-url/admin_api/v1'  # Replace 'your-api-url' with your actual API URL
API = 'your-api-key'  # Replace 'your-api-key' with your actual API key
END_POINT = 'conversions/log'

header = {'Api-Key': API, 'Content-Type': 'application/json'}

content = {
    "range": {
        "from": 'Yesterday',
        "to": 'Today',
        "timezone": "Asia/Manila",
        "interval": 'Yesterday'
    },
    "limit": None,
    "offset": 0,
    "columns": [
        'sale_datetime',
        'country',
        'campaign_id',
        'click_id',
        'status',
        'click_datetime'
    ],
    "filters": [
        {
            "name": "campaign_group",
            "operator": "EQUALS",
            "expression": "my_company"
        }
    ],
    "sort": [
        {
            "name": "click_id",
            "order": "ASC"
        }
    ]
}
content_str = json.dumps(content)
print(type(content_str))

response = requests.post(os.path.join(URL, END_POINT), headers=header, data=content_str)
response.status_code

response.json()

data_dict = {col: [] for col in response.json().get('rows')[0].keys()}

# data_dict

for item in response.json().get('rows'):
    for col in data_dict.keys():
        data_dict[col].append(item.get(col))

df = pd.DataFrame(data_dict)

# df.sort_values(by='country')

scope = ['https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive"]

credentials = ServiceAccountCredentials.from_json_keyfile_name("/path/to/your/credentials.json",
                                                               scope)  # Replace '/path/to/your/credentials.json' with the path to your actual service account credentials JSON file

client = gspread.authorize(credentials)

# sheet = client.create("NewDatabase")

# sheet.share('example@gmail.com', perm_type='user', role='writer') # Replace 'example@gmail.com' with the email you want to share the sheet with

sheet = client.open("your_spreadsheet_name").sheet1  # Replace 'your_spreadsheet_name' with the name of your actual spreadsheet
# new_sheet = client.create("

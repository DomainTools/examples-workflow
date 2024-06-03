import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_USERNAME = os.getenv('API_USERNAME')
API_KEY= os.getenv('API_KEY')

uri = '/v1/iris-enrich/'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'

data = {
    'format': 'json',
    'domain': 'domaintools.com,fedex.com,google.com,facebook.com,linkedin.com',
    'api_username': API_USERNAME,
    'api_key': API_KEY,
    'app_partner': app_partner,
    'app_name': app_name,
    'app_version': app_version
}

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

def main():
    # Make the HTTP requests to the API endpoint
    try:
        response = requests.post(f'{base_url}{uri}', headers=headers, data=data)
        if response.status_code == 200:
            json_response = response.json()

        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
        print('Results: ', json.dumps(json_response, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    main()
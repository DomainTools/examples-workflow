import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
API_KEY= os.getenv("DNSDB_API_KEY")

uri = '/dnsdb/v2/rate_limit/'
base_url = 'https://api.dnsdb.info'

headers = {
    'accept': 'application/x-ndjson',
    'X-API-KEY': API_KEY
}


def main():
    # Construct full url
    full_url = f"{base_url}{uri}"

    # Make the HTTP GET requests to the API endpoint
    try:
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            print('Response: ', json.dumps(response.json(), indent=2))
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
    except requests.RequestException as e:
        print("Error making HTTP request:", e)

if __name__ == "__main__":
    main()
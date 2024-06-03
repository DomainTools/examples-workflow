import requests
from dotenv import load_dotenv
import os
import json
from datetime import *
import math

load_dotenv()
API_KEY= os.getenv("DNSDB_API_KEY")

method = 'regex' # could also be'glob'
key = 'rrnames' # could also be rdata (left-handed search)
value = r'^[[:alpha:]]{2}\.[[:alpha:]]{4,8}\..-e\.kr\.$' # Example fo regex search
uri = f'/dnsdb/v2/{method}/{key}/{value}'
base_url = 'https://api.dnsdb.info'
limit = '10'

timestamp = datetime(2024, 1, 1, 0, 0, 0) # Not a param
# time_first_before = 
time_first_after = math.floor((timestamp - datetime(1970, 1, 1)).total_seconds())
print(time_first_after)
# time_last_before = num
# time_last_after = num

# swclient = ''
# version = ''
# id = ''
# aggr = boolean
humantime = 'true'
# offset = num

headers = {
    'accept': 'application/x-ndjson',
    'X-API-KEY': API_KEY
}


def main():
    # Construct full url
    full_url = f"{base_url}{uri}?time_first_after={time_first_after}&humantime={humantime}"

    # Make the HTTP GET requests to the API endpoint
    try:
        response = requests.get(full_url, headers=headers)
        if response.status_code == 200:
            response_text = response.text

            for line in response_text.splitlines():
                json_data = json.loads(line)
                print('RESPONSE: ', json.dumps(json_data, indent=2))
        else:
            print(f"Failed to fetch data: HTTP {response.status_code}")
    except requests.RequestException as e:
        print("Error making HTTP request:", e)

if __name__ == "__main__":
    main()
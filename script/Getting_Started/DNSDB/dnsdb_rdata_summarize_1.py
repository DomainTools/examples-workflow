import requests
from dotenv import load_dotenv
import os
import json
from datetime import *
import math

load_dotenv()
API_KEY= os.getenv("DNSDB_API_KEY")

type = 'ip' # could also be'raw' or 'ip'
value = '104.244.14.108' 
uri = f'/dnsdb/v2/summarize/rdata/{type}/{value}'
base_url = 'https://api.dnsdb.info'
limit = '10'

timestamp = datetime(2024, 1, 1, 0, 0, 0) # Not a param
time_first_before = math.floor((timestamp - datetime(1970, 1, 1)).total_seconds())
# time_first_after = num
# time_last_before = num
# time_last_after = num

# swclient = ''
# version = ''
# id = ''
# aggr = boolean
humantime = 'true'
# max_count = num

headers = {
    'accept': 'application/x-ndjson',
    'X-API-KEY': API_KEY
}


def main():
    # Construct full url
    full_url = f"{base_url}{uri}?time_first_before={time_first_before}&humantime={humantime}"

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
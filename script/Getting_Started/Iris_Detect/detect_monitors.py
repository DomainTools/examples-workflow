import requests
from dotenv import load_dotenv
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hmac_signature_generator import HmacSignatureGenerator


uri = '/v1/iris-detect/monitors/'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'

# Other params
datetime_counts_since = '2024-01-01'
include_counts = True
sort = 'term'
order = 'desc'
offset = ''
preview = 'true' # Optional param. Have to use a string here even though on other endpoints it is boolean.

load_dotenv()
API_USERNAME = os.getenv("API_USERNAME")
API_KEY= os.getenv("API_KEY")

def main():
    # Instantiate the HmacSignatureGenerator class
    signature_generator = HmacSignatureGenerator(API_USERNAME, API_KEY)

    # Generate the HMAC Signature
    signature, timestamp = signature_generator.generate_signature(uri)

    # Construct full url
    full_url = f"{base_url}{uri}?datetime_counts_since={datetime_counts_since}&include_counts={include_counts}&sort%5B%5D={sort}&order={order}&preview={preview}&app_partner={app_partner}&app_name={app_name}&app_version={app_version}&api_username={API_USERNAME}&timestamp={timestamp}&signature={signature}"

    # Make the HTTP GET requests to the API endpoint
    try:
        response = requests.get(full_url)
        print('Response: ', json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        print("Error making HTTP request:", e)

if __name__ == "__main__":
    main()
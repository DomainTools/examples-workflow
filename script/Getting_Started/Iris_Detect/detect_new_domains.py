import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hmac_signature_generator import HmacSignatureGenerator

uri = '/v1/iris-detect/domains/new/'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'

# Params
monitor_id = 'VAmAy37m9d' # Use the correct ID based on your created monitor
tlds = []
risk_score_ranges = '70-99'
# mx_exists =
discovered_since = quote('2024-01-01T00:00:00+00:00') # Using quote to encode special characters
discovered_before = ''
search = '' # A contains search for domain name
sort = 'discovered_date'
order = 'desc'
include_domain_data = True
# offset = For paginating requests beyond the limit 
# limit = 50 if include domain data is true
preview = 'true' # Optional param that can be used during testing and development


load_dotenv()
API_USERNAME = os.getenv('API_USERNAME')
API_KEY= os.getenv('API_KEY')

def main():
    # Instantiate the HmacSignatureGenerator class
    signature_generator = HmacSignatureGenerator(API_USERNAME, API_KEY)

    # Generate the HMAC Signature
    signature, timestamp = signature_generator.generate_signature(uri)

    # Construct full url
    full_url = f'{base_url}{uri}?monitor_id={monitor_id}&risk_score_ranges%5B%5D={risk_score_ranges}&discovered_since={discovered_since}&sort%5B%5D={sort}&order={order}&include_domain_data={include_domain_data}&preview={preview}&app_partner={app_partner}&app_name={app_name}&app_version={app_version}&api_username={API_USERNAME}&timestamp={timestamp}&signature={signature}'

    # Make the HTTP GET requests to the API endpoint
    try:
        response = requests.get(full_url)
        print('Response: ', json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        print('Error making HTTP request:', e)

if __name__ == "__main__":
    main()
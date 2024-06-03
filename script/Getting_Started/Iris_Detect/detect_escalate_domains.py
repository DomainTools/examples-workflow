import requests
from dotenv import load_dotenv
import os
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hmac_signature_generator import HmacSignatureGenerator

uri = '/v1/iris-detect/escalations/'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'

# A max of 100 domains per request can be block. A max of 30 requests per minute are allowed
# A max of 10 domains per request can be sent to the Google Phishing Protection team

# Body
body = {
    'watchlist_domain_ids': ['MEYM0eNywE'], # Example domain ID
    'escalation_type': 'blocked'
}


load_dotenv()
API_USERNAME = os.getenv('API_USERNAME')
API_KEY= os.getenv('API_KEY')

def main():
    # Instantiate the HmacSignatureGenerator class
    signature_generator = HmacSignatureGenerator(API_USERNAME, API_KEY)

    # Generate the HMAC Signature
    signature, timestamp = signature_generator.generate_signature(uri)

    # Construct full url
    full_url = f'{base_url}{uri}?app_partner={app_partner}&app_name={app_name}&app_version={app_version}&api_username={API_USERNAME}&timestamp={timestamp}&signature={signature}'

    # Make the HTTP POST requests to the API endpoint
    try:
        response = requests.post(full_url, json=body)
        print('Response: ', json.dumps(response.json(), indent=2))
    except requests.RequestException as e:
        print('Error making HTTP request:', e)

if __name__ == "__main__":
    main()
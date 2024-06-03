import requests
from dotenv import load_dotenv
import os
from hmac_signature_generator import HmacSignatureGenerator

# Use this script to get account information on all Iris products. 

uri = '/v1/account'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'
format = 'json'

load_dotenv()
API_USERNAME = os.getenv("API_USERNAME")
API_KEY= os.getenv("API_KEY")

def main():
    # Instantiate the HmacSignatureGenerator class
    signature_generator = HmacSignatureGenerator(API_USERNAME, API_KEY)

    # Generate the HMAC Signature
    signature, timestamp = signature_generator.generate_signature(uri)

    # Construct full url
    full_url = f"{base_url}{uri}?app_partner={app_partner}&app_name={app_name}&app_version={app_version}&format={format}&api_username={API_USERNAME}&timestamp={timestamp}&signature={signature}"

    # Make the HTTP GET requests to the API endpoint
    try:
        response = requests.get(full_url)
        print("Response: ", response.json())
    except requests.RequestException as e:
        print("Error making HTTP request:", e)

if __name__ == "__main__":
    main()
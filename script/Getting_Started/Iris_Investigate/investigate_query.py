import requests
from dotenv import load_dotenv
import os
from urllib.parse import quote
import json
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from hmac_signature_generator import HmacSignatureGenerator

load_dotenv()
API_USERNAME = os.getenv('API_USERNAME')
API_KEY= os.getenv('API_KEY')

uri = '/v1/iris-investigate/'
base_url = 'https://api.domaintools.com'
app_partner = 'YOUR_COMPANY'
app_name = 'YOUR_APP_NAME'
app_version = '1'

data = {
    'format': 'json',
    'domain': 'domaintools.com',
    'api_username': API_USERNAME,
    'api_key': API_KEY,
    'app_partner': app_partner,
    'app_name': app_name,
    'app_version': app_version,
    # 'ip': '199.30.228.112',
    # 'email': '',
    # 'email_domain': '',
    # 'nameserver_host': '',
    # 'nameserver_domain': '',
    # 'nameserver_ip': '',
    # 'registrar': '',
    # 'registrant': '',
    # 'registrant_org': '',
    # 'mailserver_host': '',
    # 'tagged_with_any': '',
    # 'tagged_with_all': '',
    # 'mailserver_domain': '',
    # 'mailserver_ip': '',
    # 'redirect_domain': '',
    # 'ssl_hash': '',
    # 'ssl_org': '',
    # 'ssl_subject': '',
    # 'ssl_email': '',
    # 'google_analytics': '',
    # 'adsense': '',
    # 'search_hash': '',
    # 'position': '',
    # 'active': True,
    # 'tld': '',
    # # Create_date supports three different operations...
    # # YYYY-MM-DD for "create date matches the given value"
    # # >YYYY-MM-DD for "create date is more than the given value"
    # # <YYYY-MM-DD for "create date is less than the given value"
    # 'create_date': '',
    # 'create_date_within': '', # Where the value is a positive integer describing, in DAYS, the maximum amount of time which has passed since a domain was first discovered.
    # 'first_seen_within': '', # Where the value is a positive integer describing, in SECONDS, the maximum amount of time which has passed since a domain was first discovered.
    # 'first_seen_since': '2024-01-01T00:00:00+00:00',
    # 'website_title': '',
    # 'expiration_date': '2025-07-08',
    # 'not_tagged_with_any': '',
    # 'not_tagged_with_all': '',
}

headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

def main():
    # Make the HTTP requests to the API endpoint
    results = []

    try:
        while True:
            response = requests.post(f'{base_url}{uri}', headers=headers, data=data)
            if response.status_code == 200:
                json_response = response.json()

                current_results = json_response['response']['results']
                results.extend(current_results)

                if not json_response['response']['has_more_results']:
                    break # Break the loop if there are no more results

                # Update the 'position' field for pagination
                data['position'] = json_response['response']['position']
            else:
                print(f"Failed to fetch data: HTTP {response.status_code}")
                break
        print('Results: ', json.dumps(results, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

if __name__ == "__main__":
    main()
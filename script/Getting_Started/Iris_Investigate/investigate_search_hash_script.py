import requests
import csv
from dotenv import load_dotenv
import os

def iris_investigate_api(search_hash):
    load_dotenv()
    API_USERNAME = os.getenv("API_USERNAME")
    API_KEY= os.getenv("API_KEY")
    base_url = 'https://api.domaintools.com/v1/'
    endpoint = 'iris-investigate'

    data = {
        'search_hash': search_hash,
        'api_key': API_KEY,
        'api_username': API_USERNAME
    }

    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    results = []

    try:
        while True:
            response = requests.post(f'{base_url}{endpoint}', headers=headers, data=data)
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
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")

    return results

def save_results_to_csv(results, filename="results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        if results:
            headers = results[0].keys()
            writer.writerow(headers)
            for result in results:
                writer.writerow(result.values())

def main():
    search_hash = 'U2FsdGVkX18z8U5LJ0l2i4FxZgnAfuF4rhv7JInMoQlZmNj1ZuqS/Jg3oW8wAFT80y3KEvnc+2DRnymYH/pfW6LRfJRUKPw31FoGr9ZxcakDCsS+1b7FbtcZuZx6pLPHvvQ62Kqx36hPnweQNFEn8EdxwwydVm2QFN4EJUfPuvBEN3QmtfI4kjwYsruzfpMGndj2XImjiAu5ekoBtP4TJZ7LrJAk7QwhjeJcij1EhhQKj3L80ZLjY+fQstLpVy54op5hSyJwMeod6Ytqe8855w=='  # domains containing icloud first seen in last 3 months
    results = iris_investigate_api(search_hash)
    if results:
        save_results_to_csv(results)
        print("Results saved to file.")
    else:
        print("No results to save.")

if __name__ == '__main__':
    main()
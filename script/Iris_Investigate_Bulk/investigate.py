import csv
from domaintools import API
import time

# Replace with your DomainTools API credentials

USER_NAME = 'YOUR_USERNAME'
KEY = 'YOUR_API_KEY'

# Initialize the DomainTools API
api = API(USER_NAME, KEY)

def get_domain_risk(domains, csv_writer):
    try:
        result = api.iris_investigate(domains)
        
        successful_domains = 0
        for data in result:
            D = data['domain']
            risk_score = data['domain_risk']['risk_score']
            csv_writer.writerow([D, risk_score])
            successful_domains += 1

        print(f"Processed batch of {len(domains)} domains. Successfully scanned {successful_domains} domains in this batch.")

    except Exception as e:
        print(f"Error processing batch of domains: {e}")

def main():
    # Read domains from input CSV
    input_file = "input_domains.csv"
    output_file = "output_domains.csv"
    
    with open(input_file, mode='r', newline='') as infile, open(output_file, mode='w', newline='') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        
        # Write header to output CSV
        csv_writer.writerow(['Domain', 'Risk Score'])
        
        domain_list = []
        total_domains_processed = 0
        for row in csv_reader:
            domain = row[0]  # assuming domain is in the first column
            domain_list.append(domain)

            if len(domain_list) == 100:
                get_domain_risk(domain_list, csv_writer)
                total_domains_processed += len(domain_list)
                
                print(f"Total domains scanned so far: {total_domains_processed}")
                
                domain_list.clear()  # Reset
                
                time.sleep(120)  # Help control rate limit
        
        # Process any remaining domains (less than 100) in the list
        if domain_list:
            get_domain_risk(domain_list, csv_writer)
            total_domains_processed += len(domain_list)
            print(f"Finished scanning. Total domains scanned: {total_domains_processed}")

if __name__ == "__main__":
    main()

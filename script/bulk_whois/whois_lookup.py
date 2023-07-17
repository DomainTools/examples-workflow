import ipaddress
import sys
import os
import time

from domaintools import API

api_username = '<YOUR API USERNAME>'
api_key = '<YOUR API KEY>'
dt_api = API(api_username, api_key)

######################## Validate IP Address ###########################
def validate_ip_address(ip_string):
   try:
       ipaddress.ip_address(ip_string)
       print('\tIP address is valid')
       return True
   except ValueError:
       print('\tIP address is not valid')
       return False

######################## MAIN ###########################
if (len(sys.argv) == 1):
    quit("Please enter a filename at the command line!")

input_file = sys.argv[1]

if (not os.path.exists(input_file)):
    quit("Input file does not exist: " + input_file)

print("Reading data ...")
with open(input_file, 'r', encoding="utf-8") as f_in:
    for line in f_in:
        ip = line.strip()
        ip_defang = ip.replace('.', '[.]')
        print("working on: " + ip_defang)

        if (not validate_ip_address(ip)): continue  

        if (os.path.isfile(ip + '_result.txt')): 
            print('\tresult already exist ... skipping')
            continue

        output_file = ip + '_result.txt'
        f_out = open(output_file, 'w', encoding='utf-8')

        ### Begin of Whois lookup
        print('\tcalling whois API')
        try:
            r = dt_api.whois(ip)
            f_out.write(r['whois']['record'])
        except Exception as e:
             print('\tERROR: ' + e.reason['error']['message'])
             f_out.close()
             os.remove(output_file)
             quit("End with error!")
        ### End of Whois lookup

        ### Begin of Iris Investigate lookup
        ### Comment this block if not using this
        print('\tcalling Iris Investigate API')
        f_out.write('--------------------- domains associated ---------------------\n')
        try:
            r = dt_api.iris_investigate(ip=ip)
            for data in r['results']:
                f_out.write(data['domain'] + '\n')
        except Exception as e:
            if ('Maximum 5000 returned' in e.reason):
                f_out.write('too many domains (5000 plus)')
                continue
            else:
                print('\tERROR' + e.reason['error']['message'])
                f_out.close()
                os.remove(output_file)
                quit("End with error!")
        ### End of Iris Investigate lookup

        f_out.close()

        time.sleep(2)           # Wait for 2 sec per IP (Rate limit)

print('Done!!!')
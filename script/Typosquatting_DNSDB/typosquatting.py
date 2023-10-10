
import dnsdb2
import dnstwist
from rapidfuzz.distance import Levenshtein
import sqlite3
from datetime import datetime
import config
#import time

#https://maxbachmann.github.io/RapidFuzz/Usage/distance/DamerauLevenshtein.html

client = dnsdb2.Client(config.api_key_DNSDB)

####################################### Sub ####################################### 
def break_into_segment (patterns):
    #Inputs must be less than 1250 total characters in length after encoding.
    # so far max tested with python is ~4164
    max_len = 3900          # Max Len for UI flex search (1250)   # 2048 default for DT # 4k max for API
    current_len = 0
    regex_array = []
    tmp_array = []
    for p in patterns:
        new_len = current_len + len(p) + 1      # 3 for the '|' after encoding (%7C) if using with UI else is 1
        if (current_len == 0):
            tmp_array.append(p)
            current_len = len(p)
        elif ((current_len > 0) and (new_len < max_len)):
            current_len = new_len
            tmp_array.append(p)
        else:
            regex_array.append(tmp_array)
            tmp_array = []                  # clear method causing issue
            tmp_array.append(p)
            current_len = len(p)

    regex_array.append(tmp_array)
    return regex_array

def call_DNSDB(myregex, exclude):
    time_last_after = '-3600' #last hour         #last 24 hrs (-86400)
    limit = 1000000
    offset = 0
    results = set()
    while True:
        try:
            for res in client.flex_rrnames_regex(myregex, exclude=exclude, time_last_after=time_last_after, limit=limit, offset=offset):
                results.add(res['rrname'])
        except dnsdb2.QueryLimited as e:
            offset += limit
        except dnsdb2.exceptions.QueryError as e:
            print ("QueryError:" + e)
            break
        except dnsdb2.exceptions.QueryFailed as e:
            print ("QueryFailed:" + e)
            break
        except dnsdb2.DnsdbException as e:
            print ("DnsdbException:" + e)
            break
        else:
            break
    #time.sleep(1)
    return results

####################################### Main ####################################### 
term = 'nike'                    # Term for typosquatting
subdomain_only = True               # False to find both apex & subdomain
run_DNSDB = True                   # False to skip DNSDB run
fake_TLD = 'fakeTLD'                # leave this alone
today = datetime.now()
exclude = ''                        # leverage DNSDB exclude parameter (input some value)
today_file = today.strftime("%Y-%m-%d_%H%M%S")

######## Typosquatting Begin ########
typosquatting = dnstwist.Fuzzer(term + '.' + fake_TLD)
typosquatting.generate()

typosquatting_domains = {}
unique_distance = set()
typosquatting_all = '|'.join([d['domain'] for d in typosquatting.domains])

for d in typosquatting.domains:
    new_d = d['domain'].replace( '.' + fake_TLD, '').replace('-' + fake_TLD + '.com', '').replace(fake_TLD, '')
    idna_encoded_bytes = new_d.encode('idna')
    unicode_string = idna_encoded_bytes.decode('idna')
    # skipping term in typosquatting (term<letter>)
    if (term in unicode_string): continue
    distance = Levenshtein.distance(term, unicode_string)

    typosquatting_domains[new_d] = distance
    unique_distance.add(distance)
typosquatting_domains[term] = 0
unique_distance.add(0)
######## Typosquatting End ########

db_file = 'e:\\typosquatting_' + term + '_' + str(today_file) +'.db'
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

conn.execute("CREATE TABLE TERMS (TERM STRING PRIMARY KEY NOT NULL, TOTAL INT NOT NULL, CLEAN_TOTAL INT NOT NULL, DATE TIMESTAMP);")
conn.execute("CREATE TABLE DISTANCE (TERM STRING NOT NULL, DIST INT NOT NULL, NUM_TYPO INT NOT NULL, DATE TIMESTAMP, PRIMARY KEY (TERM, DIST));")
conn.execute("CREATE TABLE TYPOSQUATTING (TERM STRING NOT NULL, DISTANCE INT NOT NULL, LABEL STRING NOT NULL, PUNYCODE STRING NOT NULL, DATE TIMESTAMP, PRIMARY KEY (TERM, DISTANCE, PUNYCODE));")
conn.execute("CREATE TABLE DOMAINS (TERM STRING NOT NULL, DISTANCE INT NOT NULL, DOMAIN STRING PRIMARY KEY NOT NULL, API_CALL INT NOT NULL, DATE TIMESTAMP);")
conn.execute("CREATE TABLE API_CALL (TERM STRING NOT NULL, DISTANCE INT NOT NULL, NUM INT NOT NULL, TNUM INT NOT NULL, REGEX STRING NOT NULL, DATE TIMESTAMP, PRIMARY KEY (TERM, DISTANCE, NUM));")
conn.commit()

try:
    cursor.execute("Insert into TERMS values (?,?,?,?)", (term, len(typosquatting.domains), len(typosquatting_domains), today))
    conn.commit()
except sqlite3.IntegrityError as e: pass

#print('-------------------------------------------')
#print('Label: ' + term)
#print('Total Typosquatting: ' + str(len(typosquatting.domains)))
#print('Clean Total Typosquatting: ' + str(len(typosquatting_domains)))
#print('-------------------------------------------')
total_API = 0
for dist in unique_distance:
    tmp = [k for k,v in typosquatting_domains.items() if v == dist]
    #print('Distance: ' + str(dist))
    #print('\tTyposquatting: ' + str(len(tmp)))

    for d in tmp:
        idna_encoded_bytes = d.encode('idna')
        unicode_string = idna_encoded_bytes.decode('idna')

        try:
            cursor.execute("Insert into TYPOSQUATTING values (?, ?, ?, ?, ?)", (term, dist, unicode_string, d, today))
        except sqlite3.IntegrityError as e: pass

    try:
            # find better way to insert record
            cursor.execute("Insert into DISTANCE values (?,?,?,?)", (term, dist, len(tmp), today))
            conn.commit()
    except sqlite3.IntegrityError as e: pass
           
    myregex = break_into_segment(tmp)

    total_API += len(myregex)
    #print('\t# of API call: ' + str(len(myregex)))

    # Each API call
    i = 1
    for reg in myregex:
        if (run_DNSDB):
            #if dist != 1: continue

            #print('\tAPI # ' + str(i) + '/' + str(len(myregex)))
            reg = '^.*({}).*\..*\..+$'.format('|'.join(reg)) if (subdomain_only) else '|'.join(reg)

            found_domains = call_DNSDB(reg, exclude)

            if (found_domains == None): found_len = 0
            else:
                found_len = len(found_domains)
                
                for domain in found_domains:
                    try: cursor.execute("Insert into DOMAINS values (?,?,?,?,?)", (term, dist, domain, i, today))
                    # find better way to insert record
                    except sqlite3.IntegrityError as e: pass
                conn.commit()

            #print('\t\tFound : ' + str(found_len))

            try:
                cursor.execute("Insert into API_CALL values (?,?,?,?,?,?)", (term, dist, i, len(myregex), reg, today))
                conn.commit()
            except sqlite3.IntegrityError as e: pass
            
            i += 1

#print('-------------------------------------------')
#print('Total API Call: ' + str(total_API))
print("Done")

conn.commit()
conn.close()
client.close()
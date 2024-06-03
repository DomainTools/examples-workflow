# DNSDB

[User Guide Documentation](https://www.domaintools.com/resources/user-guides/farsight-dnsdb-api-version-2-documentation/)

[SwaggerHub Documentation](https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DNSDB/2.0#/)

[DNSDB Technical Datasheet](https://www.domaintools.com/wp-content/uploads/DNSDB-API-Datasheet.pdf)

### `dnsdb_rate_limit.py`

- An example query using the DNSDB API to receive current usage, daily quota, and time until reset for the specific API key.

## RRSET Lookups

### /lookup/rrset/{type}/{value}

- `dnsdb_rrset_lookup_1.py`
- An example query using the DNSDB API to lookup all RRSETS for a specific owner name.

### /summarize/rrset/{type}/{value}

- `dnsdb_rrset_summarize_1.py`
- See summary counts for the results.

### /lookup/rrset/{type}/{value}/{rrtype}

- `dnsdb_rrset_lookup_2.py`
- An example query using the DNSDB API to lookup all RRSETS and specifying specific RRTYPES.

### /summarize/rrset/{type}/{value}/{rrtype}

- `dnsdb_rrset_summarize_2.py`
- See summary counts for the results.

### /lookup/rrset/{type}/{value}/{rrtype}/{bailiwick}'

- `dnsdb_rrset_lookup_3.py`
- An example query using the DNSDB API to lookup all RRSETS and specifying specific RRTYPES and Bailiwick.
- [What is Bailiwick?](https://www.domaintools.com/resources/blog/what-is-a-bailiwick/)

### /summarize/rrset/{type}/{value}/{rrtype}/{bailiwick}'

- `dnsdb_rrset_summarize_3.py`
- See summary counts for the results.

## RDATA Lookups

### /lookup/rdata/{type}/{value}

- `dnsdb_rdata_lookup_1.py`
- An example query using the DNSDB API to lookup all resource records for specific RDATA values.

### /summarize/rdata/{type}/{value}

- `dnsdb_rdata_summarize_1.py`
- See summary counts for the results.

### lookup/rdata/{type}/{value}/{rrtype}

- `dnsdb_rdata_lookup_2.py`
- An example query using the DNSDB API to lookup all resource records for specific RDATA values and RRTYPE.

### /summarize/rdata/{type}/{value}/{rrtype}

- `dnsdb_rdata_summarize_2.py`
- See summary counts for the results.

## Flex Search

[Regular Expression Documentation](https://www.domaintools.com/resources/blog/whats-a-regular-expression/)

### /{method}/{key}/{value}

- `dnsdb_flex_search_1.py`
- An example query using the DNSDB API to lookup all resource records using regular expressions and globs (aka wildcarding).

### /{method}/{key}/{value}/{rrtype}

- `dnsdb_flex_search_2.py`
- An example query using the DNSDB API to lookup all resource records with a specific RRTYPE using regular expressions and globs (aka wildcarding).

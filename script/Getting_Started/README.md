# Summary

Here contains a group of python scripts for API endpoints associated with the Iris and DNSDB APIs as seen in both SwaggerHubs linked below.

## SwaggerHub Links

1. [Iris](https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DomainTools_APIs/1.1#/)

2. [DNSDB](https://app.swaggerhub.com/apis-docs/DomainToolsLLC/DNSDB/2.0#/)

## Instructions

1. You'll need to go to the .env file and input your credentials

```.env
API_USERNAME="you-username"
API_KEY="your-iris-key"
DNSDB_API_KEY="your-dnsdb-key"
```

2. If you don't have Python you'll need to install Python. Here is a helpful [article](https://realpython.com/installing-python/) that can take you through the steps.

3. Depending on the script you are interested in using, you may need to install the modules used in that script. Look at the import statements at the top of the script to see what you may need to import. You will at least need to import the python-dotenv module in order to grab your credentials when executing the script.

```terminal
pip3 install python-dotenv
```

4. Execute a script:
   1. Open up a terminal and make sure you change directories into the dt-api-endpoints directory(folder).

   ```terminal
   cd path/to/directory
   ```

   2. Install any modules needed

   3. Execute the script in your terminal

   ```terminal
   python folder_name/name_of_script.py
   ```

## Authentication

- There are two ways to authenticate when using our APIs.
  - Open Key Authentication
  - Signed Authentication
- Here is [documentation](https://www.domaintools.com/resources/api-documentation/authentication/) on the different authentication methods.
- The file `hmac_signature_generator.py` shows how you can create a class to use with Signed Authentication.

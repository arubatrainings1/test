#!/usr/bin/env python
# coding: utf-8

# # Aruba Central Python workflow-Example

# Pycentral is the Python package to programmatically interact with Aruba Central via 
# REST APIs. We can download the REST API SDK from GitHub or PyPi. 
# 
# The pycentral subfolder contains the Aruba Central Python modules. Each module contains multiple Python classes. Each Class is a representation of some of Aruba Central's API categories, as mentioned in the API Reference section. Each Class has its own function definitions used to make a single REST API call.
# 
# We have Aruba central API reference here: https://developer.arubanetworks.com/aruba-central/reference
# 
# # Task Requirement:
# Utilize pycentral package to Create a new Site and a new Group , then move the APs to the new site and new group,and dynamically change it’s name to this format AP<Model>-<Sitename>-<Groupname>-<number>, for example, AP335-SJ-IAP-1.
# 
# Before we run the code we should prepare the Variables from Aruba Central API gateway for base class ArubaCentralBase,like base_url etc.  then We will go though below workflows:
# 
# 
# •	Install requests library
# •	Install pycentral library
# •	Get AP informarion
# •	Configure a new site and group
# •	Move the APs  to new site and group
# •	Re-achive AP information to verify if the APs get right site and AP information
# •	Raname APs
#     
# 

# # STEP1: install requests and pycentral

# In[1]:


get_ipython().system('pip install requests')


# In[2]:


get_ipython().system('pip install pycentral')


# # STEP2. Get central_info to access central API

#     # option1: access_token approach. replace base_url and access_token. 

# central_info = {
#     "base_url": "<api-gateway-domain-url>",
#     "token": {
#         "access_token": "<api-gateway-access-token>"
#     }
# }

#     # Option2 OAUTH APIs approach.Replace username,Password,client_id,client_secret,customer_id and base_url with your own

#     # Option2 OAUTH APIs approach.Replace username,Password,client_id,client_secret,customer_id and base_url with your own
#     
#  central_info = {
#     
#    "username": "< aruba-central-account-username>",
#    
#    "password": "< aruba-central-account-password>",
#    
#    "client_id": "< api-gateway-client-id>",
#    
#    "client_secret": "< api-gateway-client-secret>",
#    
#    "customer_id": "< aruba-central-customer-id>",
#    
#    "base_url": "< api-gateway-domain-url>"
#    
#    }

#  # Step3 # Create an instance of ArubaCentralBase using API access token 
#     # or API Gateway credentials.

# In[1]:


from pycentral.base import ArubaCentralBase
from pprint import pprint


central_info = {
    "base_url": "< api-gateway-domain-url>",
    "token": {
        "access_token": "<Your access token>"
    }
}

"""central_info = {

"username": "< aruba-central-account-username>",
"password": "< aruba-central-account-password>",
"client_id": "< api-gateway-client-id>",
"client_secret": "< api-gateway-client-secret>",
"customer_id": "< aruba-central-customer-id>",
"base_url": "< api-gateway-domain-url>"
}
}"""


ssl_verify = True

central = ArubaCentralBase(central_info=central_info,
                           ssl_verify=ssl_verify)


# Step4  Sample API calls using 'ArubaCentralBase.command()'  

#    # Description about command usage.
# 
# def command(self, apiMethod, apiPath, apiData={}, apiParams={},
#                 headers={}, files={}, retry_api_call=True):
#         """This function calls requestURL to make an API call to Aruba Central after gathering parameters required for API call.
#         
#         When an API call fails with HTTP 401 error code, the same API call is retried once after an attempt to refresh access token or create new access token is made.
#         
#         :param apiMethod: HTTP Method for API call. Should be one of the supported methods for the respective Aruba Central API endpoint.
#         
#         :type apiMethod: str
#         
#         :param apiPath: Path to the API endpoint as required by API endpoint. Refer Aruba Central API reference swagger documentation.
#         
#         :type apiPath: str
#         
#         :param apiData: HTTP payload for the API call as required by API endpoint. Refer Aruba Central API reference swagger
#             documentation, defaults to {}
#             
#         :type apiData: dict, optional
#         
#         :param apiParams: HTTP url query parameters as required by API endpoint. Refer Aruba Central API reference
#             swagger, defaults to {}
#             
#         :type apiParams: dict, optional
#         
#         :param headers: HTTP headers as required by API endpoint. Refer Aruba Central API reference swagger, defaults to {}
#         
#         :type headers: dict, optional
#         
#         :param files: Some API endpoints require a file upload instead of apiData. Provide file data in the format accepted by API endpoint and Python requests library, defaults to {}
#         
#         :type files: dict, optional
#         
#         :param retry_api_call: Attempts to refresh api token and retry the api call when invalid token error is received, defaults to True
#         
#         :type retry_api_call: bool, optional
#         
#         :return: HTTP response with HTTP staus_code and HTTP response payload. \n
#             * keyword code: HTTP status code \n
#             * keyword msg: HTTP response payload \n
#             * keyword headers: HTTP response headers \n
#             
#         :rtype: dict
#      

#  ## Step4.1 # GET sites from Aruba Central. according to the document, we should use apiParams to query.

# In[15]:


apiPath = "/central/v2/sites"

apiMethod = "GET"

apiParams = {
    "limit": 20,
    "offset": 0
}
base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiParams=apiParams)
pprint(base_resp)


# ## STEP4.2  # GET APs from Aruba Central.according to the document, we should use apiParams to query.

# In[5]:


apiPath = "/monitoring/v2/aps"

apiMethod = "GET"

apiParams = {
    "limit": 20,
    "offset": 0
}
base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiParams=apiParams)
pprint(base_resp)


# ## Step4.3     # post(CREATE) a new site. According to the document, we should use apiData to create. 

# In[7]:


apiPath = "/central/v2/sites"
apiMethod = "POST"
apiData = {
    "site_address": {
        "address": "3970 Rivermark Plaza",
        "city": "Santa Clara",
        "state": "California",
        "country": "United States",
        "zipcode": "95053"
    },
    "site_name": "site2"
}

base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiData=apiData)
pprint(base_resp)


# ## Step4.4 
# #Put the APs into the site. 
# #get the site_id from the above outputs.
# #get the device_ids(Serial number)from AP information.
# #get the URL and request method from swagger or Developer API reference. 

# In[8]:


apiPath = "central/v2/sites/associations"

apiMethod = "POST"

# for different table, please replace the Serial number below with your own APs'.

apiData = {
    "device_type": "IAP",
    "device_ids": ["<serial number of AP1>", "<serial number of AP2>"],
    "site_id": 1
}


base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiData=apiData)
pprint(base_resp)


# ## Step4.5    # Post(CREATE) a new group. According to the document, we should use apiData to create. 

# In[9]:


apiPath = "configuration/v2/groups"

apiMethod = "POST"

apiData = {
    "group_attributes": {
        "template_info": {
            "Wired": False,
            "Wireless": False
        },
        "group_password": "Aruba123!"
    },
    "group": "IAP-GROUP-test"
}


base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiData=apiData)
pprint(base_resp)


# ## Step4.6    # associate the two APs to this group"IAP-GROUP-test".

# In[92]:


apiPath = "configuration/v1/devices/move"
apiMethod = "POST"
apiData = {
    "serials": ["<serial number of AP1>", "<serial number of AP2>"],
    "group": "IAP-GROUP-test"
}

base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiData=apiData)
pprint(base_resp)


# ## step4.7  check if the APs get the new site name and new group.

# In[13]:


apiPath = "/monitoring/v2/aps"

apiMethod = "GET"

apiParams = {
    "limit": 20,
    "offset": 0
}
base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiParams=apiParams)
pprint(base_resp)

ap_dict= base_resp["msg"]["aps"] 
ap_number = base_resp["msg"]["count"]
ap_list=[]
# build a AP list including the new names.

for i in range(ap_number):
   ap_list.append("AP-" + ap_dict[i]["model"] + "-" +ap_dict[i]["site"]+"-"+ap_dict[i]["group_name"]+"-"+str(i+1))


print (ap_list)


# ## Step4.8 #Rename the AP with "AP-<MODEL>-<SITE NAME>-<GROUP NAME>-<ap number>"

# In[16]:


#use for loop to execute API calls to change AP name one by one.
apiData={}

for i in range(ap_number):
  apiPath = "configuration/v2/ap_settings/"+ ap_dict[i]["serial"]
  apiMethod = "POST"
  apiData={
    "hostname": ap_list[i],
    "ip_address": "",
    "zonename": "",
    "achannel": "",
    "atxpower": "",
    "gchannel": "",
    "gtxpower": "",
    "dot11a_radio_disable": True,
    "dot11g_radio_disable": True,
    "usb_port_disable": True
    }
     

  print(apiData)
  base_resp = central.command(apiMethod=apiMethod, 
                            apiPath=apiPath,
                            apiData=apiData)
    
  pprint(base_resp)


# Note: we have another workflow to use a csv file to import the AP's serial and hostname. check out developer website. https://developer.arubanetworks.com/aruba-central/docs/python-workflows-rest-api
# 
# and also, we have multiple way to handle the AP information. For example, we can download the AP information firectly from Aruba Central GUI,then change the format we need. or use pandas which is a Python library can esily handle csv or excel chart.

#     #Attched another workflow to handle AP information mentioned above for reference. more detail please check developer website.

# In[ ]:



#Sample CSV file:

serial_number,hostname,ip_address,zonename,achannel,atxpower,gchannel,gtxpower,dot11a_radio_disable,dot11g_radio_disable,usb_port_disable
AAAAAAAAAA,AP1,,,,,,,,,
BBBBBBBBBB,AP2,,,,,,,,,

# Create the following files by refering to the samples.
csv_filename = "csv_file.csv"
central_filename = "input_token_only.yaml"

# Get instance of ArubaCentralBase from the central_filename
from pycentral.workflows.workflows_utils import get_conn_from_file
central = get_conn_from_file(filename=central_filename)

# Rename AP using the workflow `workflows.config_apsettings_from_csv.py`
from pycentral.workflows.config_apsettings_from_csv import ApSettingsCsv
ApSettingsCsv(conn=central, csv_filename=csv_filename)


# In[ ]:


#Attached pandas to handle AP information for reference.


# import http.client
# import pandas as pd
# import json
# import pprint as pp
# 
# conn = http.client.HTTPSConnection("API gateway URL")
# 
# payload = ''
# 
# #change the below access_token
# 
# headers = {
#   'Authorization': 'KBdW22yu7OSztv4R8wIZzZqVZ1OZRnZ2'
# }
# 
# conn.request("GET", "/monitoring/v1/aps", payload, headers)
# 
# res = conn.getresponse()
# 
# data = res.read()
# 
# data_json=json.loads(data)
# 
# print(data_json)
# 
# df = pd.DataFrame(data_json["aps"])
# 
# df[['name','serial']].to_csv("apinfo.csv")
# 
# df['achannel']=""
# 
# df['atxpower']=""
# 
# df['gtxpower']=""
# 
# df['gchannel']=""
# 
# df['dot11a_radio_disable']=""
# 
# df['dot11g_radio_disable']=""
# 
# df['usb_port_disable']=""
# 
# df['zonename']=""
# 
# ap_count=int(pd.DataFrame(data_json)["count"][0])
# 
# for i in df.index:
# 
#  df.at[i,'name']=df.at[i,'site']+'-AP'+df.at[i,'model']+"-"+str(i)
#  
# df=df.rename(columns={"serial": "serial_number", "name": "hostname"})
# 
# df.loc[:,['serial_number','hostname','ip_address','zonename','achannel','atxpower','gtxpower','gchannel','dot11a_radio_disable','dot11g_radio_disable','usb_port_disable']].to_csv("csv_file.csv",index=False)
# 

# In[ ]:





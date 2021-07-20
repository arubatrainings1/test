#!/usr/bin/env python
# coding: utf-8

# # Aruba Network Automation Product Training -Lab4- Task2

# There are two Approaches to use pyaoscx: open granulated approach and Imperative Factory Approach to utilize Pyaoscx library.
# 
# 
# On Access switch:
# -	Utilize open granulated approach to create vlan200, add a description and put Interface into the VLAN. Create Lag1, add interface1/1/8 into the lag1. 
# -	Utilize Imperative Factory Approach to create VLAN201 and Lag2.
# -	Chanlenge: understand how to handle configurarion. Save the running-config to checkpoint and tftp server.
# 

# In[11]:


get_ipython().system('pip install pyaoscx ')


# In[8]:


#get to know the pyaoscx and where it is installed.
get_ipython().system('pip show pyaoscx')


# In[7]:


from pyaoscx.session import Session
from pyaoscx.pyaoscx_factory import PyaoscxFactory
from pyaoscx.vlan import Vlan
from pyaoscx.interface import Interface
from pyaoscx.static_route import StaticRoute
from pyaoscx.vrf import Vrf
import urllib3
urllib3.disable_warnings()


# In[10]:


# There are two approaches to workflows, both using the session.
version = '10.04'
switch_ip = '<yOUR switch IP'
s = Session(switch_ip, version)
s.open('<Your switch Username', 'Your switch password')


# #  APPROACH 1: OPEN GRANULATED APPROACH VLAN

# In[ ]:



# Create Vlan object -- Not yet materialized
#Vlan is Python Class has been defined in PYTHON module pycentral.vlan
#vlan200 is a object or instance of this Class

vlan200 = Vlan(s, 200, name="VLAN 200", voice=True)


# In[ ]:


# Since object is not materialized, performs a POST request -- This method internally makes a GET request right after the POST
# Obtaining all attributes VLAN related
#If you an "Internal server error", that means the vlan is already exsisted.
vlan200.apply()


# In[ ]:


#display all Vlans


# In[ ]:


Vrf.get_all(s)


# In[ ]:


#add description for vlan200
vlan200.description = "New description, changed via pyaoscx SDK1"
vlan200.apply()

# Now vlan200 contains the description attribute
print("VLAN 200 description {}".format(vlan200.description))


# In[ ]:


# Now let's create another object, that we know already exists inside of the Switch
vlan1 = Vlan(s, 1)
# Perform a GET request to obtain all data and materialize object
vlan1.get()


# In[ ]:


# Now, we are able to modify the objects internal attributes
vlan1.voice = True
# Apply changes
changed = vlan1.apply()
# If changed is True, a PUT request was done and object was modified


# In[ ]:


# More complex example using the OPEN GRANULATED APPROACH
# Create an Interface object

lag = Interface(s, 'lag1')
lag.apply()


# In[ ]:


# Create a Vlan object

vlan_1 = Vlan(s, 1)
    # In this case, now that the VLAN exists within the Switch,
    # a GET request is called to obtain the VLAN's information.
    # The information is then added to the object as attributes.
vlan_1.get()

 


# In[ ]:


# Interfaces/Ports added to LAG
port_1_1_8 = Interface(s, '1/1/8')
port_1_1_8.get()
 # Make changes to configure LAG as L2
lag.admin = 'down'
lag.routing = False
lag.vlan_trunks = [vlan_1]
lag.lacp = "passive"
lag.other_config["mclag_enabled"] = False
lag.other_config["lacp-fallback"] = False
lag.vlan_mode = "native-untagged"
lag.vlan_tag = vlan_1
 # Add port as LAG member
lag.interfaces.append(port_1_1_8)

 # Apply changes
lag.apply()

 # ===========================================================
 # ===========================================================
 # ===========================================================


# #  APPROACH 2: IMPERATIVE FACTORY APPROACH

# pyaoscx.pyaoscx_factory provide a Factory class to instantiate all pyaoscx Modules through specific methods.
# https://github.com/aruba/pyaoscx/blob/master/pyaoscx/pyaoscx_factory.py
# 

# In[ ]:


# Create VLAN 201
# Create Factory object, passing the Session Object
factory = PyaoscxFactory(s)


# In[ ]:


# Create Vlan object
# If vlan is non-existent, Factory instantly creates it inside the switch device
vlan201 = factory.vlan(201, "NAME201")


# In[ ]:


# Same complex example using the IMPERATIVE FACTORY APPROACH
# PLUS USING IMPERATIVE METHODS

# Create the Interface object
lag2 = factory.interface('lag2')
modified = lag2.configure_l2(
        description="Created using imperative method",
        admin='up',
        vlan_mode="native-untagged",
        vlan_tag=1,
        trunk_allowed_all=True,
        native_vlan_tag=True)

# If modified is True, a PUT request was done and object was modified


# #check if the VLAN is created

# In[48]:


Vlan.get_all(s)


# In[ ]:


# At the end, the session MUST be closed
s.close()


# # Challenge:
# •	Get the Access switch running-config configuration
# •	Save it to a checkpoint named “checkpoint1_by_pyaoscx”
# •	Backup running-config to tftp server 10.254.1.21
# 

# #=======================================================================================
# 
# # Solution:
# 
# #You have to change the below cell to "code" type and move them to the above the "s.close" cell to run.
# #The Challege solution:

# config1=Configuration(s)

# Configuration.get_full_config(config1,"startup-config")

# Configuration.create_checkpoint(config1,"running-config","checkpoint1_by_pyaoscx11")

# Configuration.backup_configuration(config1, "running-config", output_file="test_config",
#                              vrf="<VRF name", config_type='json',
#                              remote_file_tftp_path="tftp://<TFTP server IP>/test_config")

# # You completed the LAB4 Task2 

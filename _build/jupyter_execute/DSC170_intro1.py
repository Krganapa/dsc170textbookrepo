#!/usr/bin/env python
# coding: utf-8

# # Making maps with ArcGIS
# <a id='3.Arcgis'></a>
# A brief example of using ArcGIS API for Python. It is a popular Python library for GIS and spatial analysis. We'll use it more extensively after exploring free libraries such as Geopandas. 
# See more about ArcGIS API at https://github.com/Esri/arcgis-python-api and https://developers.arcgis.com/python/

# In[1]:


# In this course, we are not interested in maps like this!
import IPython.display as display
osm = """
<iframe width="425" height="350" frameborder="0" scrolling="no" marginheight="0" marginwidth="0" src="https://www.openstreetmap.org/export/embed.html?bbox=-117.24879741668703%2C32.87708229664578%2C-117.23815441131593%2C32.894921239943265&amp;layer=mapnik" style="border: 1px solid black"></iframe><br/><small><a href="https://www.openstreetmap.org/#map=16/32.8860/-117.2435">View Larger Map</a></small>
"""
display.HTML(osm)


# In[2]:


import arcgis
from arcgis.gis import GIS
import pandas as pd
import numpy as np

arcgis.__version__


# The first step is to connect to GIS server at arcgis.com. For advanced operations you will need to specify your username and password

# In[10]:


# Connect to GIS server
# general form: gis = GIS("http://arcgis.com", "username", "password")
# gis = GIS() # anonymous connection

# OR:

gis = GIS(username='krganapa_UCSDOnline')


# Suppose we are creating a bike paths map for San Diego. Need to find these data first. 
# 
# We can search for GIS content (data, services - eventually arcgis notebooks) using a Content Manager object. Search can have global scope, or can be limited to your organization, etc.
# 
# Notice that there are different types of content that one can find: data files such as CSV and Excel, GeoJSON, services, geodatabases, feature collections, shapefiles, different types of layers, maps and map documents, web scenes. Eventually it will include ArcGIS notebooks (in v 1.7) Can also include wild card search. 

# In[11]:


public_content = gis.content.search("Bike San diego", item_type="Feature Layer", max_items=10, outside_org=True)

# un-comment this to see other types of available data
# public_content = gis.content.search("Bike San diego", max_items=20)

# other options:

# public_content = gis.content.search("title:Puget Sound Traffic Incidents", item_type="Feature Service", outside_org=True)

# my_content = gis.content.search(query="owner:myself", item_type="csv")


# In[12]:


public_content


# In the list below, you can click on any data item to show its properties in Arcgis Online

# In[13]:


# iterate over the found items, and display them
from IPython.display import display
for item in public_content:
    display(item)


# Let's now create a base map, and we'll layer the found bike data over it

# In[14]:


map1 = gis.map('San Diego, CA')

# optionally, create a map in 3D, at specific zoom level:
# map1 = gis.map('San Diego, CA', zoomlevel = 4, mode="3D")

map1


# In[15]:


#get the item we like
bike_collisions = public_content[4]

#add to map
map1.add_layer(bike_collisions)


# In[16]:


bike_routes = public_content[7]
map1.add_layer(bike_routes)


# In[17]:


# explore the map object, recenter it
map1.center
map1.center = [32.877,-117.2374]
map1.basemaps
map1.basemap = 'hybrid'


# In[18]:


landsat_list = gis.content.search('"Landsat"', 'Imagery Layer')


# In[19]:


landsat_list


# In[22]:


landsat_ms = landsat_list[0]
map1.add_layer(landsat_ms)


# We would need to remove the bike layer, and then render it again on top of the landsat image

# In[23]:


map1.remove_layers(bike_routes)
map1.remove_layers(bike_collisions)
map1.add_layer(bike_routes)
map1.add_layer(bike_collisions)
map1.layers


# Let's find coordinates of San Diego. The process is called Geocoding

# In[24]:


from arcgis.geocoding import geocode
area = geocode('San Diego')
len(area)
for i in area:
    print(i["attributes"]["Type"], i["attributes"]["LongLabel"], i["location"])


# Notice that there are many objects with San Diego in the name, and they have different types

# In[25]:


area


# In[ ]:





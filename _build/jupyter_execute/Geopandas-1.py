#!/usr/bin/env python
# coding: utf-8

# ##  Intro to Geopandas-I

# ## Geopandas, and standard vector primitives 
# 
# **Geopandas** is a package used to process vector spatial data - though it can be used in conjunction with raster libraries such as rasterio. **Vector** data are typically used to represent discrete geometric objects which can be modeled as points, lines and polygons. By contrast, **raster** representations are often used to show continuously varying fields, where we can measure or estimate a value at any given location. Some spatial data structures (e.g., TIN) don't fall into this simplistic classification - but we'll cover them later.
# 
# Some of the most common types of planar vector entities include Points, Lines, Polygons, and their multipart varieties: Multi-Points, Multi-Lines, Multi-Polygons.  These  types are defined in OGC Simple Features spec, also adopted as ISO 19125 (https://en.wikipedia.org/wiki/Simple_Features). 
# 
# **New terms:**
# 
# **Open Geospatial Consortium** (OGC, https://www.opengeospatial.org/): international consortium of more than 530 organizations, to develop open geospatial standards.
# 
# **International Organization for Standardization** (ISO, https://www.iso.org): develops and publishes international standards.
# 
# The multipart varieties are used for entities that cannot be described by a single geometric primitive. For example, the state of Michigan is composed of two distinct peninsulas, and is often represented as Multi-Polygon. Regardless of the complexity of the underlying geometry, it is still a single feature.
# 
# There are also mixed collections (a Geometry Collection may include items of all dimensional types) - but most software packages don't work with them, and there is a limited set of operations you can do over such collections. 
# 
# Geopandas adds vector geometry and spatial operations to Pandas. It integrates with several open source libraries for specific operations: **fiona** for reading and writing files, **shapely** for geometric operations, **pyproj** for coordinate conversion, **pysal** for (some) thematic mapping, **folium** for interactive mapping, **rasterio** for raster manipulations, **rtree** for spatial indexing.
# 
# 

# ## When to use and not to use Geopandas
# Best for: exploratory data analysis with Jupyter notebooks, esp. if you are familiar with Pandas.
# 
# Not good for:
# * working across multiple coordinate systems (doesn't reproject on the fly; doesn't allow to mix projections in an operation)
# * when speed is an issue; 
# * when you need to produce publishable maps.

# In[ ]:


# Required libraries. Uncomment and run if needed.
get_ipython().system('pip install --user geopandas')
get_ipython().system('pip install --user descartes #to plot geopandas data frames')
get_ipython().system('pip install --user mapclassify #to develop map classifications. Formerly part of PySAL (until 2.0)')


# In[2]:


get_ipython().run_line_magic('matplotlib', 'inline')
import geopandas # to be able to see maps
import pandas as pd

import os
current_dir = os.getcwd()
print(current_dir)
geopandas.__version__


# Pandas uses __Series__; Geopandas uses __GeoSeries__, which is geometry column plus __index__.   The types of geometric objects that can be in the geometry column are Point, Line, Polygon, and their multipart extensions. **While a GeoSeries can mix geometric objects of different dimensions in one column, this is not recommended!!** Some operations won't work.
# 
# Reading data into Geopandas, using **read_file** from a shapefile. (can also read from URLs)
# 
# What is a **shapefile**? See https://en.wikipedia.org/wiki/Shapefile and https://gisgeography.com/arcgis-shapefile-files-types-extensions/
# Not the most convenient way to exchange spatial data...

# In[4]:


# Reading a shapefile into geopandas

shpFileIn = "/Users/kaushikramganapathy/Downloads/ZipCodes/ZipCodes.shp"

colorado = geopandas.read_file(shpFileIn)


# In[6]:


# Let's explore the "geometry" column
colorado.head(50)


# Geopandas data frame includes a __geometry__ column, which contains vector coordinates of standard types of shapes.
# 
# Notice that here geometry is presented as text, in the so called Well-Known Text (WKT) format, also specified by OGC and ISO (https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry). 
# 
# 

# The read_file method knows a lot of input formats, thanks to GDAL/OGR (https://www.gdal.org/) wrapped in fiona
# 
# Here is how you read a file from a URL (see http://geojson.xyz/). This is a useful collection of files that are easy to import.
# 

# In[7]:


# For example, retrieve Populated Places from geojson.xyz
url = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_populated_places_simple.geojson"
pop_places = geopandas.read_file(url)
pop_places.plot()

# writing files is similar: 
# colorado.to_file('zipcodes_colorado.shp') 


# GeoJSON uses the same set of graphic primitives, and a similar encoding: see https://en.wikipedia.org/wiki/GeoJSON and http://geojson.org. 
# 
# You experimented with GeoJSON in DSC80. Good sources of geojson files are: 
# 1. http://geojson.io (to create and view small GeoJSON files), 
# 1. https://github.com/datasets/geo-countries/blob/master/data/countries.geojson, and 
# 1. https://datahub.io/core/geo-countries (countries in GeoJSON), 
# 1. https://catalog.data.gov/dataset (US government data), 
# 1. http://geojson.xyz (random spatial datasets).
# 
# You may need those for projects!
# 
# Shapefiles is one of the most widely used  file formats. KML is another common one. But there are many others. See https://en.wikipedia.org/wiki/GIS_file_formats for a more complete list. Importing different formats into your project, and transforming them for use with your other data, is a big part of what GIS people do. 
# 
# In the Open Source world, OGR deals with vector data format translation (while GDAL deals with raster data). They are wrapped by fiona, which is what Geopandas rely on for reading and saving files (https://github.com/Toblerity/Fiona)  

# In[8]:


# let's refresh our pandas knowledge:

# how many records are in the dataframe
colorado.count()

# what are other ways to find the number of records?


# Notice that the records here have unique ZIP5 values. 
# See about zip codes at https://en.wikipedia.org/wiki/ZIP_Code ("Zone Improvement Plan", 5-digit zip codes in use since 1963).
# 
# Often, US administrative records are referenced by **FIPS Codes**. FIPS codes are used in many areas, not only as place codes.

# In[9]:


# look at a single polygon:

print(colorado.loc[0, 'NAME'])  # returns name of the first county
print(colorado.loc[0, 'geometry']) # returns geometry content of the first county
colorado.loc[0, 'geometry'] # plots the geometry


# In[10]:


# A brief pandas test...
# Guess what these operations do?
# Which of them would generate an error?
# Which two would produce the same result (almost)
# What will happen if we just run this cell?

colorado.iloc[0:20].plot()

# colorado.loc[300].plot()

colorado.loc[299:300].plot()

colorado.loc[{0,5,10,15,20}].plot()

colorado.loc[colorado['SHAPE_Area']> 5000000000].plot()

colorado.loc[299, 'geometry']


# ## Let's create a map!

# In[11]:


# PLOT will create a map using the Geometry column, and values in an attribute column

# Single symbol map
colorado.plot(figsize=(10,10))


# In[12]:


# map fragment: draw zip codes with coordinates south of 4200000
# cx is a coordinate-based indexer, in addition to standard Pandas indexes.

# What are standard indexes in pandas? 

# cx works over bounding boxes for each object: returns geometries that intersect a bounding box


south_colorado = colorado.cx[:,:4200000]

south_colorado.plot(figsize=(10,10))


# 
# New Term: **Bounding Box** (BBOX), also "minimum bounding rectangle (MBR)", "envelope": max extent of a 2D object in a given projection. Defined by minx, maxx, miny, maxy.
# Commonly used for spatial indexing; as part of metadata; for a simple query. 
# 
# Experiment with bounding boxes at https://boundingbox.klokantech.com/
# 

# In[13]:


# Choropleth map
# if we want to show values for a specific column, add "column = "
# most maps would need a legend

colorado.plot(column='NAME', figsize=(10,10), legend = True)

# what if you use a different column, such as NAME? Experiment. Is this a choropleth map?
# For categorical variables, it simply assigns a different color hue to different values. 
# The goal is to show qualitative differences  - so color value or saturation not to be used.
# Adding  categorical=True isn't really critical here. Don't use a sequential color map (eg no cmap='OrRd')

# colorado.plot(column='NAME', figsize=(10,10), legend = True, categorical=True)


# In[14]:


# Customize the choropleth map: specify a color map and add a legend
colorado.plot(column='SHAPE_Area', figsize=(10,10), cmap='hot', legend=True)

# Color maps are in https://matplotlib.org/users/colormaps.html (try hot, ocean, flag, terrain; Accent for categorical maps)


# __Choropleth maps__ is a very common way to start data analysis where data are summarized and presented by areal units. However, the message of the map will be different depending on what classification (clustering) method you chose. The range of values can be split into intervals that are equal in size ('equal_intervals'), or have approximately the same number of items in each interval (equal frequency, or 'quantiles'), or follow natural breaks in the distribution (some form of discriminant analysis, or optimal arrangement of values into classes. Basically, k-means clustering). See https://en.wikipedia.org/wiki/Jenks_natural_breaks_optimization; https://en.wikipedia.org/wiki/Choropleth_map 
# 
# How to select colors for a choroleth map: http://colorbrewer2.org/
# 
# __Let's look at the Powerpoint again!__
# 

# In[15]:


# Let's explore how different classification methods change the appearance of a map

import mapclassify
# https://github.com/geopandas/geopandas/issues/911. Some issues still with the move to Pysal 2.0.0 and the geopanas 0.4.1 fix

# Specifying classification sheme requires an additional library (originally a component of PySAL)
colorado.plot(column='SHAPE_Area', cmap='OrRd', scheme ='equal_interval', k=5, legend=True, figsize=(10,10))
colorado.plot(column='SHAPE_Area', cmap='OrRd', scheme ='fisher_jenks', k=5)
colorado.plot(column='SHAPE_Area', cmap='OrRd', scheme ='quantiles', k=5)


# In[18]:


# let's see how the values are clustered:
import seaborn as sns  # This allows us to easily and beautifully plot
sns.distplot(colorado['SHAPE_Area'], rug=True, kde=False)

# Let's try: Quantiles, EqualInterval, FisherJenks, NaturalBreaks

allbins = mapclassify.Quantiles(colorado['SHAPE_Area'], k=5)
allbins


# Think about the message of your map when you select symbology!
# 
# Now, let's look at another very common situation. To create a map, you often need to join geography and attribute data. Boundaries, lines, or point locations may come from a spatial data source and would contain some identifier for each record. Suppose these IDs (or some function of these IDs) match with IDs in another table. These could be country names or ISO codes; Zip codes, FIPS codesm names of natural features, etc. Then you need to join the two tables (one with geometry, another without).

# In[19]:


# Let's look at a world map, and explore the table structure behind it

world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
wmap = world.plot()
wmap.set_title("World Map")


# In[20]:


world.head()


# In[21]:


# remove areas we are not interested in:

world = world[(world.pop_est>0) & (world.name!= 'Antarctica')]
world.plot()


# In[44]:


# now, let's import an Excel file with some data
# the source of the data is: http://sdgindex.org/reports/2018/ 
# (Citation: Sachs, J., Schmidt-Traub, G., Kroll, C., Lafortune, G., Fuller, G. (2018): 
# SDG Index and Dashboards Report 2018. New York: Bertelsmann Stiftung and Sustainable Development Solutions Network (SDSN).)
# see these data in SuAVE: https://suave-dev.sdsc.edu/main/file=ilyaj_SDG18_Geo.csv&views=1110101&view=bucket

country_data = pd.read_excel('/Users/kaushikramganapathy/Downloads/GlobalIndexResults_NEW.xlsx', header=None)
country_data.columns = country_data.iloc[1] 
country_data = country_data.iloc[2:,:]# country_data.head()


# In[45]:


country_data.head()


# In[46]:


# we can plot data that is already in the geodataframe, eg:

world.plot(column='pop_est', cmap='OrRd', k=5, legend=True, figsize=(10,10))


# In[47]:


# or we can map any variable that is in the Excel file, once we join it to the shapes.
# notice that 'iso_a3' in the shapefile should match 'id' in the excel file (this is a 3-letter country code)

merged_df = pd.merge(world, country_data, left_on='iso_a3', right_on='id',how='inner', indicator=True)

# notice types of join: inner, outer, left, right. We are joining gdf (left) with df (right).
# Inner: only keep rows where the merge “on” value exists in both the left and right dataframes (the default).
# Left: keep every row in the left dataframe. Add NaN or empty for missing values in the result.
# Right: keep every row in the right dataframe. Add NaN or empty for missing values in the result.
# Outer: keep every row in both left and right dataframes. Add NaN or empty for missing values in the result.

# may want to add indicator = True to create a "_merge" column (not useful for the inner join)

# more resources: https://chrisalbon.com/python/data_wrangling/pandas_join_merge_dataframe/; 
# http://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html; 
# https://www.youtube.com/watch?v=XMjSGGej9y8 


world2 = merged_df.plot(column = 'Unemployment rate (%)', cmap='OrRd',legend=True)

# It doesn't work! Why?!
# Well, maps (and other visual representations) are useful to spot data problems
merged_df.head()


# In[48]:


# In real world, there are ALWAYS problems with data... 
# Let's eyeball it

pd.set_option('display.max_columns', None)
country_data.head(200)

# country_data.info(verbose=True)


# In[49]:


# but doesn't work if there is a lot of data...

# country_data.describe()

# these are columns that have missing values 
country_data.isnull().any()

# or 
country_data.isna().any()

# (are they identical? Yes. Why pandas has two? 
# See https://datascience.stackexchange.com/questions/37878/difference-between-isna-and-isnull-in-pandas)

# alternatively:
# [col for col in country_data.columns if country_data[col].isnull().any()]



# In[50]:


# let's fix it; replace NaN with 0s
# is this a correct approach??

import numpy as np
merged_df.replace(np.nan, 0, regex=True, inplace=True)
world2 = merged_df.plot(column = 'Unemployment rate (%)', cmap='OrRd', figsize=(10,10))
# merged_df.plot(column = 'Unemployment rate (%)', figsize=(10,10),cmap='OrRd', legend=True, k=4)

# Here is how you can save the output as an image (but for publication-quality images better use other tools)
# fig = world2.get_figure() 
# fig.savefig("output.png", dpi=300)


# DISSOLVE is another very common operaiton when creating maps by areal units. Often, neighboring units have the same value, and the boundary between them is not needed. This is when you use DISSOLVE to aggregate such neighboring geometries with the same value. DISSOLVE removes interior boundaries of a set of polygons with the same attribute value and creates one new combined polygon.

# In[51]:


# Dissolving boundaries into larger areas
world2 = merged_df.plot(column = 'UN sub-region name', figsize=(20,20))


# In[52]:


# create a new gdf with a subset of columns, and decide how to aggregate values in these columns (aggfunc)
# need at least three columns in the new gdf
cols = ['geometry','pop_est','UN sub-region name']
sub_regions = merged_df[cols].dissolve(by='UN sub-region name', aggfunc = 'sum', as_index=False)
sub_regions.plot(figsize=(20,20), column = 'UN sub-region name')

# aggfunc specifies how to compute attributes for the resultant polygons (first; last; min; max; sum; mean; median)

# Which non-spatial function is it similar to?


# In[53]:


# what do you expect to get as content of this merged_df?

sub_regions[cols].head(50)


# Maps often show more than one variable, and these variables may represent different types of geometries. **Organizing maps by layers of information is a very common approach in GIS and mapping.** Here, we will add a point layer of cities on top of the polygon layer.
# 
# Note that when maps get a bit more complex, with multiple layers and different symbology, you may want to have more control over the process. Composing the plot with matplotlib will give you more options. But overall: if you want production quality maps, do it in dedicated software.

# In[54]:


# now, let's add some more data to the map
cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))
cities.plot(marker='*', color='green', markersize=8);


# In[55]:


world2 = merged_df.plot(column = 'UN sub-region name', legend=True, figsize=(20,20))
cities.plot(ax=world2, marker='o', color='black', markersize=8);

# on this map, there is a base (world2), and cities are drawn on top of it


# In[56]:


# Beautifications:

# transparency:
world2 = merged_df.plot(column = 'UN sub-region name', legend=True, figsize=(20,20), alpha=0.2)
cities.plot(ax=world2, marker='o', color='black', markersize=50);

# remove axes:
world2 = merged_df.plot(column = 'UN sub-region name', legend=True, figsize=(20,20), alpha=0.2)
cities.plot(ax=world2, marker='o', color='black', markersize=8);
world2.set_axis_off()

# specifying line styles:

world2 = merged_df.plot(column = 'UN sub-region name', legend=True, figsize=(20,20), alpha=0.2, edgecolor='0.7', linewidth=3)
cities.plot(ax=world2, marker='*', color='black', markersize=8);
world2.set_axis_off()

# the map can be also plotted as matplotlib figure (like you did in DSC80?)

import matplotlib.pyplot as plt
fig, ax = plt.subplots(1, figsize=(20, 20))
ax.set_title ("World Cities")
ax.annotate('Credits: Your Name', xy=(2, 2))
world2 = merged_df.plot(column = 'Unemployment rate (%)', figsize=(10,10), alpha=0.9, edgecolor='0.7', linewidth=3, ax=ax, cmap='Blues')
cities.plot(ax=world2, marker='o', color='black', markersize=8);
world2.set_axis_off()
sm = plt.cm.ScalarMappable(cmap='Blues')
vmin, vmax = 0, 1
norm=plt.Normalize(vmin=vmin, vmax=vmax)
sm._A = []
cbar = fig.colorbar(sm, orientation='horizontal')


# Now, let's create a proportional symbol map overlaid over a choropleth map. First, we need to define point locations to which we will attach country data. we'll use the same lowres world map, and create centroids for each country

# In[57]:


rep_points = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
rep_points = rep_points[(rep_points.pop_est>0) & (rep_points.name!= 'Antarctica')]

rep_points['centroid'] = rep_points.centroid

# or:

rep_points['centroid'] = rep_points.representative_point()

# in the second case, Geopandas ensures that the point is within the originating polygon


# In[58]:


# Now, switch geometry from polygon to points (ie, set a new active geometry column)

rep_points = rep_points.set_geometry('centroid')
rep_points.plot()


# In[59]:


world['gdp_per_cap'] = world['gdp_md_est'] / world['pop_est']

base = world.plot(figsize=(20,20), column='gdp_per_cap', alpha=1, cmap='OrRd')

pop_max = rep_points['pop_est'].max()
pop_min = rep_points['pop_est'].min()

max_size = 2000
min_size = 2
rep_points.plot(ax=base, marker='o', color='black', markersize=min_size + (max_size-min_size)*(rep_points['pop_est']/pop_max));

# notice that markersize is not a constant; it is now computed based on other values
# this is a very simple way to scale points; other scaling functions can be used


# In[60]:


# plotting with folium
import folium
from folium.plugins import MarkerCluster


# In[61]:


rep_points.head()

# We can either use a new layer (eg cities, as below), 
# or transform the world geodataframe from polygons into points - as in the next cell

cities = geopandas.read_file(geopandas.datasets.get_path('naturalearth_cities'))


# In[62]:


rep_points.head()
rep_points.set_geometry('centroid')
rep_points.drop(['geometry'], axis=1, inplace=True)
rep_points.rename(columns={'centroid': 'geometry'}) # need to rename to avoid issues with other packages


# In[63]:


map1 = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")
# pjson = cities.to_json()


pjson = rep_points.to_json()

rps = folium.features.GeoJson(pjson)
map1.add_child(rps)


map1


# In[69]:


import folium
from folium.plugins import MarkerCluster


# In[70]:


# same, using MarkerCluster
map1 = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")
locations = []
for idx, row in cities.iterrows():
    locations.append([row['geometry'].y, row['geometry'].x])
    
map1.add_child(MarkerCluster(locations=locations))


# In[71]:


# references: https://ocefpaf.github.io/python4oceanographers/blog/2015/12/14/geopandas_folium/ 
# (see how to add popups)
# Also https://github.com/python-visualization/folium/blob/master/examples/GeoJSON_and_choropleth.ipynb 
# for the use of the Choropleth class

# set the map center and zoom
map1 = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")

# Then you can simply pass a geodataframe to the Choropleth class, 
# and specify the key (in the geodataframe) to be used for mapping
# You can convert to json (eg wjson = world.to_json() ) and explore it to make sure that the key_on is set correctly.
# Because internally it uses GeoJson class


folium.Choropleth(
    geo_data=world,
    data=world,
    columns=['name','gdp_per_cap'],
    key_on='feature.properties.name',
    fill_color='YlGn',
    fill_opacity=0.9,
    line_weight=2,
#     bins=[0, 0.01, 0.02, 0.03, 0.05, 0.1, 0.2],
    legend_name='GDP per Capita',
    highlight=True, 
    nan_fill_color ='purple'
).add_to(map1)

map1.add_child(MarkerCluster(locations=locations))

map1


# Check out folium examples at https://github.com/python-visualization/folium - they are cool!

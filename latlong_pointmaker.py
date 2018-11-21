
# coding: utf-8

# In[2]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
import shapely as sp
from shapely.geometry import Point
def ll_pointmaker(dset, color = 'ro'):
    dpoints = []
    for n in range(len(dset)):
        point = Point((dset.PlanetographicLatitude[n]),(dset.Longitude[n]))
        dpoints.append(point)
    
    for n in range(len(dset)):
        plt.plot(dpoints[n].x, dpoints[n].y, color)
        plt.xlabel('Planetographic Latitude')
        plt.ylabel('Longitude')



# coding: utf-8

# In[3]:


import pandas as pd
from planet4 import io
import geopandas as gp
import shapely
from planet4 import markings
from shapely.ops import unary_union


# In[4]:


fans = pd.read_csv(r"C:\Users\Zade\Documents\python_from_others\planet4_results\P4_catalog_v1.1_L1C_cut_0.5_fan.csv")

blotches = pd.read_csv(r"C:\Users\Zade\Documents\python_from_others\planet4_results\P4_catalog_v1.1_L1C_cut_0.5_blotch.csv")


# In[15]:


def get_tile_fraction(tile_id, scope = 'hirise'):
    id_ = tile_id
    blotch = blotches[blotches.tile_id == io.check_and_pad_id(id_)]
    fan = fans[fans.tile_id == io.check_and_pad_id(id_)]
    gs_blotch = gp.GeoSeries([markings.Blotch(row, scope).to_shapely() for _,row in blotch.iterrows()])
    gs_fans = gp.GeoSeries([markings.Fan(row, scope).to_shapely() for _,row in fan.iterrows()])
    gs = pd.concat([gs_blotch, gs_fans], ignore_index=True, sort=True)
    unionized = gs.unary_union
    squared_pixel_scale = fans.map_scale.iloc[0]**2
    area = unionized.area * squared_pixel_scale
    pixel_area = markings.IMG_X_SIZE * markings.IMG_Y_SIZE
    tile_area = pixel_area * squared_pixel_scale
    fraction = area / tile_area
    return fraction


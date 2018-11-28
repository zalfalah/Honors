
import pandas as pd
from planet4 import io
import geopandas as gp
import shapely
from planet4 import markings
from shapely.ops import unary_union

fans = pd.read_csv(r"C:\Users\Zade\Documents\python_from_others\planet4_results\P4_catalog_v1.1_L1C_cut_0.5_fan.csv")
blotches = pd.read_csv(r"C:\Users\Zade\Documents\python_from_others\planet4_results\P4_catalog_v1.1_L1C_cut_0.5_blotch.csv")

def get_tile_fraction(tile_id, scope = 'hirise'):
    '''
    Takes a tile_id and returns the fractional ground coverage of both fans and blotches within that tile
    
    Parameters
    __________
    tile_id : str
        The tile_id you wish to find coverage for
    scope : str, optional
        Select between hirise (default) or other scopes 
        
    Returns
    _______
    float
        The fraction of the ground covered by both fans and blotches for your given tile as a float
    '''
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

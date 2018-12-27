from pathlib import Path

import geopandas as gp
import pandas as pd
from shapely.ops import unary_union

from planet4 import io, markings
from my_io import get_fans_blotches, get_tilecoords, get_metadata


def get_geoseries(fans, blotches, scope='hirise'):
    gs_blotch = gp.GeoSeries(
        [markings.Blotch(row, scope=scope).to_shapely() for _, row in blotches.iterrows()]
    )
    gs_fans = gp.GeoSeries(
        [markings.Fan(row, scope=scope).to_shapely() for _, row in fans.iterrows()]
    )
    return pd.concat([gs_blotch, gs_fans], ignore_index=True, sort=True)

    
def get_tile_fraction(tile_id, scope="hirise"):
    """
    Takes a tile_id and returns the fractional ground coverage of both fans and blotches within that tile

    Parameters
    ==========
    tile_id : str
        The tile_id you wish to find coverage for
    scope : str, optional
        Select between hirise (default) or other scopes

    Returns
    =======
    float
        The fraction of the ground covered by both fans and blotches for your given tile as a float
    """
    id_ = tile_id
    fans, blotches = get_fans_blotches()
    blotch = blotches[blotches.tile_id == io.check_and_pad_id(id_)]
    fan = fans[fans.tile_id == io.check_and_pad_id(id_)]
    gs = get_geoseries(fan, blotch)
    unionized = gs.unary_union
    total_pixels = markings.IMG_X_SIZE * markings.IMG_Y_SIZE
    fraction = unionized.area / total_pixels
    return fraction


def get_total_npixels(obsid):
    """Calculate the actual number of pixels shown in Planet Four
    
    Parameters
    ==========
    obsid : str
        The HiRISE obsid for which the fraction should be calculated.
    
    Returns
    =======
    int
        Number of pixels of all tiles shown in Planet Four
    """
     # we read the number of pixels from planet4.markings and subtract the overlaps
    new_pixels_per_tile = (markings.IMG_X_SIZE-100) * (markings.IMG_Y_SIZE-100)
    tile_coords = get_tilecoords().query("obsid == @obsid")
    no_of_tiles = tile_coords['x_tile'].max() * tile_coords['y_tile'].max()
    return no_of_tiles * new_pixels_per_tile
   
    
def get_fans_blotches_per_obsid(obsid):
    fans, blotches = get_fans_blotches()
    fans_per_obsid = fans.query("obsid == @obsid")
    blotches_per_obsid = blotches.query("obsid == @obsid")
    return fans_per_obsid, blotches_per_obsid
    

def get_obsid_fraction(obsid):
    """
    Calculate the covered fraction for a given HiRISE obsid.

    Parameters
    ==========
    obsid : str
        The HiRISE obsid for which the fraction should be calculated.

    Returns
    =======
    float
        The fraction of the area of this HiRISE image that was shown in
        PlanetFour that is covered by either fan or blotch objects.
    """
    fans, blotches = get_fans_blotches_per_obsid(obsid)
    gs = get_geoseries(fans, blotches)
    unionized = gs.unary_union
    total_pixels = get_total_npixels(obsid)
    fraction = unionized.area / total_pixels
    return fraction


def get_Ls(obsid):
    metadata = get_metadata()
    metadata.set_index("OBSERVATION_ID", inplace=True)
    return metadata.at[obsid, "SOLAR_LONGITUDE"]
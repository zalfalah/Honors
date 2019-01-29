import geopandas as gp
import pandas as pd

from planet4 import io, markings
from my_io import get_fans_blotches, get_tilecoords, get_metadata, get_region_names


def get_geoseries(fans, blotches, scope="hirise"):
    gs_blotch = gp.GeoSeries(
        [
            markings.Blotch(row, scope=scope).to_shapely()
            for _, row in blotches.iterrows()
        ]
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
    new_pixels_per_tile = (markings.IMG_X_SIZE - 100) * (markings.IMG_Y_SIZE - 100)
    tile_coords = get_tilecoords().query("obsid == @obsid")
    no_of_tiles = tile_coords["x_tile"].max() * tile_coords["y_tile"].max()
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

#Trying to get Latitude
def get_Lat(obsid):
    metadata = get_metadata()
    metadata.set_index("OBSERVATION_ID", inplace=True)
    return metadata.at[obsid, "IMAGE_CENTER_LATITUDE"]

def get_obsids_for_region(region_name, year=None):
    region_names = get_region_names()
    region_names.roi_name = region_names["roi_name"].str.lower()
    roi = region_name.lower()
    if year is None:
        return region_names.query("roi_name == @roi").obsid
    else:
        return region_names.query("roi_name == @roi and MY == @year").obsid


class CoverageCalculator:
    which_values = ["fans", "blotches", "both"]

    def __init__(self):
        self.read_data()
        self.read_metadata()
        print("Note that obsid must be set to a string value before this works.")
        self._obsid = None
        self.union_done = False
        self._which = "both"

    @property
    def which(self):
        return self._which

    @which.setter
    def which(self, value):
        if value not in self.which_values:
            raise ValueError(f"value must be one of {self.which_values}.")
        self._which = value
        self.union_done = False

    def read_data(self):
        print("Reading fans and blotches in...")
        self.fans, self.blotches = get_fans_blotches()
        print("Done.")

    def read_metadata(self):
        print("Reading metadata...")
        self.meta = get_metadata().set_index("OBSERVATION_ID")
        print("Done.")

        
    #Trying to add PlanetographicLatitude
    @property
    def Lat(self):
        return self.meta.at[self.obsid, "IMAGE_CENTER_LATITUDE"]
        
    @property
    def Ls(self):
        return self.meta.at[self.obsid, "SOLAR_LONGITUDE"]

    @property
    def obsid(self):
        if self._obsid is not None:
            return self._obsid
        else:
            raise ValueError("obsid must be set.")

    @obsid.setter
    def obsid(self, value):
        self._obsid = value
        self.union_done = False

    @property
    def fans_per_obsid(self):
        if self.obsid is not None:
            return self.fans.query("obsid == @self.obsid")
        else:
            raise ValueError("obsid is not set.")

    @property
    def blotches_per_obsid(self):
        if self.obsid is not None:
            return self.blotches.query("obsid == @self.obsid")
        else:
            raise ValueError("obsid is not set.")

    @property
    def gs_blotches(self):
        return gp.GeoSeries(
            [
                markings.Blotch(row, scope="hirise").to_shapely()
                for _, row in self.blotches_per_obsid.iterrows()
            ]
        )

    @property
    def gs_fans(self):
        return gp.GeoSeries(
            [
                markings.Fan(row, scope="hirise").to_shapely()
                for _, row in self.fans_per_obsid.iterrows()
            ]
        )

    @property
    def gs_combined(self):
        if self.which == "both":
            return pd.concat(
                [self.gs_fans, self.gs_blotches], ignore_index=True, sort=True
            )
        elif self.which == "fans":
            return self.gs_fans
        elif self.which == "blotches":
            return self.gs_blotches

    @property
    def union(self):
        if not self.union_done:
            self._union = self.gs_combined.unary_union
            self.union_done = True
        return self._union

    @property
    def total_npixels(self):
        return get_total_npixels(self.obsid)

    @property
    def covered_fraction(self):
        return round(self.union.area / self.total_npixels, 3)

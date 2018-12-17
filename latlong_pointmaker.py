import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shapely as sp
from shapely.geometry import Point


def ll_pointmaker(dset, color='ro'):
    """
    Takes a dataset, creates points for each object with (x,y) values being represented by (Planetographic Latitude, Longitude)
    then graphs these points, defaults each point to be a red dot

    Parameters
    __________
    dset : dataframe
        The dataframe from which we take our Lat/Long Coordinates
    color : str
        A color selection option for our resulting graph, default red dots

    Returns
    _______
    plot
        Planetographic Latitude vs. Longitude for each object in our dataset
    """
    dpoints = []
    for n in range(len(dset)):
        point = Point((dset.PlanetographicLatitude[n]), (dset.Longitude[n]))
        dpoints.append(point)

    for n in range(len(dset)):
        plt.plot(dpoints[n].x, dpoints[n].y, color)
        plt.xlabel('Planetographic Latitude')
        plt.ylabel('Longitude')

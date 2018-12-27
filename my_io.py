import sys
from pathlib import Path
import pandas as pd

if sys.platform == "darwin":
    rootpath = Path("/Users/klay6683/Dropbox/data/planet4/p4_for_Zade/P4_catalog_v1.1/")
else:
    rootpath = Path("C:/Users/Zade/Documents/python_from_others/planet4_results/")

def get_fans_blotches():
    fans = pd.read_csv(rootpath / "P4_catalog_v1.1_L1C_cut_0.5_fan.csv")
    blotches = pd.read_csv(rootpath / "P4_catalog_v1.1_L1C_cut_0.5_blotch.csv")
    return fans, blotches


def get_tilecoords():
    return pd.read_csv(rootpath / "P4_catalog_v1.1_tile_coords_final.csv")


def get_metadata():
    return pd.read_csv(rootpath / "P4_catalog_v1.1_metadata.csv")
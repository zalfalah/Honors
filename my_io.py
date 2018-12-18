import sys
from pathlib import Path

if sys.platform == "darwin":
    rootpath = Path("/Users/klay6683/Dropbox/data/planet4/p4_for_Zade/P4_catalog_v1.1/")
else:
    rootpath = Path("C:/Users/Zade/Documents/python_from_others/planet4_results/")

fans = pd.read_csv(rootpath / "P4_catalog_v1.1_L1C_cut_0.5_fan.csv")
blotches = pd.read_csv(rootpath / "P4_catalog_v1.1_L1C_cut_0.5_blotch.csv")

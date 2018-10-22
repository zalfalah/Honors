import pandas as pd
import seaborn as sns
import os
from pathlib import Path
if os.environ['USER'] == 'klay6683':
    basedir = Path("/Users/klay6683/Dropbox/data/planet4/p4_for_Zade/P4_catalog_v1.1/")
else:
    basedir = Path("C:\Users\Zade\Desktop\HonorsMaterials\ForTask1\p4_analysis\P4_catalog_v1.0\")
#this shouldn't be this long, basedir should be regardless of which pc it's on right? and the path above directs it to this
#ask michael
fans = basedir / "P4_catalog_v1.0_L1C_cut_0.5_fan_meta_merged.csv"
blotches = basedir / "P4_catalog_v1.0_L1C_cut_0.5_blotch_meta_merged.csv"

#this doesn't have types in it don't know if we need it.  Only do if we mix dsets
#can add an if to mix dsets, concat and add type identifiers.  Will that be necessary though? only mix once, already have it
def plot_counts_over_time(dset):
    """
    Takes a data set and plots its counts vs time (time being l_s)
    ------------------------
    Params:
    dset : dataframe
    The dataframe to be plotted vs time
    ------------------------
    Returns:
    dataframe marking id's plotted vs. l_s
    """
    groupset = (dset).groupby('obsid')
    dcl = groupset.marking_id.count()
    dcl = dcl.to_frame()
    #lvo is l_s_vs_obsid
    lvo = (dset).drop_duplicates(subset = 'obsid').set_index('obsid').l_s
    dcl = dcl.join(lvo)
    sns.scatterplot(data=dset, y = 'marking_id', x = 'l_s')

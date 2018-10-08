import pandas as pd
import seaborn as sns
import os
from pathlib import Path

if os.environ['USER'] == 'klay6683':
    basedir = Path("....")
else:
    basedir = Path("...")

fans = basedir / "..."
blotches = basedir / "...."


def plot_counts_over_time():

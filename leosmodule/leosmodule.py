"""Leos test module
Version: 1.0.0

Interaction analysis by CellphoneDB version 5.0.0 (CPDB).
<https://pypi.org/project/cellphonedb/>
<https://github.com/ventolab/CellphoneDB>

This tool has 2 main functions:
    * add_one: adds 1 to a number

Author: Leonhard Menschner <leonhard.menschner@ukdd.de>
Created: 2024.06.03
"""

# import standard modules
from datetime import datetime
from itertools import combinations, product
from pathlib import Path
import sys
import zipfile

# import other modules
from cellphonedb.src.core.methods import cpdb_statistical_analysis_method
from IPython.display import display
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill, Alignment, Font
from openpyxl.utils import get_column_letter
from scipy import sparse
from scipy.sparse import csr_matrix
from tqdm import tqdm
import h5py
import openpyxl
import pkg_resources
import scipy.io
import anndata as ad
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
pd.set_option("display.max_columns", 100)
pd.set_option("display.max_rows", None)



# checks correct installation
def requirement_check():
    """Prints installed packages and marks incorrect versions.
    """

    requirement_dict = {
        "python": {"min": "3.11"},
        "ipykernel": {"min": "6.28.0"},
        "IPython": {"min": "8.25"},
        "notebook": {"min": "7.0.8"},    # core module of Jupyter notebook
        "anndata": {"min": "0.10.8"},
        "cellphonedb": {"min": "5.0.1"},
        "geosketch": {"min": "1.2"},
        "h5py": {"min": "3.11.0"},
        "ktplotspy": {"min": "0.2.4"},
        "matplotlib": {"min": "3.9.0"},
        "numpy": {"min": "1.26.4"},
        "numpy_groupies": {"min": "0.11.1"},
        "openpyxl": {"min": "3.1.5"},
        "pathlib": {"min": "1.0.1"},
        "pandas": {"min": "2.2.2"},
        "requests": {"min": "2.32.3"},
        "scanpy": {"min": "1.10.2"},
        "scikit_learn": {"min": "1.5.1"},
        "scipy": {"min": "1.11.0"},
        "setuptools": {"min": "69.5.1"},
        "tqdm": {"min": "4.60", "max": "5.0"},
    }

    for package_name, version_range in requirement_dict.items():
        try:
            # get installed package version
            if package_name == "python":
                installed_version = pkg_resources.parse_version(f'{sys.version_info[0]}.{sys.version_info[1]}')
            else:
                installed_version = pkg_resources.parse_version(pkg_resources.get_distribution(package_name).version)
            # check for minimal requirement
            min_version = pkg_resources.packaging.version.parse(version_range["min"])
            range_str = f'(>={version_range.get("min")})'
            status = "correct" if min_version <= installed_version else "incorrect"
            # also check for maximal requirements if provided
            if version_range.get("max"):
                max_version = pkg_resources.packaging.version.parse(version_range["max"])
                range_str = f'(>={version_range.get("min")},<{version_range.get("max")})'
                status = "correct" if installed_version <= max_version else "incorrect"
            # print results
            if status == "correct":
                print(f'{package_name} version: {installed_version} is correct {range_str}')
            else:
                print(f'\033[1;31;48m{package_name} version: {installed_version} is {status} and should be {range_str}\033[0;0m')
        except pkg_resources.DistributionNotFound:
            print(f'\033[1;31;48m{package_name} is not found\033[0;0m')


##### function to add one #####
def add_one(number):
    return number + 1

##### functions used by several functions #####
def string_to_list(string):
    """Convert a string to a list if necessary.

    Parameters
    --------------------
    string : str, list[str]

    Returns
    --------------------
    list
    """
    
    return [string] if isinstance(string, str) else string
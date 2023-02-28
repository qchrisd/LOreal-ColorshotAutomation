
"""data_helpers.py: Contains helpful methods for acquiring and manipulating data files and data structures."""

## Imports
import pandas as pd

def get_filepaths(text_file):
    with open(text_file) as file:
        lines = file.read().splitlines()
        
    return lines


def get_data(file_paths):
    """Gets data from a list of excel spreadsheets.

    Args:
        file_paths (list): A list of file paths to get data from.
    """
    
    list_of_dfs = []
    for path in file_paths:
        current_file_df = pd.read_excel(path,
                                     sheet_name="Plan")
        list_of_dfs.append(current_file_df)
    
    all_data = pd.concat(list_of_dfs,
                         ignore_index=True,
                         axis=0)
    
    return all_data
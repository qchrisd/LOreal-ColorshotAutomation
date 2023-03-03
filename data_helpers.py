
"""data_helpers.py: Contains helpful methods for acquiring and manipulating data files and data structures."""

## Imports
import pandas as pd
import re

def get_filepaths(text_file):
    """Reads the data filepaths in from a file

    Args:
        text_file (string): File path for the text file that contains the paths to the data files.

    Returns:
        list: List of strings containing data file paths.
    """
    with open(text_file) as file:
        lines = file.read().splitlines()
        
    return lines


def get_data(file_paths):
    """Gets data from a list of excel spreadsheets.

    Args:
        file_paths (list): A list of file paths to get data from.
        
    Returns:
        pandas.Dataframe: Data from all files provided in the file_paths list 
    """
    
    list_of_dfs = []
    for path in file_paths:
        current_file_df = pd.read_excel(path,
                                     sheet_name="Plan")
        current_file_df["Date"] = pd.to_datetime(current_file_df["Date"],
                                                 format="%Y%m%d-%H%M%S")
        list_of_dfs.append(current_file_df)
    
    all_data = pd.concat(list_of_dfs,
                         ignore_index=True,
                         axis=0)
    
    return all_data


def get_missing_rows(df1, df2):
    """Returns rows in df1 that are not present in df2.

    Args:
        df1 (pandas.Dataframe): Dataframe that has additional rows.
        df2 (pandas.Dataframe): Dataframe to check against.

    Returns:
        _type_: _description_
    """
    merged_df = pd.merge(df1, df2,
                         how="outer",
                         indicator=True)
    missing_rows = merged_df[merged_df["_merge"] == "left_only"][df1.columns]
    return missing_rows


def find_standard(name_string: str):
    std_regex = re.compile(".*[Ss][Tt][Dd]$")
    if std_regex.search(name_string):
        return True
    return False


def mark_standards(data_set: pd.DataFrame):
    data_set["STD"] = data_set["Name"].apply(find_standard)
    return data_set


def extract_shade_name(name_string: str):
    if find_standard(name_string):
        name_string = name_string[:-3]
    return name_string


"""data_helpers.py: Contains helpful methods for acquiring and manipulating data files and data structures."""

## Imports
import pandas as pd
import numpy as np
import datetime
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
    """Determines if a string ends with "STD" tag in any case combination.

    Args:
        name_string (str): The string to check.

    Returns:
        bool: True if the name ends in the "STD" tag. False if not.
    """
    # std_regex = re.compile(".*[Ss][Tt][Dd]$")  # Filter for finding STD tag at the end of the line
    std_regex = re.compile(".*STD.*")
    if std_regex.search(name_string):
        return True
    return False


def mark_standards(data_set: pd.DataFrame):
    """Adds a column to a dataframe marking standards.

    Args:
        data_set (pd.DataFrame): Dataset containing a "Name" column filled with strings.

    Returns:
        pd.DataFrame: A new pandas dataframe with a "STD" column added.
    """
    data_set["STD"] = data_set["Name"].apply(find_standard)
    return data_set


def extract_shade_name(name_string: str):
    """Extracts a clean "token" shade name without a "STD" tag if present.

    Args:
        name_string (str): String to clean.

    Returns:
        str: A version of name_string without the "STD" tag.
    """
    if find_standard(name_string):
        name_string = name_string.replace("STD", "")
    return name_string


def mark_shade_names(data_set: pd.DataFrame):
    """Adds a column to a dataframe with clean tagless shade names.

    Args:
        data_set (pd.DataFrame): A dataset containing a "Name" column of strings.

    Returns:
        pd.DataFrame: A new pandas dataframe with a "ShadeName" column added.
    """
    data_set["ShadeName"] = data_set["Name"].apply(extract_shade_name)
    return data_set


def get_groups(data_set: pd.DataFrame):
    """Returns all possible groups based on date, shade name, and hair type

    Args:
        data_set (pd.DataFrame): Dataframe with at least columns `Date`, `ShadeName`, and `Fiber`.

    Returns:
        pd.DataFrame: DataFrame with the same column names where one row is one group.
    """
    groups = data_set.groupby([pd.Grouper(key="Date", freq="1D"),"ShadeName","Fiber"]).size().reset_index()
    groups = groups.drop(columns=[0])
    return groups
    
    
def filter_for_group(data: pd.DataFrame, 
                     group_date: datetime.datetime, 
                     shade_name: str, 
                     hair_type: str):
    """Gets a single set's data.

    Args:
        data (pd.DataFrame): Dataframe with all data points.
        group_date (datetime.datetime): The date to filter by
        shade_name (str): The shade name to filter by.
        hair_type (str): The hair type to filter by.

    Returns:
        pd.DataFrame: A truncated version of the dataset with just the desired criteria.
    """
    filter_criteria = np.where((data["Date"].dt.date == group_date.date()) &
                               (data["ShadeName"] == shade_name) &
                               (data["Fiber"] == hair_type))
    filtered_data = data.loc[filter_criteria]
    return filtered_data
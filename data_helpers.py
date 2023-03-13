
"""data_helpers.py: Contains helpful methods for acquiring and manipulating data files and data structures."""

## Imports
import math
from decimal import Decimal
import pandas as pd
import numpy as np
import datetime
import re
from colour.difference import delta_E


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


#TODO Refactor so there is no default of "Plan" for the sheet name
def get_data(file_paths: list,
             sheet_name: str = "Plan"):
    """Gets data from a list of excel spreadsheets.

    Args:
        file_paths (list): A list of file paths to get data from.
        
    Returns:
        pandas.Dataframe: Data from all files provided in the file_paths list 
    """
    
    list_of_dfs = []
    for path in file_paths:
        current_file_df = pd.read_excel(path,
                                     sheet_name=sheet_name)
        try:
            current_file_df["Date"] = pd.to_datetime(current_file_df["Date"],
                                                    format="%Y%m%d-%H%M%S")
        except:
            pass
        current_file_df["File Path"] = path
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
    missing_rows = missing_rows.reset_index(drop=True)
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
    groups = data_set.groupby([pd.Grouper(key="Date", freq="1D"),"Nuance","Fiber"]).size().reset_index()
    groups = groups.drop(columns=[0])
    return groups
    
    
def filter_for_group(data: pd.DataFrame, 
                     group_date: datetime.datetime, 
                     nuance: str, 
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
                               (data["Nuance"] == nuance) &
                               (data["Fiber"] == hair_type))
    filtered_data = data.loc[filter_criteria]
    return filtered_data


def calculate_colorimetry(data_std: pd.DataFrame,
                          data_comparison: pd.DataFrame):
    std_L = data_std.iloc[0]["L*"]
    std_a = data_std.iloc[0]["a*"]
    std_b = data_std.iloc[0]["b*"]
    std_C = math.sqrt(std_a**2 + std_b**2)
    std_h = data_std.iloc[0]["h°"]
    comparison_L = data_comparison.iloc[0]["L*"]
    comparison_a = data_comparison.iloc[0]["a*"]
    comparison_b = data_comparison.iloc[0]["b*"]
    comparison_C = math.sqrt(comparison_a**2 + comparison_b**2)
    comparison_h = data_comparison.iloc[0]["h°"]
    
    ave_C = (std_C + comparison_C)/2
    factor_G = 0.5 * (1 - math.sqrt(ave_C**7/(ave_C**7+25**7)))
    std_a_prime = std_a * (1 + factor_G)
    comparison_a_prime = comparison_a * (1 + factor_G)
    std_C_prime = math.sqrt(std_a_prime**2 + std_b**2)
    comparison_C_prime = math.sqrt(comparison_a_prime**2 + comparison_b**2)
    
    std_h_prime = math.degrees(math.atan2(std_a_prime,std_b))
    comparison_h_prime = math.degrees(math.atan2(comparison_a_prime, comparison_b))
    
    delta_h_prime = -(((comparison_h_prime - std_h_prime) + 180) % 360 - 180)  # Finds smallest angle from std to comparison where '-' is anticlockwise, '+' is clockwise
    
    std_lab = np.array([std_L, std_a, std_b]) 
    comparison_lab = np.array([comparison_L, comparison_a, comparison_b])
    delta_E2000 = delta_E(std_lab, comparison_lab,
                          method = "CIE 2000")
    
    round_digits = Decimal("1.000")
    delta_E2000 = float(Decimal(delta_E2000).quantize(round_digits))
    delta_L = float(Decimal(comparison_L-std_L).quantize(round_digits))
    delta_a = float(Decimal(comparison_a-std_a).quantize(round_digits))
    delta_b = float(Decimal(comparison_b-std_b).quantize(round_digits))
    delta_C = float(Decimal(comparison_C_prime-std_C_prime).quantize(round_digits))
    delta_h = float(Decimal(delta_h_prime).quantize(round_digits))
    delta_H = float(Decimal(2 * math.sqrt(std_C_prime * comparison_C_prime) * math.sin(math.radians(delta_h/2))).quantize(round_digits))
    
    return delta_E2000, delta_L, delta_a, delta_b, delta_C, delta_h, delta_H


def report_comparison(standard: pd.DataFrame,
                      comparison: pd.DataFrame):
    delta_E2000, delta_L, delta_a, delta_b, delta_C, delta_h, delta_H = calculate_colorimetry(standard, comparison)
    new_row = pd.DataFrame({
        "Name Standard":[standard.iloc[0]["Name"]],
        "Shade Standard":[standard.iloc[0]["Nuance"]],
        "FLA Standard":[standard.iloc[0]["Formula number"]],
        "Fiber Standard":[standard.iloc[0]["Fiber"]],
        "L* Standard":[standard.iloc[0]["L*"]],
        "a* Standard":[standard.iloc[0]["a*"]],
        "b* Standard":[standard.iloc[0]["b*"]],
        " ":[None],
        "Name Comparison":[comparison.iloc[0]["Name"]],
        "Shade Comparison":[comparison.iloc[0]["Nuance"]],
        "FLA Comparison":[comparison.iloc[0]["Formula number"]],
        "Fiber Comparison":[comparison.iloc[0]["Fiber"]],
        "L* Comparison":[comparison.iloc[0]["L*"]],
        "a* Comparison":[comparison.iloc[0]["a*"]],
        "b* Comparison":[comparison.iloc[0]["b*"]],
        "Notes":[""],
        "dE2000":[delta_E2000],
        "dL*":[delta_L],
        "da*":[delta_a],
        "db*":[delta_b],
        "dC":[delta_C],
        "dh":[delta_h],
        "dH (metric difference)":[delta_H]
    })
    return new_row


def write_all_data(all_data: pd.DataFrame,
                   output_file_path: str):
    with pd.ExcelWriter(output_file_path,
                        engine="xlsxwriter") as writer:
        all_data.to_excel(writer,
                          sheet_name="All Data",
                          index=False)


def write_report(good_data: pd.DataFrame,
               output_file_path: str):
    with pd.ExcelWriter(output_file_path,
                        engine='xlsxwriter') as writer:

        good_data.to_excel(writer,
                           sheet_name="Report",
                           index=False,
                           header=False,
                           startrow=1)
        workbook = writer.book
        worksheet = writer.sheets["Report"]
        worksheet.set_column("H:H", 1, workbook.add_format({"bg_color":"#595959"}))
        worksheet.set_column("Q:Q", 10, workbook.add_format({"bg_color":"#FCD5B4"}))
        worksheet.set_column("R:W", 10, workbook.add_format({"bg_color":"#D5E8FF"}))
        # worksheet.set_row(":W", 10, workbook.add_format({"bg_color":"#D5E8FF"}))

        # Add a header format.
        header_format = workbook.add_format({
            'bold': True,
            'text_wrap': True,
            'valign': 'top',
            'font_color': '#F2F2F2',
            'bg_color': '#595959',
            'border': 1})

        # Write the column headers with the defined format.
        for col_num, value in enumerate(good_data.columns.values):
            worksheet.write(0, col_num, value, header_format)


def write_bad_comparisons(all_data: pd.DataFrame,
                   output_file_path: str):
    with pd.ExcelWriter(output_file_path,
                        engine="xlsxwriter") as writer:
        all_data.to_excel(writer,
                          sheet_name="Bad comparisons",
                          index=False)
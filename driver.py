

"""driver.py: Drives the colorshot data automation and colorimetry calculations."""

## Imports
import pandas as pd
from data_helpers import (get_filepaths, 
                          get_data, 
                          get_missing_rows,
                          mark_standards,
                          mark_shade_names,
                          get_groups,
                          filter_for_group)

def driver():
    """Main method of the program.
    """
    
    # Get data held in the master file
    try:
        master_data = get_data(["./all_data.xlsx"])
    except:
        master_data = pd.DataFrame()
    
    # Get data from the files
    data_filepaths = get_filepaths("./data_filepaths.confidential")
    data = get_data(data_filepaths)
    
    # Find and process new data
    if master_data.columns.size == 0:
        for column_name in data.columns:
            master_data = master_data.assign(**{column_name:None})
    new_data = get_missing_rows(data, master_data)
    new_data = mark_standards(new_data)
    new_data = mark_shade_names(new_data)
    
    # Process sets
    sets = get_groups(new_data)
    print(sets)
    for index, row in sets.iterrows():
        date, shade_name, hair_type = row
        print(date, shade_name, hair_type)
        filtered_data = filter_for_group(new_data,
                                         date,
                                         shade_name,
                                         hair_type)
        print(filtered_data.head())
    #TODO Find sets of standards

## Main
if __name__ == "__main__":
    driver()
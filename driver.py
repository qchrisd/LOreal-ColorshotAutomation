

"""driver.py: Drives the colorshot data automation and colorimetry calculations."""

## Imports
import pandas as pd
from data_helpers import (get_filepaths, 
                          get_data, 
                          get_missing_rows,
                          mark_standards,
                          mark_shade_names,
                          get_groups,
                          filter_for_group,
                          report_comparison,
                          write_report)

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
    good_comparisons = []
    bad_comparisons = []
    sets = get_groups(new_data)
    
    # print(sets)  #! LOGGING
    
    for _, row in sets.iterrows():
        date, nuance, hair_type = row
        filtered_data = filter_for_group(new_data,
                                         date,
                                         nuance,
                                         hair_type).reset_index()
        
        # print(date, nuance, hair_type, list(filtered_data["ShadeName"]), filtered_data.shape[0], sum(filtered_data["STD"]))  #! Logging should be removed before final build

        if filtered_data.shape[0] <= 1:  # No comparisons can be made if there is only 1 data point in the set.
            bad_comparisons.append(filtered_data)
        elif sum(filtered_data["STD"]) < 1:  # No standards in the set
            bad_comparisons.append(filtered_data)
        elif sum(filtered_data["STD"]) >= 2:  # Too many standards for comparisons.
            #TODO Narrow filter band
            pass
        else:
            standard = filtered_data.loc[filtered_data["STD"] == True]
            for index in filtered_data.index:
                if index == standard.index:  # Skips testing standards against themselves
                    continue
                comparison = filtered_data.loc[index:index+1]
                good_comparisons.append(report_comparison(standard, comparison))
                
    good_comparisons = pd.concat(good_comparisons, ignore_index=True)
    
    
    write_report(good_comparisons,
               None,
               "./Test.xlsx")

    #TODO Back up file
    
    #TODO Write report file
    

## Main
if __name__ == "__main__":
    driver()


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
                          write_report,
                          write_all_data)

def driver():
    """Main method of the program.
    """
    
    # Get data held in the master file
    print("Getting previous ColorShot entries... ", end="", flush=True)
    try:
        master_data = get_data(["./all_data.xlsx"], sheet_name="All Data")
        print("Success")
    except:
        master_data = pd.DataFrame()
        print("Did not find a file. Creating a new dataframe.")
        
    # Get data held in the previous report files
    print("Getting previous report entries... ", end="", flush=True)
    try:
        previous_report_data = get_data(["./Colorimetry Report.xlsx"], sheet_name="Report")
        print("Success")
    except:
        previous_report_data = pd.DataFrame()
        print("Did not find a file. Creating a new dataframe.")
    
    # Get data from the files
    data_filepaths = get_filepaths("./data_filepaths.confidential")
    data = get_data(data_filepaths)
    
    # Find new data
    if master_data.columns.size == 0:
        for column_name in data.columns:
            master_data = master_data.assign(**{column_name:None})
    new_data = get_missing_rows(data, master_data)
    all_data = pd.concat([master_data, new_data], ignore_index=True)  # Update all_data table
    
    # Label new data for colorimetry
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
    
    # Handle edge cases where pd.concat() cannot merge comparisons.
    if len(good_comparisons) == 0:
        print("No new data found.")
        exit(0)
    elif len(good_comparisons) == 1:
        good_comparisons = good_comparisons[0]
    else:            
        good_comparisons = pd.concat(good_comparisons, ignore_index=True)

    # Process previous report data
    if previous_report_data.columns.size == 0:  # File did not exist
        for column_name in good_comparisons.columns:
            previous_report_data = previous_report_data.assign(**{column_name:None})
    report_data = pd.concat([previous_report_data, good_comparisons])
    
    #TODO Back up file

    # Write files
    write_all_data(all_data,
                   "./all_data.xlsx")
    write_report(report_data,
               "./Colorimetry Report.xlsx")
    

## Main
if __name__ == "__main__":
    driver()
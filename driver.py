

"""driver.py: Drives the colorshot data automation and colorimetry calculations."""

## Imports
import sys
import pandas as pd
from data_helpers import (get_filepaths, 
                          get_data, 
                          get_missing_rows,
                          mark_standards,
                          mark_shade_names,
                          process_sets,
                          get_groups,
                          write_report,
                          write_all_data,
                          write_bad_comparisons,
                          backup_file)

def driver():
    """Main method of the program.
    """
    
    # Get data held in the master file
    print("Getting previous ColorShot entries... ", end="", flush=True)
    try:
        master_data = get_data(["./all_data.xlsx"], sheet_name="All Data", include_path=False)
        print("Success")
    except FileNotFoundError as e:
        master_data = pd.DataFrame()
        print("Did not find a file. Creating a new dataframe.")
    except PermissionError as e:
        print("Failed")
        print("\nThe all_data.xlsx file cannot be accessed. You probably have it open or the permissions for the folder are wonky. Check this and try again.")
        sys.exit(1)
        
    # Get data held in the previous report files
    print("Getting previous report entries... ", end="", flush=True)
    try:
        previous_report_data = get_data(["./Colorimetry Report.xlsx"], sheet_name="Report")
        print("Success")
    except FileNotFoundError as e:
        previous_report_data = pd.DataFrame()
        print("Did not find a file. Creating a new dataframe.")
    except PermissionError as e:
        print("Failed")
        print("\nThe Colorimetry Report.xlsx file cannot be accessed. You probably have it open or the permissions for the folder are wonky. Check this and try again.")
        sys.exit(1)
    
    # Get data from the files
    data_filepaths = get_filepaths("./data_filepaths.confidential")
    data = get_data(data_filepaths)
    
    # Find new data
    if master_data.columns.size == 0:
        for column_name in data.columns:
            master_data = master_data.assign(**{column_name:None})
    new_data = get_missing_rows(data, master_data)
    
    # Label new data for colorimetry
    new_data = mark_standards(new_data)
    new_data = mark_shade_names(new_data)
    
    # Process sets
    sets = get_groups(new_data)
    good_rows, good_comparisons, bad_comparisons = process_sets(sets, new_data)
    
    # Handle edge cases where pd.concat() cannot merge list.
    write_all_data_flag = True
    if len(good_rows) == 0:
        write_all_data_flag = False
    elif len(good_rows) == 1:
        all_data = good_rows[0]
    else:
        good_rows = pd.concat(good_rows, ignore_index=True)
        all_data = pd.concat([master_data, good_rows], ignore_index=True)
    
    write_report_flag = True
    if len(good_comparisons) == 0:
        print("No new comparisons found.")
        write_report_flag = False
    elif len(good_comparisons) == 1:
        good_comparisons = good_comparisons[0]
    else:            
        good_comparisons = pd.concat(good_comparisons, ignore_index=True)
    
    write_bad_comparisons_flag = True
    if len(bad_comparisons) == 0:
        write_bad_comparisons_flag = False
    elif len(bad_comparisons) == 1:
        bad_comparisons = bad_comparisons[0]
        print("Some data points could not be assigned a set. Check the 'Bad Comparisons' file for this data.")
    else:
        bad_comparisons = pd.concat(bad_comparisons, ignore_index=True)
        print("Some data points could not be assigned a set. Check the 'Bad Comparisons' file for this data.")
    print("")

    # Process previous report data
    if previous_report_data.columns.size == 0:  # File did not exist
        for column_name in good_comparisons.columns:
            previous_report_data = previous_report_data.assign(**{column_name:None})

    # Back up files
    backup_file("all_data.xlsx")
    backup_file("Colorimetry Report.xlsx")

    # Write files
    if write_all_data_flag:
        write_all_data(all_data,
                    "./all_data.xlsx")
    if write_report_flag:
        report_data = pd.concat([previous_report_data, good_comparisons])
        write_report(report_data,
                     "./Colorimetry Report.xlsx")
    if write_bad_comparisons_flag:
        write_bad_comparisons(bad_comparisons,
                            "./Bad Comparisons.xlsx")
    

## Main
if __name__ == "__main__":
    driver()
    print("\nFinished. Exiting the program.\n")
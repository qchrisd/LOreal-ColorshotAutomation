

"""driver.py: Drives the colorshot data automation and colorimetry calculations."""

## Imports
import pandas as pd
from data_helpers import get_filepaths, get_data, get_missing_rows

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
    
    # Find new data
    if master_data.columns == []:
        master_data.columns = data.columns
    new_data = get_missing_rows(data, master_data)
    
    #TODO Find sets of standards

## Main
if __name__ == "__main__":
    driver()


"""driver.py: Drives the colorshot data automation and colorimetry calculations."""

## Imports
from data_helpers import get_filepaths, get_data


def driver():
    """Main method of the program.
    """
    data_filepaths = get_filepaths("./data_filepaths.confidential")
    data = get_data(data_filepaths)

## Main
if __name__ == "__main__":
    driver()
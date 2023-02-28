
## Imports
import pytest
import pandas as pd

# Testing module
from data_helpers import get_filepaths, get_data, get_missing_rows


def test_get_filepaths_integration():
    expected = ["G:\Colorshot-MS\Test File 1.xlsx",
                "G:\Colorshot-MS\Test File 2.xlsx"]
    actual = get_filepaths("./tests/integration_files/test_filepaths.txt")
    assert actual == expected
    

@pytest.mark.parametrize("test_cases,expected",
                         [(["./tests/integration_files/Test File 1.xlsx", "./tests/integration_files/Test File 2.xlsx"],
                           pd.read_excel("./tests/integration_files/get_data expected.xlsx")),
                          (["./tests/integration_files/Test File 1.xlsx"],
                           pd.read_excel("./tests/integration_files/Test File 1.xlsx", sheet_name="Plan"))
                          ])
def test_get_data(test_cases, expected):
    actual = get_data(test_cases)
    pd.testing.assert_frame_equal(actual, expected)
    
    
    
if __name__ == "__main__":
    test_get_filepaths_integration()
    test_get_data()
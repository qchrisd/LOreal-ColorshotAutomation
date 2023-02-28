
"""test_data_helpers.py: Unit tests for data_helpers.py"""

## Imports
import pandas as pd
import numpy as np

from data_helpers import get_missing_rows


def test_get_missing_rows():
    df1 = pd.DataFrame({"col1":[1,2,3,4,5],
                        "col2":["a","b","c","d","e"]})
    df2 = pd.DataFrame({"col1":[2,3,4],
                        "col2":["b","c","d"]})
    expected = pd.DataFrame({"col1":[1,5],
                             "col2":["a","e"]})
    actual = get_missing_rows(df1, df2)
    assert np.array_equal(actual.values, expected.values)
     
     
if __name__ == "__main__":
    test_get_missing_rows()
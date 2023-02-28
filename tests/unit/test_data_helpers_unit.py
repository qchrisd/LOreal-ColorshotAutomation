
"""test_data_helpers.py: Unit tests for data_helpers.py"""

## Imports
import pytest
import pandas as pd
import numpy as np

from data_helpers import get_missing_rows

@pytest.mark.parametrize("df1,df2,expected",
                         [(pd.DataFrame({"col1":[1,2,3,4,5], "col2":["a","b","c","d","e"]}),
                           pd.DataFrame({"col1":[2,3,4], "col2":["b","c","d"]}),
                           pd.DataFrame({"col1":[1,5], "col2":["a","e"]})),
                          (pd.DataFrame({"col1":[1,2,3,4,5], "col2":["a","b","c","d","e"]}),
                           pd.DataFrame({"col1":[], "col2":[]}),
                           pd.DataFrame({"col1":[1,2,3,4,5], "col2":["a","b","c","d","e"]}))
                          ])
def test_get_missing_rows(df1, df2, expected):
    actual = get_missing_rows(df1, df2)
    assert np.array_equal(actual.values, expected.values)
     
     
if __name__ == "__main__":
    test_get_missing_rows()
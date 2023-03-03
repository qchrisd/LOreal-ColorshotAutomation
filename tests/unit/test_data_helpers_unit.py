
"""test_data_helpers.py: Unit tests for data_helpers.py"""

## Imports
import pytest
import pandas as pd
import numpy as np

from data_helpers import get_missing_rows, find_standard, mark_standards, extract_shade_name

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
     

@pytest.mark.parametrize("input,expected",
                         [
                             ("Shade5ASTD",True),
                             ("Gaiav2Shade5A",False),
                             ("ShadeSTDname",False),
                             ("shade5astd",True),
                             ("Shade5AsTd",True)
                         ])
def test_find_standard(input, expected):
    actual = find_standard(input)
    assert actual == expected


@pytest.mark.parametrize("input_dataframe,expected",
                         [
                             (pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"]}),
                              pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"],
                                            "STD":[True,False,False,True,True]}))
                         ])
def test_mark_standards(input_dataframe,expected):
    actual = mark_standards(input_dataframe)
    pd.testing.assert_frame_equal(actual, expected)
     

def test_extract_shade_name(input, expected):
    pass
     
     
if __name__ == "__main__":
    test_get_missing_rows()
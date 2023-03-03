
"""test_data_helpers.py: Unit tests for data_helpers.py"""

## Imports
import pytest
import pandas as pd
import numpy as np

from data_helpers import (get_missing_rows, 
                          find_standard, 
                          mark_standards, 
                          extract_shade_name, 
                          mark_shade_names,
                          get_groups)

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
     

@pytest.mark.parametrize("input,expected",
                         [
                             ("Shade5ASTD","Shade5A"),
                             ("Gaiav2Shade5A","Gaiav2Shade5A"),
                             ("ShadeSTDname","ShadeSTDname"),
                             ("shade5astd","shade5a"),
                             ("Shade5AsTd","Shade5A")
                         ])
def test_extract_shade_name(input, expected):
    actual = extract_shade_name(input)
    assert actual == expected


@pytest.mark.parametrize("input,expected",
                         [
                             (pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"]}),
                              pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"],
                                            "ShadeName":["Shade5A","Gaiav2Shade5A","ShadeSTDname","shade5a","Shade5A"]}))
                         ])
def test_mark_shade_names(input, expected):
    actual = mark_shade_names(input)
    assert np.array_equal(actual.values, expected.values)


@pytest.mark.parametrize("input,expected",
                         [
                             ({"Date":["20220502-120000","20220502-120010","20220502-120020","20220502-120030","20220505-120030","20220505-120050"],
                               "Name":["ShadeName01","ShadeName01STD","ShadeName01","ShadeName01STD","ShadeName02","ShadeName02STD"],
                               "Nuance":["5A","5A","5A","5A","6A","6A"],
                               "Fiber":["BN","BN","BP","BP","BP","BP"],
                               "ShadeName":["ShadeName01","ShadeName01","ShadeName01","ShadeName01""ShadeName02","ShadeName02"]},
                              {"Date":[pd.to_datetime(20220502, format="%Y%m%d"),pd.to_datetime(20220502, format="%Y%m%d"),pd.to_datetime(20220505, format="%Y%m%d")],
                               "ShadeName":["ShadeName01","ShadeName01","ShadeName02"],
                               "Fiber":["BN","BP","BP"]}
                              )
                         ])
def test_get_groups(input, expected):
    actual = get_groups(input)
    np.array_equal(actual.values, expected.values)

     
if __name__ == "__main__":
    test_get_missing_rows()
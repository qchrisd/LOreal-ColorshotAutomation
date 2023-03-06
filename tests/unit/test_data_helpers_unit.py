
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
                          get_groups,
                          filter_for_group)

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
                             (pd.DataFrame({"Date":["20220502-120000","20220502-120010","20220502-120020","20220502-120030","20220505-120030","20220505-120050"],
                                            "Name":["ShadeName01","ShadeName01STD","ShadeName01","ShadeName01STD","ShadeName02","ShadeName02STD"],
                                            "Nuance":["5A","5A","5A","5A","6A","6A"],
                                            "Fiber":["BN","BN","BP","BP","BP","BP"],
                                            "ShadeName":["ShadeName01","ShadeName01","ShadeName01","ShadeName01","ShadeName02","ShadeName02"]}),
                              pd.DataFrame({"Date":[pd.to_datetime(20220502, format="%Y%m%d"),pd.to_datetime(20220502, format="%Y%m%d"),pd.to_datetime(20220505, format="%Y%m%d")],
                                            "ShadeName":["ShadeName01","ShadeName01","ShadeName02"],
                                            "Fiber":["BN","BP","BP"]})
                              )
                         ])
def test_get_groups(input, expected):
    input["Date"] = pd.to_datetime(input["Date"],
                                   format="%Y%m%d-%H%M%S")
    actual = get_groups(input)
    pd.testing.assert_frame_equal(actual, expected)
    # assert np.array_equal(actual.values, expected.values)


@pytest.mark.parametrize("input_data,input_filter,expected",
                         [
                            (
                                pd.DataFrame({"Date":["20220502-120000","20220502-120010","20220502-120020","20220502-120030","20220505-120030","20220505-120050"],
                                              "Name":["ShadeName01","ShadeName01STD","ShadeName01","ShadeName01STD","ShadeName02","ShadeName02STD"],
                                              "Nuance":["5A","5A","5A","5A","6A","6A"],
                                              "Fiber":["BN","BN","BP","BP","BP","BP"],
                                              "ShadeName":["ShadeName01","ShadeName01","ShadeName01","ShadeName01","ShadeName02","ShadeName02"]}
                                ),
                                [pd.to_datetime("20220502-120000", format="%Y%m%d-%H%M%S"), "ShadeName01", "BN"],
                                pd.DataFrame({"Date":["20220502-120000","20220502-120010"],
                                              "Name":["ShadeName01","ShadeName01STD",],
                                              "Nuance":["5A","5A"],
                                              "Fiber":["BN","BN"],
                                              "ShadeName":["ShadeName01","ShadeName01"]}
                                )
                            )
                         ])
def test_filter_for_group(input_data, input_filter, expected):
    group_date, shade_name, hair_type = input_filter
    input_data["Date"] = pd.to_datetime(input_data["Date"],
                                        format="%Y%m%d-%H%M%S")
    expected["Date"] = pd.to_datetime(expected["Date"],
                                      format="%Y%m%d-%H%M%S")
    actual = filter_for_group(input_data,
                              group_date,
                              shade_name,
                              hair_type)
    pd.testing.assert_frame_equal(actual, expected)

     
if __name__ == "__main__":
    test_get_missing_rows()
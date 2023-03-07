
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
                          filter_for_group,
                          calculate_colorimetry,
                          report_comparison)

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
                             ("ShadeSTDname",True),
                             ("shade5astd",False),
                             ("Shade5AsTd",False)
                         ])
def test_find_standard(input, expected):
    actual = find_standard(input)
    assert actual == expected


@pytest.mark.parametrize("input_dataframe,expected",
                         [
                             (pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"]}),
                              pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"],
                                            "STD":[True,False,True,False,False]}))
                         ])
def test_mark_standards(input_dataframe,expected):
    actual = mark_standards(input_dataframe)
    pd.testing.assert_frame_equal(actual, expected)
     

@pytest.mark.parametrize("input,expected",
                         [
                             ("Shade5ASTD","Shade5A"),
                             ("Gaiav2Shade5A","Gaiav2Shade5A"),
                             ("ShadeSTDname","Shadename"),
                             ("shade5astd","shade5astd"),
                             ("Shade5AsTd","Shade5AsTd")
                         ])
def test_extract_shade_name(input, expected):
    actual = extract_shade_name(input)
    assert actual == expected


@pytest.mark.parametrize("input,expected",
                         [
                             (pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"]}),
                              pd.DataFrame({"Name":["Shade5ASTD","Gaiav2Shade5A","ShadeSTDname","shade5astd","Shade5AsTd"],
                                            "ShadeName":["Shade5A","Gaiav2Shade5A","Shadename","shade5astd","Shade5AsTd"]}))
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



@pytest.mark.parametrize("input_std,input_comparison,expected",
                         [
                             (
                                 pd.DataFrame({"L*":[28.500],
                                               "a*":[8.391],
                                               "b*":[11.176],
                                               "C":[13.976],
                                               "h°":[43.445]}),
                                 pd.DataFrame({"L*":[22.433],
                                               "a*":[9.626],
                                               "b*":[14.223],
                                               "C":[17.174],
                                               "h°":[46.416]}),
                                 {"delta_E2000":4.895,
                                  "delta_L":-6.067,
                                  "delta_a":1.235,
                                  "delta_b":3.047,
                                  "delta_C":3.383,
                                  "delta_h":2.972}
                             ),
                             (
                                 pd.DataFrame({"L*":[61.43],
                                               "a*":[2.25],
                                               "b*":[-4.96],
                                               "C":[5.447],
                                               "h°":[304.173]}),
                                 pd.DataFrame({"L*":[61.29],
                                               "a*":[3.72],
                                               "b*":[-5.39],
                                               "C":[6.549],
                                               "h°":[315.928]}),
                                 {"delta_E2000":1.871,
                                  "delta_L":-0.1400,
                                  "delta_a":1.47,
                                  "delta_b":-0.43,
                                  "delta_C":1.754,
                                  "delta_h":11.755}
                             ),
                             (
                                 pd.DataFrame({"L*":[5.296],
                                               "a*":[4.492],
                                               "b*":[-6.538],
                                               "C":[0],
                                               "h°":[0]}),
                                 pd.DataFrame({"L*":[6.704],
                                               "a*":[5.902],
                                               "b*":[-10.737],
                                               "C":[0],
                                               "h°":[0]}),
                                 {"delta_E2000":3.29,
                                  "delta_L":1.408,
                                  "delta_a":1.410,
                                  "delta_b":-4.199,
                                  "delta_C":4.517,
                                  "delta_h":-6.349}
                             )                         ]
                        )
def test_calculate_colorimetry(input_std, input_comparison, expected):
    delta_E2000, delta_L, delta_a, delta_b, delta_C, delta_h = calculate_colorimetry(input_std,input_comparison)
    assert delta_E2000 == expected["delta_E2000"]
    assert delta_L == expected["delta_L"]
    assert delta_a == expected["delta_a"]
    assert delta_b == expected["delta_b"]
    assert delta_C == expected["delta_C"]
    assert delta_h == expected["delta_h"]


@pytest.mark.parametrize("input_std,input_comparison,expected",
                         [
                             (
                                 
                             )
                         ])
def test_report_comparison(input_std, input_comparison, expected):
    actual = report_comparison(input_std, input_comparison)
    pd.testing.assert_frame_equal(actual, expected)


if __name__ == "__main__":
    test_get_missing_rows()
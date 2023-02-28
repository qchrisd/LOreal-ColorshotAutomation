

from data_helpers import get_filepaths


def test_get_filepaths_integration():
    expected = ["G:\Colorshot-MS\Test File 1.xlsx",
                "G:\Colorshot-MS\Test File 2.xlsx"]
    actual = get_filepaths("./tests/integration_files/test_filepaths.txt")
    assert actual == expected
    
    
if __name__ == "__main__":
    test_get_filepaths_integration()
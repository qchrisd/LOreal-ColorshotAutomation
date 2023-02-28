
"""data_helpers.py: Contains helpful methods for acquiring and manipulating data files and data structures."""

## Imports


def get_filepaths(text_file):
    with open(text_file) as file:
        lines = file.read().splitlines()
        
    return lines
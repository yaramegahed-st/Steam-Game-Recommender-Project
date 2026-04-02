"""
CSC111 Project 2 UI File Reading Helpers

This file contains helper functions used by the UI for reading dataset files
and normalizing game titles before matching them against the Steam dataset.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed, Levi Pan, Haoxuan Shen, Laien Zou.
"""

import csv
from pathlib import Path

APP_DIR = Path(__file__).resolve().parent


def read_file(filename: str) -> list[str]:
    """Return a list of cleaned game names from the given file."""
    lst_file = []

    file_path = APP_DIR / filename

    with open(file_path, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)
        for row in data:
            game_name = clean_up_line(row[1])
            lst_file.append(game_name)

    return lst_file


def clean_up_line(line: str) -> str:
    """Return a lowercase alphabetic-only version of line with spaces removed."""
    clean_line = ""

    line = line.lower()
    line_lst = line.split()

    for word in line_lst:
        clean_word = ""
        for char in word:
            if char.isalpha():
                clean_word += char
        clean_line += clean_word

    return clean_line


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod()

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['csv', 'pathlib'],
        'allowed-io': ['read_file']
    })

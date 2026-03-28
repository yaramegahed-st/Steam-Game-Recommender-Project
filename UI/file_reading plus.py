import csv
from pathlib import Path

UI_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = UI_DIR.parent

def read_file(filename: str) -> list:
    """Return a list of a cleaned version of the game names in the file"""
    lst_file = []

    file_path = PROJECT_ROOT / filename

    with open(file_path, encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)
        data = list(reader)
        for row in data:
            game_name = clean_up_line(row[1])
            lst_file.append(game_name)

    return lst_file



def clean_up_line(line: str) -> str:
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

import csv

def read_file(filename: str) -> list:
    """Return a list of a cleaned version of the game names in the file"""
    lst_file = []

    with open(filename) as file:
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


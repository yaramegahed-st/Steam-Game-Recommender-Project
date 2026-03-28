"""
CSC111 Project 2 GameUserGrpah Class

This file is aim to create the GameUserGraph class for project 2

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations
import csv
import random
from typing import Any
from vertex import _Vertex
import game
import user


class GameUserGraph:
    """A graph used to represent game and user in the dataset..

    Private Instance Attributes:
         - _vertices:A collection of the vertices contained in this graph. A map of items to _Vertex object.
         - _games: A dictionary that contains all the game information in the csv file.
         - _users: A dictionarty contains all user information and comments in csv file.
    """

    _vertices: dict[Any, _Vertex]
    _games: dict[int, game.Game]
    _users: dict[Any, user.User]

    def __init__(self, games: dict[int, game.Game], users: dict[Any, user.User]) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self._games = games
        self._users = users

    def get_game(self, game_id: int) -> game.Game:
        """Return the Game object with the given game_id

        Precondition:
            - game_id in self._games
        """
        return self._games[game_id ]

    def get_all_vertices(self, kind: str = '') -> set:
        """Return a set of all vertex items in this graph.

        If kind != '', only return the items of vertices whose item_type is kind.

        Preconditions:
            - kind in {'', 'game', 'user'}
        """
        if kind == '':
            return set(self._vertices.keys())
        else:
            return {item for item in self._vertices
                    if self._vertices[item].item_type == kind}

    def get_neighbours(self, item: Any) -> set:
        """Return a set of the neighbours of the given vertex item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item not in self._vertices:
            raise ValueError

        return {vertex.item for vertex in self._vertices[item].neighbours}

    def add_vertex(self, item: Any, kind: str) -> None:
        """Add a vertex with the given item to this graph.

        The new vertex is not adjacent to any other vertices.

        Preconditions:
            - item not in self._vertices
        """
        if item not in self._vertices:
            self._vertices[item] = _Vertex(item, kind)

    def add_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between the two vertices with the given items in this graph.

        Raise a ValueError if item1 or item2 do not appear as vertices in this graph.

        Preconditions:
            - item1 != item2
        """
        if item1 in self._vertices and item2 in self._vertices:
            v1 = self._vertices[item1]
            v2 = self._vertices[item2]

            v1.neighbours.add(v2)
            v2.neighbours.add(v1)
        else:
            raise ValueError

    def add_game_edge(self, item1: Any, item2: Any) -> None:
        """Adding edge between two games vertices if they are similar.

        See more how two games can be similar in Vertex file

        Preconditions:
            - self._vertices[item1].item_type == "game"
            - self._vertices[item2].item_type == "game"
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        if v1.get_similarity(v2, self._games):
            self.add_edge(item1, item2)

    def filter_top_games_with_genre(self, genres: list[str], low_price: int,
                                    high_price: int) -> tuple[list[str], list[int]]:
        """Return a list of strings that contains the 10 tops game that are recommended,
         and the list of app_id corresponding to the games.

        The genres is the list of string of genre that contains the game preferences that the user input, and
        low_price and high_price is the price range of the recommended games.

        The first return list contains 10 games' names that are highly recommended by the algorithm of
        similarity score,and it is sorted in descending order by the similarity score.
        The second return list is the 10 app_id for the games. It should correspond to the first game name list.

        The function would first select all the games from self._games where their genre is in the list of input
        genres. Then it would randomly choose a game from the list that has Game object neighbours and use
        recommended_ten_top_games to generate the list.

        Precondition:
            - single_genre in game.GENRE
            - 0 <= low_price < high_price

        >>> games = load_game_data('data/medium_game_sample_300.csv')
        >>> users = load_user_data ('data/medium_user_sample_50.csv')
        >>> g = load_game_user_graph(games, users)
        >>> names, ids = g.filter_top_games_with_genre(['Action'], 5, 20)
        >>> len(names) <= 10
        True
        >>> len(names) == len(ids)
        True
        >>> all(game_id in games for game_id in ids)
        True
        >>> all(0 <= games[i].get_price() <= 20 for i in ids)
        True
        """
        filtered_games = []

        for game_id, game_obj in self._games.items():
            if any(genre in genres for genre in game_obj.get_game_genre()):
                filtered_games.append(game_id)

        while filtered_games:
            chosen_game_id = random.choice(filtered_games)
            rec_names, rec_ids = self.recommended_ten_top_games(chosen_game_id, low_price, high_price)

            if rec_names:
                return rec_names, rec_ids

            filtered_games.remove(chosen_game_id)

        return [], []

    def recommended_ten_top_games(self, item: Any, low_price: int | None,
                                  high_price: int | None) -> tuple[list[str], list[int]]:
        """Return a list of strings that contains the 10 tops game that are recommended,
         and the list of app_id corresponding to the games with the given app_id and the price range of a certain game.

        The first return list contains 10 games' names that are highly recommended by the algorithm of similarity score,
        and it is sorted in descending order by the similarity score.
        The second return list is the 10 app_id for the games. It should correspond to the first game name list.

        If the game does not contain 10 similar games that fit the requirments,
        then return the list with all the similar games sorting by similarity score.

        If the similar game's price is not between low_price and high_price, then this game will not
        be considered in the recommended list. If low_price and high_price are all None, select all the games that in
        self._vertices[item]. Else if only one of them is None, select the game that game price is smaller than
        high-price or greater than low_price.

         Precondition:
            - item in self._vertices.keys()
            - self._vertices[item].item_type == "game"
            - 0 <= low_price < high_price

        # Case 1: No price filter
        >>> games = load_game_data('data/medium_game_sample_300.csv')
        >>> users = load_user_data('data/medium_user_sample_50.csv')
        >>> g = load_game_user_graph(games, users)
        >>> sample_game_id = next(iter(games))
        >>> rec_names, rec_ids = g.recommended_ten_top_games(sample_game_id, None, None)
        >>> len(rec_names)
        5
        >>> len(rec_ids)
        5
        >>> rec_names[0]
        'Resident Evil / biohazard HD REMASTER'
        >>> rec_names[-1]
        'Squishy the Suicidal Pig'
        >>> rec_ids[0]
        304240
        >>> rec_ids[-1]
        318430

        # Case 2: Price range filter
        >>> rec_names2, rec_ids2 = g.recommended_ten_top_games(sample_game_id, 5, 20)
        >>> len(rec_names2) <= len(rec_names)
        True
        >>> len(rec_names) == len(rec_ids)
        True

        # Case 3: Only low price
        >>> rec_names3, rec_ids3 = g.recommended_ten_top_games(sample_game_id, 10, None)
        >>> all(games[i].get_price() >= 10 for i in rec_ids3)
        True

        # Case 4: Only high price
        >>> rec_names4, rec_ids4 = g.recommended_ten_top_games(sample_game_id, None, 15)
        >>> all(games[i].get_price() <= 15 for i in rec_ids4)
        True
        """
        target_vertex = self._vertices[item]

        scores = []

        for neighbour in target_vertex.neighbours:
            if neighbour.item_type == 'game':
                game_id = neighbour.item
                price = self._games[game_id].get_price()

                if low_price is None and high_price is None:
                    include_game = True
                elif low_price is None:
                    include_game = price <= high_price
                elif high_price is None:
                    include_game = price >= low_price
                else:
                    include_game = low_price <= price <= high_price

                if include_game and self._games[game_id].passes_recommendation_restrictions():
                    score = target_vertex.similarity_score(neighbour, self._games)
                    scores.append((score, game_id))

        # Sort by descending similarity score, then by app_id for tie-breaking
        scores.sort(key=lambda x: (-x[0], x[1]))
        top_10 = scores[:10]

        names = []
        ids = []

        for _, game_id in top_10:
            names.append(self._games[game_id].get_game_name())
            ids.append(game_id)

        return names, ids


def _parse_platform(text: str) -> list[str]:
    """Return a list of strings that represent the platforms of a game

    This is a helper function of load_game_data
    """
    result = []
    for p in text.split('|'):
        p = p.strip().lower()
        if p == 'windows':
            result.append('Window')
        elif p == 'mac':
            result.append('Mac')
        elif p == 'linux':
            result.append('Linux')
    return result


def _parse_tags(text: str) -> set[str]:
    """Return a set of tags correspond to the game.

    Text is read from csv file

    This is a helper function of load_game_data
    """
    return {tag.strip() for tag in text.split('|')}


def _to_int_or_none(value: str) -> int | None:
    """Return the value into integer

    Value is the text reading from csv file

    This is a helper function of load_game_data
    """
    if value and value.lower() != 'nan':
        return int(float(value))
    return None


def _create_statistics(row: dict[str, str]) -> game.Statistics:
    """Return a Statistics object created from one CSV row.

    This is a helper function of load_game_data.
    """
    return game.Statistics(
        row['review_score_description'],
        _to_int_or_none(row['metacritic_score']),
        _to_int_or_none(row['num_positive_review']),
        _to_int_or_none(row['num_negative_review']),
        _to_int_or_none(row['recommendations'])
    )


def load_game_data(game_file: str) -> dict[Any, game.Game]:
    """Return a dictionary that contains all game information in the dataset.

    The key is the app_id of the game, and value is the Game object of the game

    Preconditions:
        - game_file is the path to a CSV file corresponding to the steam game data
          format described on the report.
    """
    data = {}

    with open(game_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            app_id = int(row['app_id'])
            genre = [g.strip() for g in row['game_genre'].split('|')]
            price = float(row['price'])
            platform = _parse_platform(row['platform'])
            tags = _parse_tags(row['tags'])
            summary = row['summary']
            stat = _create_statistics(row)

            one_game = game.Game(app_id, row['name'], genre, price, platform, tags, summary, stat)
            data[app_id] = one_game

    return data


def load_user_data(user_file: str) -> dict[Any, user.User]:
    """Return a dictionary that contains all user information in the dataset.

    The key is the user_id of the game, and value is the User object of the game

    Preconditions:
        - user_file is the path to a CSV file corresponding to the user data
          format described on the report.
    """
    data = {}

    with open(user_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_id = int(row['user_id'])
            game_id = int(row['app_id'])
            comment = row['comment']
            recommended = row['recommended'].strip().lower() in {'true', '1'}

            if user_id not in data:
                data[user_id] = user.User(user_id)

            data[user_id].add_review(game_id, comment, recommended)

    return data


def load_game_user_graph(game_data: dict[Any, game.Game], user_data: dict[Any, user.User]) -> GameUserGraph:
    """Return the GameUserGraph corresponding to the given dataset.

    >>> games = load_game_data('data/small_game_sample_30.csv')
    >>> users = load_user_data('data/small_user_sample_5.csv')
    >>> g = load_game_user_graph(games, users)
    >>> len(g.get_all_vertices(kind='game'))
    30
    >>> len(g.get_all_vertices(kind='user'))
    5
    >>> user_id = next(iter(users))
    >>> reviewed_games = users[user_id].get_reviewed_games()
    >>> all(game_id in g.get_neighbours(user_id) for game_id in reviewed_games)
    True
    >>> len(g.get_neighbours(user_id)) >= len(reviewed_games)
    True
    """

    graph = GameUserGraph(game_data, user_data)

    # add game vertices
    for game_id in game_data:
        graph.add_vertex(game_id, 'game')

    # add user vertices
    for user_id in user_data:
        graph.add_vertex(user_id, 'user')

    # connect user and game
    for user_id in user_data:
        current_user = user_data[user_id]

        for game_id in current_user.get_reviewed_games():
            if game_id in game_data:
                graph.add_edge(user_id, game_id)

        # connect similar games
    game_ids = list(game_data.keys())
    for i in range(len(game_ids)):
        for j in range(i + 1, len(game_ids)):
            g1 = game_ids[i]
            g2 = game_ids[j]

            game1 = game_data[g1]
            game2 = game_data[g2]

            # Only compare if they share tags
            if game1.get_tags().intersection(game2.get_tags()):
                graph.add_game_edge(g1, g2)

    return graph


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta
    
    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['csv', 'game', 'user', 'vertex', 'random'],
        'allowed-io': ['load_game_data', 'load_user_data'],
        'max-nested-blocks': 4
    })


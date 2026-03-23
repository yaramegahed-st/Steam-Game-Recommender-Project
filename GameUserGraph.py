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
from typing import Any
from Vertex import _Vertex
import Game
import User


class GameUserGraph:
    """A graph used to represent game and user in the dataset..

    Private Instance Attributes:
         - _vertices:A collection of the vertices contained in this graph. A map of items to _Vertex object.
         - _games: A dictionary that contains all the game information in the csv file.
         - _users: A dictionarty contains all user information and comments in csv file.
    """

    _vertices: dict[Any, _Vertex]
    _games: dict[int, Game.Game]
    _users: dict[Any, User.User]

    def __init__(self, games: dict[int, Game.Game], users: dict[Any, User.User]) -> None:
        """Initialize an empty graph (no vertices or edges)."""
        self._vertices = {}
        self._games = games
        self._users = users

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

    def recommended_ten_top_games(self, item: Any) -> tuple[list[str], list[int]]:
        """Return a list of strings that contains the 10 tops game that are recommended,
         and the list of app_id corresponding to the games.

        The first return list contains 10 games that are highly recommended by the algorithm of similarity score,
        and it is sorted in descending order by the similarity score.
        The second return list is the 10 app_id for the games. It should correspond to the first game name list.

         Precondition:
            - self._vertices[item].item_type == "game"
        """
        target_vertex = self._vertices[item]

        scores = []  # (score, game_id)

        # compute similarity with all other games
        for other_id in self._vertices:
            other_vertex = self._vertices[other_id]

            if other_id != item and other_vertex.item_type == 'game':
                score = target_vertex.similarity_score(other_vertex, self._games)
                scores.append((score, other_id))

        # sort using lambda (by score only)
        scores.sort(key=lambda x: x[0], reverse=True)

        # take top 10
        top_10 = scores[:10]

        # build result
        names = []
        ids = []

        for score, game_id in top_10:
            game = self._games[game_id]
            names.append(game.get_description())
            ids.append(game_id)

        return names, ids


def load_game_data(game_file: str) -> dict[Any, Game.Game]:
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
            # Basic fields
            app_id = int(row['app_id'])
            genre = row['game_genre']
            price = float(row['price'])

            # Platform
            platform = []
            for p in row['platform'].split('|'):
                p = p.strip().lower()

                if p == 'windows':
                    platform.append('Window')
                elif p == 'mac':
                    platform.append('Mac')
                elif p == 'linux':
                    platform.append('Linux')

            # Tags
            tags = set()
            for tag in row['tags'].split('|'):
                tags.add(tag.strip())

            # Summary
            summary = row['summary']

            # Statistics (handle possible nulls)
            description = row['review_score_description']

            if row['metacritic_score'] and row['metacritic_score'].lower() != 'nan':
                metacritic = int(row['metacritic_score'])
            else:
                metacritic = None

            if row['num_positive_review'] and row['num_positive_review'].lower() != 'nan':
                pos_review = int(row['num_positive_review'])
            else:
                pos_review = None

            if row['num_negative_review'] and row['num_negative_review'].lower() != 'nan':
                neg_review = int(row['num_negative_review'])
            else:
                neg_review = None

            if row['recommendations'] and row['recommendations'].lower() != 'nan':
                recommendation = int(row['recommendations'])
            else:
                recommendation = None

            # Create objects
            stats = Game.Statistics(description, metacritic, pos_review, neg_review, recommendation)

            game = Game.Game(app_id, genre, price, platform, tags, summary, stats)

            # Store
            data[app_id] = game

    return data


def load_user_data(user_file: str) -> dict[Any, User.User]:
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
            # user id
            user_id = int(row['user_id'])

            # game id
            game_id = int(row['app_id'])

            # comment
            if row['comment'] and row['comment'].lower() != 'nan':
                comment = row['comment']
            else:
                comment = None

            # recommended
            value = row['recommended']

            if value == 'True' or value == '1':
                recommended = True
            else:
                recommended = False

            # create User object
            user = User.User(user_id, game_id, comment, recommended)

            # store in dictionary
            data[user_id] = user

    return data


def load_game_user_graph(game_data: dict[Any, Game.Game], user_data: dict[Any, User.User]) -> GameUserGraph:
    """Return the GameUserGraph corresponding to the given dataset."""

    graph = GameUserGraph(game_data, user_data)

    # add game vertices
    for game_id in game_data:
        graph.add_vertex(game_id, 'game')

    # add user vertices
    for user_id in user_data:
        graph.add_vertex(user_id, 'user')

    # connect user and game
    for user in user_data.values():
        user_id = user.get_user_id()
        game_id = user.get_game_id_comment()

        # connect user to the game they reviewed
        if game_id in game_data:
            graph.add_edge(user_id, game_id)

    # connect game to game (similarity)
    game_ids = list(game_data.keys())

    for i in range(len(game_ids)):
        for j in range(i + 1, len(game_ids)):
            g1 = game_ids[i]
            g2 = game_ids[j]

            graph.add_game_edge(g1, g2)

    return graph

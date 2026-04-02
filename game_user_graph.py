"""
CSC111 Project 2 GameUserGraph Class

This file contains the GameUserGraph class and helper functions used in project 2.

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
from vertex import _Vertex
import game
import user


class GameUserGraph:
    """A graph used to represent games and users in the dataset.

    Private Instance Attributes:
         - _vertices: A collection of the vertices contained in this graph. It maps items to _Vertex objects.
         - _games: A dictionary that contains all the game information in the csv file.
         - _users: A dictionary that contains all user information and comments in the csv file.
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
        """Return the Game object with the given game_id.

        Precondition:
            - game_id in self._games
        """
        return self._games[game_id]

    def get_games(self) -> dict[int, game.Game]:
        """Return the dictionary of all games."""
        return self._games

    def get_similarity_score(self, game_id1: int, game_id2: int) -> float:
        """Return the similarity score between the two given games.

        Preconditions:
            - game_id1 in self._vertices
            - game_id2 in self._vertices
            - self._vertices[game_id1].item_type == 'game'
            - self._vertices[game_id2].item_type == 'game'
        """
        v1 = self._vertices[game_id1]
        v2 = self._vertices[game_id2]
        return v1.similarity_score(v2, self._games)

    def get_comments_for_game(self, game_id: int) -> list[str]:
        """Return the list of user comments attached to the given game.

        Preconditions:
            - game_id in self._vertices
            - self._vertices[game_id].item_type == 'game'
        """
        comments = []
        for neighbour in self._vertices[game_id].neighbours:
            if neighbour.item_type == 'user':
                current_user = self._users[neighbour.item]
                user_comments = current_user.get_comments()
                if game_id in user_comments and user_comments[game_id]:
                    comments.append(user_comments[game_id])
        return comments

    def get_all_vertices(self, kind: str = '') -> set[Any]:
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

    def get_neighbours(self, item: Any) -> set[Any]:
        """Return a set of the neighbours of the given vertex item.

        Raise a ValueError if item does not appear as a vertex in this graph.
        """
        if item not in self._vertices:
            raise ValueError(f'{item} is not a vertex in this graph.')

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
            raise ValueError(f'{item1} or {item2} is not a vertex in this graph.')

    def add_game_edge(self, item1: Any, item2: Any) -> None:
        """Add an edge between two game vertices if they are similar.

        See more about how two games can be similar in the Vertex file.

        Preconditions:
            - item1 in self._vertices
            - item2 in self._vertices
            - self._vertices[item1].item_type == "game"
            - self._vertices[item2].item_type == "game"
        """
        v1 = self._vertices[item1]
        v2 = self._vertices[item2]

        if v1.get_similarity(v2, self._games):
            self.add_edge(item1, item2)

    def filter_top_games_with_genre(self, genres: list[str], low_price: int | None,
                                    high_price: int | None) -> tuple[list[str], list[int]]:
        """Return up to 10 recommended games matching the given genres and price range.

        The genres parameter contains the user's selected genres, and low_price and high_price
        give the allowed price range for recommended games.

        The first returned list contains game names, sorted in descending order by similarity.
        The second returned list contains the corresponding app_ids.

        This function first finds games whose genres match the user's preferences. It then checks
        those candidate games in deterministic priority order until it finds one that produces a
        non-empty recommendation list through recommended_ten_top_games.

        Precondition:
            - all(g in game.GENRE for g in genres)
            - (low_price is None or low_price >= 0)
            - (high_price is None or high_price >= 0)
            - low_price is None or high_price is None or low_price < high_price

        >>> games = load_game_data('data/medium_game_sample_300.csv')
        >>> users = load_user_data('data/medium_user_sample_50.csv')
        >>> g = load_game_user_graph(games, users)
        Building game graph, please wait...
        Game graph built.
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
            matches_genre = False
            for genre in game_obj.get_game_genre():
                if genre in genres:
                    matches_genre = True

            if matches_genre:
                filtered_games.append(game_id)

        filtered_games.sort(key=self._genre_filter_sort_key, reverse=True)

        for chosen_game_id in filtered_games:
            rec_names, rec_ids = self.recommended_ten_top_games(chosen_game_id, low_price, high_price)

            if rec_names:
                return rec_names, rec_ids

        return [], []

    def _matches_price_range(self, one_game: game.Game, low_price: int | None,
                             high_price: int | None) -> bool:
        """Return whether one_game satisfies the given price range.

        When low_price is None, it means that the lower bound of the budget is 0, when high_price is None, it
        means the upper bound of the budget is 250.
        """
        price = one_game.get_price()

        if low_price is None and high_price is None:
            return True
        elif low_price is None:
            return price <= high_price
        elif high_price is None:
            return price >= low_price
        else:
            return low_price <= price <= high_price

    def _genre_filter_sort_key(self, game_id: int) -> tuple[float, int, int]:
        """Return the sort key used for deterministic genre-based fallback selection.

        Precondition:
            - game_id in self.vertices.keys()
        """
        one_game = self._games[game_id]

        positive_ratio = one_game.get_positive_ratio()
        if positive_ratio is None:
            positive_ratio_value = -1.0
        else:
            positive_ratio_value = positive_ratio

        num_positive = one_game.get_num_positive_review()
        num_negative = one_game.get_num_negative_review()
        if num_positive is None or num_negative is None:
            total_reviews = -1
        else:
            total_reviews = num_positive + num_negative

        return positive_ratio_value, total_reviews, -game_id

    def _collect_scored_games(self, item: Any, low_price: int | None,
                              high_price: int | None) -> list[tuple[float, int]]:
        """Return recommendation scores for game neighbours of the given starting game.

        Only adjacent game vertices are considered as recommendation candidates.
        This means the recommender uses the stored game-game similarity edges in
        the graph instead of comparing the starting game to every game in the dataset.

        When low_price is None, it means that the lower bound of the budget is 0, when high_price is None, it
        means the upper bound of the budget is 250.
        """
        target_vertex = self._vertices[item]
        scores = []

        for other_vertex in target_vertex.neighbours:
            if other_vertex.item_type != 'game':
                continue

            other_id = other_vertex.item
            looked_up_vertex = self._vertices[other_id]
            other_game = self._games[other_id]

            if self._matches_price_range(other_game, low_price, high_price) \
                    and other_game.is_recommendable():
                score = target_vertex.similarity_score(looked_up_vertex, self._games)
                scores.append((score, other_id))

        return scores

    def recommended_ten_top_games(self, item: Any, low_price: int | None,
                                  high_price: int | None) -> tuple[list[str], list[int]]:
        """Return up to 10 recommended games for the given starting game and price range.

        When low_price is None, it means that the lower bound of the budget is 0, when high_price is None, it
        means the upper bound of the budget is 250.

        The first returned list contains recommended game names, sorted in descending order by
        similarity score. The second returned list contains the corresponding app_ids.

        Only neighbouring game vertices connected by stored game-game similarity
        edges are considered. If there are fewer than 10 such games that satisfy
        the restrictions, return all matching games in descending order by
        similarity score.

        A candidate game is excluded if its price falls outside the requested range. If both
        bounds are None, then no price filter is applied.

        Preconditions:
            - item in self._vertices.keys()
            - self._vertices[item].item_type == "game"
            - (low_price is None or low_price >= 0)
            - (high_price is None or high_price >= 0)
            - low_price is None or high_price is None or low_price < high_price

        # Case 1: No price filter
        >>> games = load_game_data('data/medium_game_sample_300.csv')
        >>> users = load_user_data('data/medium_user_sample_50.csv')
        >>> g = load_game_user_graph(games, users)
        Building game graph, please wait...
        Game graph built.
        >>> sample_game_id = next(iter(games))
        >>> rec_names, rec_ids = g.recommended_ten_top_games(sample_game_id, None, None)
        >>> len(rec_names) <= 10
        True
        >>> len(rec_names) == len(rec_ids)
        True
        >>> all(game_id in games for game_id in rec_ids)
        True

        # Case 2: Price range filter
        >>> rec_names2, rec_ids2 = g.recommended_ten_top_games(sample_game_id, 5, 20)
        >>> len(rec_names2) <= len(rec_names)
        True
        >>> len(rec_names2) == len(rec_ids2)
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
        scores = self._collect_scored_games(item, low_price, high_price)

        scores.sort(key=self._score_sort_key)
        top_10 = scores[:10]

        names = []
        ids = []

        for _, game_id in top_10:
            names.append(self._games[game_id].get_game_name())
            ids.append(game_id)

        return names, ids

    def recommended_ten_top_games_with_genres(self, item: Any, genres: list[str], low_price: int | None,
                                              high_price: int | None) -> tuple[list[str], list[int]]:
        """Return up to 10 recommended games that also match at least one selected genre.

        This method filters candidate neighbour games by price, recommendability,
        and selected genres before taking the top 10 by similarity score.
        """
        scores = self._collect_scored_games(item, low_price, high_price)
        filtered_scores = []

        for score, game_id in scores:
            one_game = self._games[game_id]
            matches_genre = False

            for genre in one_game.get_game_genre():
                if genre in genres:
                    matches_genre = True

            if matches_genre:
                filtered_scores.append((score, game_id))

        filtered_scores.sort(key=self._score_sort_key)
        top_10 = filtered_scores[:10]

        names = []
        ids = []

        for _, game_id in top_10:
            names.append(self._games[game_id].get_game_name())
            ids.append(game_id)

        return names, ids

    @staticmethod
    def _score_sort_key(score_and_id: tuple[float, int]) -> tuple[float, int]:
        """Return the sort key for recommendation scores."""
        score = score_and_id[0]
        game_id = score_and_id[1]
        return -score, game_id


def _parse_platform(text: str) -> list[str]:
    """Return the list of platforms for one game.

    This is a helper function for load_game_data.
    """
    result = []
    for p in text.split('|'):
        p = p.strip().lower()
        if p == 'windows':
            result.append('Windows')
        elif p == 'mac':
            result.append('Mac')
        elif p == 'linux':
            result.append('Linux')
    return result


def _parse_tags(text: str) -> set[str]:
    """Return the set of tags for one game.

    Text is read from the csv file.
    """
    return {tag.strip() for tag in text.split('|')}


def _to_int_or_none(value: str) -> int | None:
    """Return value converted to an integer, or None if it is missing.

    This is a helper function for load_game_data.
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
    """Return a dictionary containing all game information in the dataset.

    The key is the app_id of the game, and the value is the corresponding Game object.

    Preconditions:
        - game_file is the path to a CSV file corresponding to the steam game data
          format described on the report.
    """
    data = {}

    with open(game_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)

        for row in reader:
            app_id = int(row['app_id'])
            genre = []
            for one_genre in row['game_genre'].split('|'):
                genre.append(one_genre.strip())
            price = float(row['price'])
            platform = _parse_platform(row['platform'])
            tags = _parse_tags(row['tags'])
            summary = row['summary']
            stat = _create_statistics(row)

            one_game = game.Game(app_id, row['name'], genre, price, platform, tags, summary, stat)
            data[app_id] = one_game

    return data


def load_user_data(user_file: str) -> dict[Any, user.User]:
    """Return a dictionary containing all user information in the dataset.

    The key is the user_id, and the value is the corresponding User object.

    Preconditions:
        - user_file is the path to a CSV file corresponding to the user data
          format described in the report.
    """
    data = {}

    with open(user_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)

        for row in reader:
            user_id = f"user_{int(row['user_id'])}"
            game_id = int(row['app_id'])
            comment = row['comment']
            recommended = row['recommended'].strip().lower() in {'true', '1'}

            if user_id not in data:
                data[user_id] = user.User(user_id)

            data[user_id].add_review(game_id, comment, recommended)

    return data


def load_game_user_graph(game_data: dict[Any, game.Game], user_data: dict[Any, user.User]) -> GameUserGraph:
    """Return the GameUserGraph corresponding to the given dataset.

    >>> games = load_game_data('data/medium_game_sample_300.csv')
    >>> users = load_user_data('data/medium_user_sample_50.csv')
    >>> g = load_game_user_graph(games, users)
    Building game graph, please wait...
    Game graph built.
    >>> len(g.get_all_vertices(kind='game')) == len(games)
    True
    >>> len(g.get_all_vertices(kind='user')) == len(users)
    True
    >>> user_id = next(iter(users))
    >>> reviewed_games = users[user_id].get_reviewed_games()
    >>> all(game_id in g.get_neighbours(user_id) for game_id in reviewed_games)
    True
    >>> len(g.get_neighbours(user_id)) == len(reviewed_games)
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
    print("Building game graph, please wait...")
    game_ids = list(game_data.keys())
    for i in range(len(game_ids)):
        for j in range(i + 1, len(game_ids)):
            graph.add_game_edge(game_ids[i], game_ids[j])
    print("Game graph built.")

    return graph


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['csv', 'game', 'user', 'vertex'],
        'allowed-io': ['load_game_data', 'load_user_data', 'load_game_user_graph'],
        'max-nested-blocks': 4
    })

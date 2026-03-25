"""
CSC111 Project 2 Vertex Class

This file is aim to create the Vertex class for project 2

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations
from typing import Any
import game


class _Vertex:
    """A vertex in the graph class, used to represent user or game object.

    Instance Attributes:
        - item: The data stored in this vertex, representing a game or user.
        - item_type: The type of this vertex: 'game' or 'user'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.item_type in {'game', 'user'}
    """
    item: Any
    item_type: str
    neighbours: set[_Vertex]

    def __init__(self, item: Any, item_type: str) -> None:
        """Initialize a new vertex with the given item and kind.
        The item should be either app_id of the game or the user_id, and item_type is either "game" or "user"

        This vertex is initialized with no neighbours.

        Preconditions:
            - item_type in {'user', 'game'}
        """
        self.item = item
        self.item_type = item_type
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)

    def similarity_score(self, other: _Vertex, dataset: dict[int, game.Game]) -> float:
        """Return the similarity score of two games vertrices. It will depend on tag_similarity and platform_match.

        Here is the algorithm of the calculation:
            genre_bonus = 1 if two games have the same game_genre, otherwise 0
            tag_similarity = the intersection between tags of self and other / the union betweem tags of self and other
            platform_match = 1 if two games share at least one platform, otherwise 0
            similarity_score = 0.8 * tag_similarity + 0.1 * platform_match + 0.1 * genre_bonus

        Preconditions:
            - self.item_type == "game"
            - other.item_type == "game"

        >>> stat1 = game.Statistics('Very Positive', 80, 100, 20, 50)
        >>> g1 = game.Game(1, 'Game one', 'Action', 10.0, ['Window'], {'Action', 'Adventure'}, 'game one', stat1)
        >>> stat2 = game.Statistics('Overwhelmingly Positive', 90, 200, 10, 80)
        >>> g2 = game.Game(2, 'Game Two', 'Action', 20.0, ['Window'], {'Action', 'RPG'}, 'game two', stat2)
        >>> game_data = {1: g1, 2: g2}
        >>> v1 = _Vertex(1, 'game')
        >>> v2 = _Vertex(2, 'game')
        >>> round(v1.similarity_score(v2, game_data), 2)
        0.47
        """
        # Retrieve the actual Game objects using the IDs stored in self.item
        game1 = dataset[self.item]
        game2 = dataset[other.item]

        return 0.8 * tag_score(game1, game2) + 0.1 * platform_score(game1, game2) + 0.1 * genre_score(game1, game2)

    def get_similarity(self, other: _Vertex, dataset: dict[int, game.Game]) -> bool:
        """Return whether the given two game vertices are similar judging by the similarity_score.

        Return True if similarity_score(self, _Vertex) >= 0.3, else return False.

        Preconditions:
            - self.item_type == "game"
            - other.item_type == "game"
        """
        return self.similarity_score(other, dataset) >= 0.35


def genre_score(g1: game.Game, g2: game.Game) -> float:
    """Return the genre score between two games, 1 if they have the same genre, 0 if not

    This is a helper function of similarity_score

    Preconditions:
        - self.item_type == "game"
        - other.item_type == "game"
    """
    return 1.0 if g1.get_game_genre() == g2.get_game_genre() else 0.0


def tag_score(g1: game.Game, g2: game.Game) -> float:
    """Return the tag score between two games,

    tag_similarity = the intersection between tags of self and other / the union betweem tags of self and other

    This is a helper function of similarity_score

    Preconditions:
        - self.item_type == "game"
        - other.item_type == "game"
    """
    tags1 = g1.get_tags()
    tags2 = g2.get_tags()
    union = tags1.union(tags2)
    if not union:
        tag_similarity = 0.0
    else:
        intersection = tags1.intersection(tags2)
        tag_similarity = len(intersection) / len(union)
    return tag_similarity


def platform_score(g1: game.Game, g2: game.Game) -> float:
    """Return the platform score between two games, 1 if they have common platform, 0 if not

    This is a helper function of similarity_score

    Preconditions:
        - self.item_type == "game"
        - other.item_type == "game"
    """
    platforms1 = set(g1.get_platform())
    platforms2 = set(g2.get_platform())
    if platforms1.intersection(platforms2):
        return 1.0
    else:
        return 0.0


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': ['game'],
        'max-nested-blocks': 4,
        'max-args': 6
    })

"""
CSC111 Project 2 Game Class

This file contains the Game and Statistics classes used in project 2.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations
from typing import Optional

DESCRIPTION = ["Overwhelmingly Positive", "Very Positive", "Mostly Positive", "Mixed", "Mostly Negative",
               "Overwhelmingly Negative", "Positive", "Negative"]
GENRE = ["Action", "Adventure", "Casual", "Indie", "Massively Multiplayer", "Racing", "RPG", "Simulation", "Sports",
         "Strategy", "Free to Play", "Early Access"]
PLATFORM = ["Mac", "Windows", "Linux"]


class Statistics:
    """Statistics data that represents detailed information about a game.

    Instance Attributes:
        - review_score_description: The overall review description for the game.
        - metacritic_score: A weighted average of professional critic reviews for the game, ranging from 0 to 100,
                            or None if the game does not contain metacritic score.
        - num_positive_review: Number of positive reviews of the game.
        - num_negative_review: Number of negative reviews of the game.
        - num_recommendation: Number of recommendations for the game.

    Representation Invariants:
        - metacritic_score is None or 0 <= metacritic_score <= 100
        - num_positive_review is None or num_positive_review >= 0
        - num_negative_review is None or num_negative_review >= 0
        - num_recommendation is None or num_recommendation >= 0

    """
    review_score_description: str
    metacritic_score: Optional[int]
    num_positive_review: Optional[int]
    num_negative_review: Optional[int]
    num_recommendation: Optional[int]

    def __init__(self, description: str, score: Optional[int], pos_review: Optional[int],
                 neg_review: Optional[int], recommendation: Optional[int]) -> None:
        """Initialize statistics with the data for a game.

        Preconditions:
            - description is not None
            - 0 <= score <= 100 or score is None
            - pos_review >= 0 or pos_review is None
            - neg_review >= 0 or neg_review is None
            - recommendation >= 0 or recommendation is None
        """

        self.review_score_description = description
        self.metacritic_score = score
        self.num_positive_review = pos_review
        self.num_negative_review = neg_review
        self.num_recommendation = recommendation


class Game:
    """A game in the Steam dataset.

    Instance Attributes:
        - app_id: A unique id that represents the game.
        - game_name: The English name of the game.
        - game_genre: The genre of the game.
        - price: The price of the game.
        - platform: The platforms the user can use to play the game.
        - tags: The tags of the game, which describe the topics or features related to it.
        - description: A summary of the game.
        - statistics: Statistics data that contains detailed information about the game.

    Representation Invariants:
        - self.app_id > 0
        - all(g in GENRE for g in self.game_genre)
        - self.price >= 0.0
        - all(p in PLATFORM for p in self.platform)

    """
    app_id: int
    game_name: str
    game_genre: list[str]
    price: float
    platform: list[str]
    tags: set[str]
    description: str
    statistics: Statistics

    def __init__(self, game_id: int, name: str, genre: list[str], price: float, platform: list[str],
                 tags: set[str], summary: str, stat: Statistics) -> None:
        """Initialize a new game with the given data.

        Preconditions:
            - all(g in GENRE for g in genre)
            - price >= 0.0
            - all(p in PLATFORM for p in platform)
        """
        self.app_id = game_id
        self.game_name = name
        self.game_genre = genre
        self.price = price
        self.platform = platform
        self.tags = tags
        self.description = summary
        self.statistics = stat

    def get_app_id(self) -> int:
        """Return the app_id for the given game."""
        return self.app_id

    def get_game_name(self) -> str:
        """Return the name of the game."""
        return self.game_name

    def get_game_genre(self) -> list[str]:
        """Return the overall genre for the game.

        Precondition:
            - all(g in GENRE for g in self.game_genre)
        """
        return self.game_genre

    def get_price(self) -> float:
        """Return the price of the game."""
        return self.price

    def get_platform(self) -> list[str]:
        """Return the platform that the game could play on.

        Precondition:
            - all(p in PLATFORM for p in self.platform)
        """
        return self.platform

    def get_tags(self) -> set[str]:
        """Return the set of tags related to the game."""
        return self.tags

    def get_description(self) -> str:
        """Return the overall description of the game.

        This should be the summary of the game.
        """
        return self.description

    def get_review_score_description(self) -> str:
        """Return the overall description for the game."""
        return self.statistics.review_score_description

    def get_metacritic_score(self) -> Optional[int]:
        """Return the metacritic score of the game."""
        return self.statistics.metacritic_score

    def get_num_positive_review(self) -> Optional[int]:
        """Return the number of positive reviews of the game."""
        return self.statistics.num_positive_review

    def get_num_negative_review(self) -> Optional[int]:
        """Return the number of negative reviews of the game."""
        return self.statistics.num_negative_review

    def get_num_recommendation(self) -> Optional[int]:
        """Return the number of user recommendations for the game."""
        return self.statistics.num_recommendation

    def get_positive_ratio(self) -> float | None:
        """Return the positive review ratio of this game.

        This method returns None when the game does not have enough review
        information to compute a ratio.

        Preconditions:
            - self.statistics is not None

        Return None if the game does not have enough data to compute the ratio.
        """
        pos = self.get_num_positive_review()
        neg = self.get_num_negative_review()

        if pos is None or neg is None:
            return None
        if pos + neg == 0:
            return None

        return pos / (pos + neg)

    def is_recommendable(self) -> bool:
        """Return whether this game satisfies the recommendation restrictions.

        This method returns False when the game does not have enough review
        information to be evaluated.

        Preconditions:
            - self.statistics is not None

        A game can be recommended only if:
            - its positive ratio is greater than 0.70
            - it has more than 500 total reviews
        """
        ratio = self.get_positive_ratio()
        pos = self.get_num_positive_review()
        neg = self.get_num_negative_review()

        return (
            ratio is not None
            and ratio > 0.70
            and pos is not None
            and neg is not None
            and (pos + neg) > 500
        )


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod()

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['R1705', 'E9998', 'E9999', 'static_type_checker'],
        'extra-imports': ['typing'],
        'allowed-io': []
    })

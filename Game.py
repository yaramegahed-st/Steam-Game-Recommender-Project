"""
CSC111 Project 2 Game Class

This file is aim to create the Game and Statistics class for project 2

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""
from typing import Optional

DESCRIPTION = ["Overwhelmingly Positive", "Very Positive", "Mostly Positive", "Mixed", "Mostly Negative",
               "Overwhelmingly Negative", "Positive", "Negative"]
GENRE = ["Action", "Adventure", "Casual", "Indie", "Massively Multiplayer", "Racing", "RPG", "Simulation", "Sports",
         "Strategy", "Free to Play", "Early Access"]
PLATFORM = ["Mac", "Window", "Linux"]


class Statistics:
    """ Statistics data that represent the detail informationn of the certain game.

    Instance Attributes:
        - review_score_description: The overall description for the game, this attribute is mostly in the DESCRIPTION,
                                    if there are too less review for the game, then this is game is not be considered.
        - metacritic_score: A weighted average of professional critic reviews video games, ranging from 0 to 100,
                            or None if the game does not contain metacritic score.
        - num_positive_review: Number of positive reviews of the game.
        - num_negative_review: Number of positive reviews of the game.
        - num_recommednation: Number of recommednation for the game.

    Representation Invariants:
        - 0 <= metacritic_score <= 100
        - num_positive_review >= 0
        - num_negative_review >= 0
        - num_recommednation >= 0

    """
    review_score_description: str
    metacritic_score: Optional[int]
    num_positive_review: Optional[int]
    num_negative_review: Optional[int]
    num_recommendation: Optional[int]

    def __init__(self, description: str, score: Optional[int], pos_review: Optional[int],
                 neg_review: Optional[int], recommendation: Optional[int]) -> None:
        """Initialize statistic with the data of a game.

        Preconditions:
            - self.review_score_description is not None
            - 0 <= metacritic_score <= 100 or metacritic_score is None
            - num_positive_review >=0 or num_positive_review is None
            - num_negative_review >= 0 or num_negative_review is None
            - num_recommendation >= 0 or num_recommendation is None
        """

        self.review_score_description = description
        self.metacritic_score = score
        self.num_positive_review = pos_review
        self.num_negative_review = neg_review
        self.num_recommendation = recommendation


class Game:
    """A game in Steam Dataset.

    Instance Attributes:
        - app_id: An unique id that represent each game.
        - game_genre: The genre of the game.
        - price: The price of the game.
        - platform: The platform that user can use to play the game, it should be in the subset of the PLATFORM.
        - tags: The tags of the game which represent what types of topic that the game related to.
        - description: Summary for the game
        - statistics: Statistics data that contains detailed information about the game, see more in the Statistics
                      class.

    Representation Invariants:
        - self.app_id > 0
        - self.game_genre in GENRE
        - self.price >= 0.0
        - all(p in PLATFORM for p in self.platform)

    """
    app_id: int
    game_genre: str
    price: float
    platform: list[str]
    tags: set[str]
    description: str
    statistics: Statistics

    def __init__(self, game_id: int, genre: str, price: float, platform: list[str], tags: set[str],
                 summary: str, stat: Statistics) -> None:
        """Initialize a new game with given data

        Preconditions:
            - game_genre in GENRE
            - price >= 0.0
            - platform in PLATFORM
        """
        self.app_id = game_id
        self.game_genre = genre
        self.price = price
        self.platform = platform
        self.tags = tags
        self.description = summary
        self.statistics = stat

    def get_app_id(self) -> int:
        """Return the app_id for the given game."""
        return self.app_id

    def get_game_genre(self) -> str:
        """Return the overall genre for the game.

        Precondition:
            -self.game_genre in GENRE
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
        """Return a list of tags related to the game."""
        return self.tags

    def get_description(self) -> str:
        """Return the overall description of the game.

        This should be the summary of the game.
        """
        return self.description

    def get_review_score_description(self) -> str:
        """Return the overall description for the game."""
        return self.statistics.review_score_description

    def get_metacritic_score(self) -> int:
        """Return the metacritic score of the game."""
        return self.statistics.metacritic_score

    def get_num_positive_review(self) -> int:
        """Return the number of positive reviews of the game."""
        return self.statistics.num_positive_review

    def get_num_negative_review(self) -> int:
        """Return the number of negative reviews of the game."""
        return self.statistics.num_negative_review

    def get_num_recommendation(self) -> int:
        """Returh the number of users recommendation of the game."""
        return self.statistics.num_recommendation

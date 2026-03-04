"""
CSC111 Project 2 Game Class
This file is aim to create the Game and Statistics class for project 2
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
        - metacritic_score: A weighted average of professional critic reviews video games, ranging from 0 to 100.
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
    metacritic_score: int
    num_positive_review: int
    num_negative_review: int
    num_recommendation: int


class Game:
    """A game in Steam Dataset.

    Instance Attributes:
        - app_id: An unique id that represent each game.
        - game_genre: The genre of the game.
        - price: The price of the game.
        - Platform: The platform that user can use to play the game, it should be in the subset of the PLATFORM.
        - tags: The tags of the game which represent what types of topic that the game related to.
        - statistics: Statistics data that contains detailed information about the game, see more in the Statistics
                      class.

    Representation Invariants:
        - app_id > 0
        - game_genre in GENRE
        - price > 0.0
        - platform in PLATFORM

    """
    app_id: int
    game_genre: str
    price: float
    genre: str
    platform: list[str]
    tags: list[str]
    statistics: Optional[Statistics]

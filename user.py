"""
CSC111 Project 2 User Class
This file is aim to create the User class for project 2

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""
from typing import Optional


class User:
    """ User class that represent the user_id and text of commend.

    Instance Attributes:
        - user_id: The id for each user.
        - comment: A dictionary that represent comments that the user made to games. The key is the app_id of the game
                   that the user comment on, and value is the comment content.
        - game_recommended: A dictionart of whether the user recommend a certain game, True for yes and False for no.
                            The key is the app_id of the game, and value is the bool of recommended.

    Representation Invariants:
        - self.user_id > 0
    """
    _user_id: int
    _comments: dict[int, str]
    _recommended: dict[int, bool]

    def __init__(self, user_id: int) -> None:
        """Initialize the user with given data

        Preconditions:
            - self.user_id > 0
        """
        self._user_id = user_id
        self._comments = {}
        self._recommended = {}

    def get_user_id(self) -> int:
        """Return the user_id of the user."""
        return self._user_id

    def add_review(self, game_id: int, comment: str, recommended: bool) -> None:
        """Mutating the review dictionarty of the user with the given game_id, comment and recommended value of the game

        Precondition:
            - self.game_id is in the game dataset of the graph
        """
        self._comments[game_id] = comment
        self._recommended[game_id] = recommended

    def get_comments(self) -> dict[int, str]:
        """Return all the comments the user made on the games."""
        return self._comments

    def get_recommended_games(self) -> list[int]:
        """Return the list of app_id that the user recommended the game"""
        return [gid for gid, rec in self._recommended.items() if rec]

    def get_reviewed_games(self) -> list[int]:
        """Return the app_id that the user reviews"""
        return list(self._comments.keys())

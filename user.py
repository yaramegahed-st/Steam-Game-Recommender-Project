"""
CSC111 Project 2 User Class

This file contains the User class used in project 2.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations


class User:
    """A user in the review dataset.

    Instance Attributes:
        - _user_id: The id for each user.
        - _comments: A dictionary that stores comments the user made on games. The key is the app_id of the game
                     the user commented on, and the value is the comment content.
        - _recommended: A dictionary storing whether the user recommended a certain game. The key is the app_id
                        of the game, and the value is a boolean.

    Representation Invariants:
        - self._user_id != ''
    """
    _user_id: str
    _comments: dict[int, str]
    _recommended: dict[int, bool]

    def __init__(self, user_id: str) -> None:
        """Initialize the user with the given data.

        Preconditions:
            - user_id != ''
        """
        self._user_id = user_id
        self._comments = {}
        self._recommended = {}

    def get_user_id(self) -> str:
        """Return the user_id of the user."""
        return self._user_id

    def add_review(self, game_id: int, comment: str, recommended: bool) -> None:
        """Add review information for the given game to this user.

        Precondition:
            - game_id is in the game dataset of the graph
        """
        self._comments[game_id] = comment
        self._recommended[game_id] = recommended

    def get_comments(self) -> dict[int, str]:
        """Return all the comments the user made on the games."""
        return self._comments

    def get_recommended_games(self) -> list[int]:
        """Return the app_ids of the games this user recommended."""
        recommended_games = []

        for game_id in self._recommended:
            if self._recommended[game_id]:
                recommended_games.append(game_id)

        return recommended_games

    def get_reviewed_games(self) -> list[int]:
        """Return the app_ids of the games this user reviewed."""
        return list(self._comments.keys())


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod()

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': [],
        'allowed-io': []
    })

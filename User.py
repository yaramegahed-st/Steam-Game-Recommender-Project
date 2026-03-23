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
        - game_id_comment: The game id that the user comment on, the id should be in the game dataset
        - comment: Comment that the user written to a game
        - game_recommended: Whether the user recommend the game, True for yes and False for no

    Representation Invariants:
        - self.user_id > 0
        - self.game_id_comment > 0
    """
    user_id: int
    game_id_comment: int
    comment: Optional[str]
    game_recommended: bool

    def __init__(self, user_id: int, game_id: int, comment: Optional[str], recommended: bool) -> None:
        """Initialize the user with given data

        Preconditions:
            - self.user_id > 0
            - self.game_id_comment > 0
        """
        self.user_id = user_id
        self.game_id_comment = game_id
        self.comment = comment
        self.game_recommended = recommended

    def get_user_id(self) -> int:
        """Return the user_id of the user."""
        return self.user_id

    def get_game_id_comment(self) -> int:
        """Return the game_id_comment of the user"""
        return self.game_id_comment

    def get_comment(self) -> Optional[str]:
        """Return the comment given by the user, or None if user does not make any comment."""
        return self.comment

    def get_recommedned(self) -> Optional[bool]:
        """Return whether the user recommend the game, True for yes, False for no, or None if the user does not make any
           recommendation.
        """
        return self.game_recommended


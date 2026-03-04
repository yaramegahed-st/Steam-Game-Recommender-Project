"""
CSC111 Project 2 User Class
This file is aim to create the User class for project 2
"""
from typing import Optional


class User:
    """ User class that represent the user_id and text of commend.

    Instance Attributes:
        - user_id: The id for each user
        - comment: Comment that the user written to a game, or None if they do not make any comment.
        - game_recommended: Whether the user recommend the game, True for yes and False for no, or None if the user does
                            not make any recommendation.

    Representation Invariants:
        - user_id > 0
    """
    user_id: int
    comment: Optional[str]
    game_recommended: Optional[bool]

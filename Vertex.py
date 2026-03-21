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
import csv
from typing import Any


class _Vertex:
    """A vertex in the graph class, used to represent an user or a game object.

    Instance Attributes:
        - item: The data stored in this vertex, representing a game or user.
        - type: The type of this vertex: 'game' or 'user'.
        - neighbours: The vertices that are adjacent to this vertex.

    Representation Invariants:
        - self not in self.neighbours
        - all(self in u.neighbours for u in self.neighbours)
        - self.kind in {'game', 'user'}
    """
    item: Any
    item_type: str
    neighbour: set[_Vertex]

    def __init__(self, item: Any, item_type: str) -> None:
        """Initialize a new vertex with the given item and kind.

        This vertex is initialized with no neighbours.

        Preconditions:
            - item_type in {'user', 'book'}
        """
        self.item = item
        self.item_type = item_type
        self.neighbours = set()

    def degree(self) -> int:
        """Return the degree of this vertex."""
        return len(self.neighbours)



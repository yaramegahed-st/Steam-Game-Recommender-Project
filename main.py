"""
CSC111 Project 2 main.py
This file is aim to create the main file of the recommended system of Steam Game, providing list of commands that
help user to set up and open the Steam recommended system.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations

# Importing classes
import game
import user
import vertex
import game_user_graph
import VisualizationGraph

import csv

game_data = game_user_graph.load_game_data('data/cleaned_steam_data.csv')
user_data = game_user_graph.load_user_data('data/sample_user_data.csv')

graph = game_user_graph.load_game_user_graph(game_data, user_data)

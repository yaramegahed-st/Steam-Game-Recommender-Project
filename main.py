"""
CSC111 Project 2 main.py
This file launches the Steam game recommender system by loading the datasets,
building the graph, and opening the user interface.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed,Levi Pan,Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations

import game_user_graph
from ui3 import Interface


def run_program() -> None:
    """Load the datasets, build the graph, and launch the interface.

    Preconditions:
        - game dataset should be in the project root folder
        - user dataset should be in the project root folder
    """
    game_data = game_user_graph.load_game_data('data/filtered_steam_data_4000.csv')
    user_data = game_user_graph.load_user_data('data/sample_user_data_4000.csv')
    graph = game_user_graph.load_game_user_graph(game_data, user_data)

    Interface(graph, 'data/filtered_steam_data_4000.csv')


if __name__ == '__main__':
    run_program()

    # User Choice Method
    # for question 1, enter "Left 4 Dead 2"
    # for question 2, choose all the genres
    # for question 3, don't use the sliders
    # the results will be displayed for top ten games similar to "Left 4 Dead 2" ie have similar genres and price range
    # see the bar chart and path visualization
    # see the comments page
    # click on "Back to Home" to clear all previous answers and get new recommendations

    # Most Recommended Game Method
    # for question 1, enter "aaa" which is not a valid game name, hence it cannot be used in the filtering
    # for question 2, choose the genres you please
    # for question 3, use the sliders how you please
    # the recommendation system will pick a game with the highest number of recommendations that clears all the
    # filters and the results
    # will be displayed for top ten games similar to that random game ie have similar genres and price range
    # see the bar chart and path visualization
    # see the comments page

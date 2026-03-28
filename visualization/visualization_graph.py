"""
CSC111 Project 2 VisualizationGraph Class

This file is aim to create the VisualizationGraph class for project 2

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed, Levi Pan, Haoxuan Shen, Laien Zou.
"""


from __future__ import annotations

from typing import Any

import networkx as nx
import plotly.graph_objects as go

from game import Game
from game_user_graph import GameUserGraph


class VisualizationGraph:
    """A helper class for visualizing a local Steam game recommendation graph.

    Instance Attributes:
        - _source_graph: the original GameUserGraph
        - _center_game: the selected center game
        - _graph_nx: the local networkx graph for visualization
    Representation Invariants:
        - _center_game.get_app_id() in _source_graph.get_all_vertices('game')
        - all(node_id in _source_graph.get_all_vertices('game') for node_id in _graph_nx.nodes)
    """
    _source_graph: GameUserGraph
    _center_game: Game
    _graph_nx: nx.Graph

    def __init__(self, graph: GameUserGraph, center_game: Game) -> None:
        """Initialize a visualization graph centered at center_game.

        Preconditions:
        - center_game.get_app_id() in graph.get_all_vertices('game')
        """
        self._source_graph = graph
        self._center_game = center_game
        self._graph_nx = nx.Graph()
        self._build_local_graph()

    def _build_local_graph(self) -> None:
        """Build the local networkx graph for visualization.

        The local graph contains the center game and the top 10 recommended
        similar games returned by the source graph. Nodes are keyed by app_id,
        while displayed labels use game names.

        Preconditions:
            - self._center_game.get_app_id() in self._source_graph.get_all_vertices('game')
        """
        _, recommended_ids = self._source_graph.recommended_ten_top_games(
            self._center_game.get_app_id(), None, None
        )

        center_id = self._center_game.get_app_id()

        self._graph_nx.add_node(
            center_id,
            game_obj=self._center_game,
            is_center=True
        )

        for game_id in recommended_ids:
            recommended_game = self._source_graph.get_game(game_id)

            similarity = self._source_graph.get_similarity_score(center_id, game_id)

            layout_weight = 1.0 + 4.0 * similarity

            self._graph_nx.add_node(
                recommended_game.get_app_id(),
                game_obj=recommended_game,
                is_center=False,
                similarity_to_center=similarity
            )
            self._graph_nx.add_edge(
                center_id,
                recommended_game.get_app_id(),
                weight=layout_weight,
                similarity=similarity
            )

    def get_node_colour(self, one_game: Game, is_center: bool) -> str:
        """Return the display colour for one_game in this visualization graph.

        The center game is always coloured red. Other games are coloured according
        to their primary genre, defined as the first genre in the game's genre list.

        Preconditions:
            - one_game.get_game_genre() != []
        """
        genre_colours = {
            'Action': 'orange',
            'Adventure': 'green',
            'Casual': 'gold',
            'Indie': 'purple',
            'Massively Multiplayer': 'magenta',
            'Racing': 'gray',
            'RPG': 'blue',
            'Simulation': 'brown',
            'Sports': 'pink',
            'Strategy': 'teal',
            'Free to Play': 'black',
            'Early Access': 'darkred'
        }

        if is_center:
            return 'red'

        primary_genre = one_game.get_game_genre()[0]

        if primary_genre in genre_colours:
            return genre_colours[primary_genre]
        else:
            return 'lightblue'

    def build_node_texts(self) -> list[str]:
        """Return hover text for all nodes in this visualization graph.

        Each hover text contains the basic information of one game, including
        its name, price, genre, platform, and all comments associated with it.

        Preconditions:
            - all('game_obj' in self._graph_nx.nodes[node] for node in self._graph_nx.nodes)
        """
        texts = []

        for node_id in self._graph_nx.nodes:
            one_game = self._graph_nx.nodes[node_id]['game_obj']

            text = f'Game: {one_game.get_game_name()}'
            text += f'<br>Price: {one_game.get_price()}'
            text += f'<br>Genre: {", ".join(one_game.get_game_genre())}'
            text += f'<br>Platform: {", ".join(one_game.get_platform())}'

            comments = self._source_graph.get_comments_for_game(node_id)
            if comments:
                text += '<br><br>Comments:'
                for comment in comments:
                    text += f'<br>- {comment}'

            texts.append(text)

        return texts

    def build_edge_trace(self, pos: dict[Any, tuple[float, float]]) -> go.Scatter:
        """Return a Plotly trace for the edges in this graph.

        Preconditions:
        - set(self._graph_nx.nodes).issubset(pos)
        """
        x_edges = []
        y_edges = []
        edge_texts = []

        for edge in self._graph_nx.edges:
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]

            similarity = self._graph_nx.edges[edge].get('similarity', None)
            if similarity is None:
                text = ''
            else:
                text = f'Similarity: {similarity:.2f}'

            x_edges.extend([x0, x1, None])
            y_edges.extend([y0, y1, None])
            edge_texts.extend([text, text, None])

        return go.Scatter(
            x=x_edges,
            y=y_edges,
            mode='lines',
            line={'width': 1, 'color': 'gray'},
            hoverinfo='text',
            text=edge_texts
        )

    def build_node_trace(self, pos: dict[Any, tuple[float, float]]) -> go.Scatter:
        """Return a Plotly trace for the nodes in this graph.

        The center game is coloured red. Other games are coloured according to
        their primary genre.

        Preconditions:
            - set(self._graph_nx.nodes).issubset(pos)
        """
        x_nodes = []
        y_nodes = []
        node_ids = list(self._graph_nx.nodes)
        hover_texts = self.build_node_texts()
        colours = []
        labels = []

        for node_id in node_ids:
            x, y = pos[node_id]
            x_nodes.append(x)
            y_nodes.append(y)

            one_game = self._graph_nx.nodes[node_id]['game_obj']
            labels.append(one_game.get_game_name())

            is_center = (node_id == self._center_game.get_app_id())
            colours.append(self.get_node_colour(one_game, is_center))

        return go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode='markers+text',
            text=labels,
            textposition='top center',
            hovertext=hover_texts,
            hoverinfo='text',
            marker={
                'size': 22,
                'color': colours,
                'line': {'width': 1, 'color': 'black'}
            }
        )
    
    def _build_figure(self) -> go.Figure:
        """Return the Plotly figure for this visualization graph."""
        pos = nx.spring_layout(self._graph_nx, seed=42, weight='weight')

        edge_trace = self.build_edge_trace(pos)
        node_trace = self.build_node_trace(pos)

        figure = go.Figure(data=[edge_trace, node_trace])
        figure.update_layout(
            title=f'Steam Game Recommendation Graph: {self._center_game.get_game_name()}',
            title_x=0.5,
            showlegend=False,
            hovermode='closest',
            margin={"b": 20, "l": 20, "r": 20, "t": 60},
            xaxis={"showgrid": False, "zeroline": False, "showticklabels": False},
            yaxis={"showgrid": False, "zeroline": False, "showticklabels": False}
        )
        return figure

    def show(self) -> None:
        """Display this visualization graph in the browser."""
        figure = self._build_figure()
        figure.show()

    def save_html(self, file_name: str) -> None:
        """Save this visualization graph to an HTML file."""
        figure = self._build_figure()
        figure.write_html(file_name)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['networkx', 'plotly.graph_objects', 'game', 'game_user_graph'],
        'allowed-io': [],
        'max-line-length': 120
    })

"""
CSC111 Project 2 VisualizationGraph Class

This file contains the VisualizationGraph class used in project 2.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed, Levi Pan, Haoxuan Shen, Laien Zou.
"""


from __future__ import annotations

from typing import Any
import math
import tempfile
import webbrowser
from pathlib import Path

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
        - _recommended_ids: the app_ids of the recommended games to display
        - _use_given_recommendations: whether to use the given recommendation ids
            instead of computing new ones

    Representation Invariants:
        - self._center_game.get_app_id() in self._source_graph.get_all_vertices('game')
        - all(node_id in self._source_graph.get_all_vertices('game') for node_id in self._graph_nx.nodes)
    """
    _source_graph: GameUserGraph
    _center_game: Game
    _graph_nx: nx.Graph
    _recommended_ids: list[int]
    _use_given_recommendations: bool

    def __init__(self, graph: GameUserGraph, center_game: Game,
                 recommended_ids: list[int] | None = None) -> None:
        """Initialize a visualization graph centered on center_game.

        Preconditions:
        - center_game.get_app_id() in graph.get_all_vertices('game')
        """
        self._source_graph = graph
        self._center_game = center_game
        self._graph_nx = nx.Graph()
        if recommended_ids is None:
            self._recommended_ids = []
            self._use_given_recommendations = False
        else:
            self._recommended_ids = recommended_ids[:]
            self._use_given_recommendations = True
        self._build_local_graph()

    def _build_local_graph(self) -> None:
        """Build the local networkx graph for visualization.

        The local graph contains the center game and the recommended similar
        games returned by the source graph. Nodes are keyed by app_id, while
        displayed labels use game names.

        Preconditions:
            - self._center_game.get_app_id() in self._source_graph.get_all_vertices('game')
        """
        if self._use_given_recommendations:
            recommended_ids = self._recommended_ids
        else:
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
            if game_id == center_id:
                continue

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

    def _wrap_text(self, text: str, line_length: int = 45) -> str:
        """Return text wrapped across multiple HTML lines."""
        words = text.split()
        if not words:
            return text

        lines = []
        current = words[0]
        for word in words[1:]:
            if len(current) + 1 + len(word) <= line_length:
                current += ' ' + word
            else:
                lines.append(current)
                current = word
        lines.append(current)
        return '<br>'.join(lines)

    def _split_label(self, text: str, line_length: int = 26) -> str:
        """Return text split across lines for more compact node labels."""
        words = text.split()
        if not words:
            return text

        lines = []
        current = words[0]
        for word in words[1:]:
            if len(current) + 1 + len(word) <= line_length:
                current += ' ' + word
            else:
                lines.append(current)
                current = word
        lines.append(current)

        if len(lines) > 2:
            return '<br>'.join(lines[:2])
        else:
            return '<br>'.join(lines)

    def get_node_colour(self, is_center: bool) -> str:
        """Return the display colour for a node in this visualization graph.

        The center game is always coloured red. Other games use one shared colour
        to keep the graph visually consistent.
        """
        if is_center:
            return 'red'
        return '#5dade2'

    def build_node_texts(self) -> list[str]:
        """Return hover text for all nodes in this visualization graph.

        Each hover text contains the basic information of one game, including
        its name, price, genre, platform, and available user comments.

        Preconditions:
            - all('game_obj' in self._graph_nx.nodes[node] for node in self._graph_nx.nodes)
        """
        texts = []

        for node_id in self._graph_nx.nodes:
            one_game = self._graph_nx.nodes[node_id]['game_obj']

            text = f'Game: {one_game.get_game_name()}'
            text += f'<br>Price: ${one_game.get_price():.2f}'
            text += f'<br>Genre: {", ".join(one_game.get_game_genre())}'
            text += f'<br>Platform: {", ".join(one_game.get_platform())}'
            text += f'<br>Review: {one_game.get_review_score_description()}'

            if node_id != self._center_game.get_app_id():
                similarity = self._source_graph.get_similarity_score(self._center_game.get_app_id(), node_id)
                text += f'<br>Similarity: {similarity:.2f}'

            comments = self._source_graph.get_comments_for_game(node_id)
            if comments:
                text += '<br><br>Comments:'
                for comment in comments[:1]:
                    wrapped_comment = self._wrap_text(comment, 42)
                    text += f'<br>- {wrapped_comment}'

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

    def _build_center_trace(self, pos: dict[Any, tuple[float, float]],
                            node_text_map: dict[Any, str]) -> go.Scatter:
        """Return the Plotly trace for the center game node."""
        center_id = self._center_game.get_app_id()
        center_game = self._graph_nx.nodes[center_id]['game_obj']
        center_x, center_y = pos[center_id]

        return go.Scatter(
            x=[center_x],
            y=[center_y],
            mode='markers+text',
            text=[self._split_label(center_game.get_game_name())],
            textposition='top center',
            hovertext=[node_text_map[center_id]],
            hoverinfo='text',
            marker={
                'size': 42,
                'color': 'red',
                'line': {'width': 1, 'color': 'black'}
            },
            textfont={'size': 12, 'color': '#30486f'},
            hoverlabel={'bgcolor': '#ff1406', 'font_size': 13, 'font_color': 'white'}
        )

    def _get_outer_node_ids(self) -> list[int]:
        """Return the recommended game ids shown around the center node."""
        center_id = self._center_game.get_app_id()
        outer_ids = []

        for node_id in self._graph_nx.nodes:
            if node_id != center_id:
                outer_ids.append(node_id)

        return outer_ids

    def _build_outer_trace(self, pos: dict[Any, tuple[float, float]],
                           node_text_map: dict[Any, str]) -> go.Scatter:
        """Return the Plotly trace for the surrounding recommendation nodes."""
        outer_ids = self._get_outer_node_ids()
        x_nodes = []
        y_nodes = []
        labels = []
        hover_texts = []

        for node_id in outer_ids:
            x, y = pos[node_id]
            x_nodes.append(x)
            y_nodes.append(y)
            one_game = self._graph_nx.nodes[node_id]['game_obj']
            labels.append(self._split_label(one_game.get_game_name()))
            hover_texts.append(node_text_map[node_id])

        return go.Scatter(
            x=x_nodes,
            y=y_nodes,
            mode='markers+text',
            text=labels,
            textposition='top center',
            hovertext=hover_texts,
            hoverinfo='text',
            marker={
                'size': 34,
                'color': '#5dade2',
                'line': {'width': 1, 'color': 'black'}
            },
            textfont={'size': 12, 'color': '#30486f'},
            hoverlabel={'bgcolor': '#5dade2', 'font_size': 13, 'font_color': 'white'}
        )

    def build_node_traces(self, pos: dict[Any, tuple[float, float]]) -> list[go.Scatter]:
        """Return Plotly traces for the center node and surrounding nodes."""
        node_text_map = dict(zip(self._graph_nx.nodes, self.build_node_texts()))
        center_trace = self._build_center_trace(pos, node_text_map)
        outer_trace = self._build_outer_trace(pos, node_text_map)

        return [outer_trace, center_trace]

    def _get_similarity_extremes(self, node_ids: list[int]) -> tuple[float, float]:
        """Return the minimum and maximum similarity among the given nodes."""
        similarities = []

        for node_id in node_ids:
            similarities.append(self._graph_nx.nodes[node_id].get('similarity_to_center', 0.0))

        return (min(similarities), max(similarities))

    @staticmethod
    def _normalized_similarity(similarity: float, min_similarity: float,
                               max_similarity: float) -> float:
        """Return similarity rescaled into the interval [0, 1]."""
        if max_similarity == min_similarity:
            return 0.5
        else:
            return (similarity - min_similarity) / (max_similarity - min_similarity)

    def _build_star_layout(self) -> dict[Any, tuple[float, float]]:
        """Return a deterministic star-like layout centered on the selected game.

        Games with higher similarity to the center game are placed closer to it.
        """
        center_id = self._center_game.get_app_id()
        node_ids = self._get_outer_node_ids()

        pos = {center_id: (0.0, 0.0)}
        if not node_ids:
            return pos

        step = (2 * math.pi) / len(node_ids)
        min_radius = 0.65
        max_radius = 1.55
        min_similarity, max_similarity = self._get_similarity_extremes(node_ids)

        for index, node_id in enumerate(node_ids):
            angle = (math.pi / 2) - index * step
            similarity = self._graph_nx.nodes[node_id].get('similarity_to_center', 0.0)
            normalized_similarity = self._normalized_similarity(
                similarity, min_similarity, max_similarity
            )

            radius = max_radius - normalized_similarity * (max_radius - min_radius)
            pos[node_id] = (radius * math.cos(angle), radius * math.sin(angle))

        return pos

    def _build_figure(self) -> go.Figure:
        """Return the Plotly figure for this visualization graph."""
        pos = self._build_star_layout()

        edge_trace = self.build_edge_trace(pos)
        node_traces = self.build_node_traces(pos)

        figure = go.Figure(data=[edge_trace, *node_traces])
        figure.update_layout(
            title=f'Steam Game Recommendation Graph: {self._center_game.get_game_name()}',
            title_x=0.5,
            title_y=0.98,
            showlegend=False,
            hovermode='closest',
            width=1500,
            height=900,
            plot_bgcolor='#dbe3f0',
            paper_bgcolor='white',
            font={'family': 'Helvetica, Arial, sans-serif', 'size': 16, 'color': '#30486f'},
            margin={"b": 20, "l": 20, "r": 20, "t": 70},
            xaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "range": [-2.1, 2.1],
                "constrain": "domain"
            },
            yaxis={
                "showgrid": False,
                "zeroline": False,
                "showticklabels": False,
                "range": [-2.1, 2.1],
                "scaleanchor": "x",
                "scaleratio": 1
            },
            annotations=[
                {
                    'text': ('Legend: red = center game, blue = recommended games, and games '
                             'with higher similarity are placed closer to the center.'),
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0.5,
                    'y': 0.98,
                    'showarrow': False,
                    'font': {'size': 13, 'color': '#30486f'}
                }
            ]
        )
        return figure

    def show(self) -> None:
        """Display this visualization graph in the browser."""
        figure = self._build_figure()
        temp_path = self._write_temp_html(figure, 'steam_recommendation_graph_')
        webbrowser.open(temp_path.as_uri())

    def _build_positive_ratio_figure(self) -> go.Figure:
        """Return a bar chart showing positive review ratio for the center and recommended games."""
        game_names = []
        positive_ratios = []

        display_ids = [self._center_game.get_app_id()]
        for game_id in self._recommended_ids:
            if game_id not in display_ids:
                display_ids.append(game_id)

        for game_id in display_ids:
            one_game = self._source_graph.get_game(game_id)
            positive_ratio = one_game.get_positive_ratio()

            if positive_ratio is not None:
                game_names.append(one_game.get_game_name())
                positive_ratios.append(positive_ratio)

        bar_colours = []
        if positive_ratios == []:
            highest_ratio = None
        else:
            highest_ratio = max(positive_ratios)

        for positive_ratio in positive_ratios:
            if positive_ratio == highest_ratio:
                bar_colours.append('red')
            else:
                bar_colours.append('#5dade2')

        figure = go.Figure()
        figure.add_trace(
            go.Bar(
                x=game_names,
                y=positive_ratios,
                marker={'color': bar_colours}
            )
        )
        figure.update_layout(
            title='Positive Review Ratio of the Center and Recommended Games',
            title_x=0.5,
            xaxis_title='Displayed Games',
            yaxis_title='Positive Review Ratio',
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'family': 'Helvetica, Arial, sans-serif', 'size': 14, 'color': '#30486f'},
            margin={"b": 150, "l": 60, "r": 30, "t": 110},
            annotations=[
                {
                    'text': 'Legend: red = highest positive review ratio',
                    'xref': 'paper',
                    'yref': 'paper',
                    'x': 0.5,
                    'y': 1.08,
                    'showarrow': False,
                    'font': {'size': 12, 'color': '#30486f'}
                }
            ]
        )
        figure.update_xaxes(tickangle=-25)
        figure.update_yaxes(range=[0, 1])
        return figure

    def show_positive_ratio_chart(self) -> None:
        """Display the positive review ratio bar chart in the browser."""
        figure = self._build_positive_ratio_figure()
        temp_path = self._write_temp_html(figure, 'steam_positive_ratio_chart_')
        webbrowser.open(temp_path.as_uri())

    def _write_temp_html(self, figure: go.Figure, prefix: str) -> Path:
        """Write figure to a temporary HTML file and return its path."""
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', prefix=prefix, delete=False)
        temp_path = Path(temp_file.name)
        temp_file.close()
        figure.write_html(str(temp_path))
        return temp_path

    def save_html(self, file_name: str) -> None:
        """Save this visualization graph to an HTML file."""
        figure = self._build_figure()
        figure.write_html(file_name)


if __name__ == '__main__':
    import doctest
    import python_ta

    doctest.testmod()

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': [
            'typing', 'math', 'tempfile', 'webbrowser', 'pathlib',
            'networkx', 'plotly.graph_objects', 'game', 'game_user_graph'
        ],
        'allowed-io': ['VisualizationGraph.show', 'VisualizationGraph.show_positive_ratio_chart']
    })

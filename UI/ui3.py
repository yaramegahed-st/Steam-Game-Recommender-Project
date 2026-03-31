"""
CSC111 Project 2 Steam UI

This file defines the Tkinter interface for the Steam game recommender system.
It collects user preferences, shows recommended games, and links the results to
the browser-based recommendation graph visualization.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of the group by Yara Megahed
in CSC111 project 2 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are expressly prohibited.

This file is Copyright 2026 CSC111 Project 2 Group Yara Megahed, Levi Pan, Haoxuan Shen, Laien Zou.
"""

from __future__ import annotations

from functools import partial
from pathlib import Path
from typing import Any
from tkinter import Tk, Frame, Label, Button, Entry, BooleanVar, Checkbutton, Scale, IntVar, Text, Scrollbar

from PIL import Image, ImageTk

import game_user_graph
from game_user_graph import GameUserGraph
from visualization.visualization_graph import VisualizationGraph
from file_reading import read_file, clean_up_line

PROJECT_ROOT = Path(__file__).resolve().parent.parent
UI_DIR = Path(__file__).resolve().parent

GENRE = ["Action", "Adventure", "Casual", "Indie", "Massively Multiplayer", "Racing", "RPG", "Simulation", "Sports",
         "Strategy", "Free to Play", "Early Access"]

BG_COLOUR = "#DCDCDC"
CARD_COLOUR = "#EBEBEB"
PRIMARY_TEXT = "#1b2838"
SECONDARY_TEXT = "#4f6b82"
ACCENT_COLOUR = "#66c0f4"
ACCENT_DARK = "#0f4061"
SOFT_BORDER = "#c9dceb"
ERROR_COLOUR = "#c0392b"
BUTTON_TEXT = "#0a1a28"


class Interface:
    """A Tkinter interface for collecting preferences and displaying recommendations.

    Instance Attributes:
        - window: The main Tkinter window for the application.
        - container: The outer frame that stores all page frames.
        - graph: The recommendation graph used to generate results.
        - game_data: The path to the game dataset used for title matching.
        - q1_error_label: The error label shown on the favourite-game page.
        - q2_error_label: The error label shown on the genre page.
        - q3_error_label: The error label shown on the budget page.
        - min_budget: The Tkinter variable storing the minimum budget.
        - max_budget: The Tkinter variable storing the maximum budget.
        - frames: The page frames in this interface, keyed by page name.
        - entries: Text-entry widgets keyed by question id.
        - answers: The stored survey answers keyed by question id.
        - q2_vars: The checkbox variables for the genre question.
        - result_games_label: The label used to display the result summary.
        - result_text_widget: The text widget used to display recommendation details.
        - visual_status_label: The status label shown on the visualization page.
        - visual_comments_text_widget: The text widget showing user comments.
        - selected_game: The selected or fallback starting game for the current results.
        - selection_message: The explanation shown above the recommendation results.
        - current_result_ids: The app_ids currently displayed on the results page.
        - img: The home-page image resource kept alive for Tkinter.
        - result_frame: The frame used for the recommendation results page.

    Representation Invariants:
        - 'home' in self.frames
        - 'q1' in self.frames
        - 'q2' in self.frames
        - 'q3' in self.frames
        - 'result' in self.frames
        - 'visual' in self.frames
    """

    window: Tk
    container: Frame
    graph: GameUserGraph
    game_data: str
    q1_error_label: Label | None
    q2_error_label: Label | None
    q3_error_label: Label | None
    min_budget: IntVar | None
    max_budget: IntVar | None
    frames: dict[str, Frame]
    entries: dict[str, Entry]
    answers: dict[str, dict[str, Any]]
    q2_vars: dict[str, BooleanVar]
    result_games_label: Label | None
    result_text_widget: Text | None
    visual_status_label: Label | None
    visual_comments_text_widget: Text | None
    selected_game: Any | None
    selection_message: str
    current_result_ids: list[int]
    img: Any
    result_frame: Frame

    def __init__(self, source_graph: GameUserGraph, game_data: str) -> None:
        """Initialize the full Steam recommender interface.

        This sets up the main window, stores the shared recommendation data,
        creates all survey/result/visualization pages, and starts the Tkinter
        event loop.
        """
        self.window = Tk()
        self.window.title("Steam Game Finder")
        self.window.geometry("1000x1000")
        self.window.configure(bg=BG_COLOUR)

        self.container = Frame(self.window, bg=BG_COLOUR)
        self.container.pack(fill="both", expand=True)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.graph = source_graph
        self.game_data = game_data

        self.q1_error_label = None
        self.q2_error_label = None
        self.q3_error_label = None

        self.min_budget = None
        self.max_budget = None

        self.frames = {}
        self.entries = {}
        self.answers = {}
        self.q2_vars = {}
        self.result_games_label = None
        self.result_text_widget = None
        self.visual_status_label = None
        self.visual_comments_text_widget = None
        self.selected_game = None
        self.selection_message = ''
        self.current_result_ids = []

        self.create_home_frame()
        self.create_q1_frame()
        self.create_q2_frame()
        self.create_q3_frame()
        self.create_result_visual_frame()
        self.create_visual_frame()
        self.create_last_page()

        self.show_frame("home")
        self.window.mainloop()

    def _build_card(self, frame: Frame, width: int = 760) -> Frame:
        """Return a centred card-style frame."""
        card = Frame(frame, bg=CARD_COLOUR, highlightbackground=SOFT_BORDER, highlightthickness=1)
        card.place(relx=0.5, rely=0.5, anchor="center", width=width)
        return card

    def _make_primary_button(self, parent: Frame, text: str, command: object) -> Button:
        """Return a consistently styled primary button."""
        return Button(
            parent,
            text=text,
            font=("Helvetica", 17, "bold"),
            command=command,
            bg=ACCENT_COLOUR,
            fg=BUTTON_TEXT,
            activebackground="#9ddcff",
            activeforeground=BUTTON_TEXT,
            relief="flat",
            bd=0,
            padx=20,
            pady=12,
            cursor="hand2"
        )

    def _make_secondary_button(self, parent: Frame, text: str, command: object) -> Button:
        """Return a consistently styled secondary button."""
        return Button(
            parent,
            text=text,
            font=("Helvetica", 14),
            command=command,
            bg="#e8f0f8",
            fg=PRIMARY_TEXT,
            activebackground="#d7e6f4",
            activeforeground=PRIMARY_TEXT,
            relief="flat",
            bd=0,
            padx=16,
            pady=10,
            cursor="hand2"
        )

    def create_home_frame(self) -> None:
        """Create the home page."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["home"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        image = Image.open(UI_DIR / "video_games.jpg")
        image = image.resize((420, 240))
        self.img = ImageTk.PhotoImage(image)

        card = self._build_card(frame, width=780)

        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=36)
        inner.pack(fill="both", expand=True)

        badge = Label(
            inner,
            text="◉  STEAM GAME FINDER",
            font=("Helvetica", 15, "bold"),
            bg=CARD_COLOUR,
            fg=ACCENT_DARK
        )
        badge.pack(pady=(0, 14))

        title = Label(
            inner,
            text="Steam Games you can't Miss!!",
            font=("Helvetica", 30, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        title.pack(pady=(0, 10))

        subtitle = Label(
            inner,
            text=(
                "Answer a few quick questions to get a Top Ten list of Steam-style "
                "recommendations based on your favourite game, genres, and budget."
            ),
            font=("Helvetica", 15),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=650,
            justify="center"
        )
        subtitle.pack(pady=(0, 24))

        image_label = Label(inner, image=self.img, bg=CARD_COLOUR)
        image_label.pack(pady=(0, 24))

        start_button = self._make_primary_button(inner, "Start Survey", partial(self.show_frame, "q1"))
        start_button.pack()

    def create_q1_frame(self) -> None:
        """Create the question 1 page."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["q1"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=34)
        inner.pack(fill="both", expand=True)

        label = Label(
            inner,
            text="Question 1",
            font=("Helvetica", 26, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        label.pack(pady=(0, 16))

        question = Label(
            inner,
            text="What is your favourite Steam game, one that you are currently playing? Enter only one game. "
                 "If you enter more than one game, we will only pick the first one.",
            font=("Helvetica", 16),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=620,
            justify="center"
        )
        question.pack(pady=(0, 18))

        entry = Entry(
            inner,
            font=("Helvetica", 17),
            width=32,
            relief="flat",
            bg="#f3f8fc",
            fg=PRIMARY_TEXT,
            highlightthickness=1,
            highlightbackground=SOFT_BORDER,
            highlightcolor=ACCENT_COLOUR
        )
        entry.pack(pady=(0, 12), ipady=10)

        self.entries["q1"] = entry

        self.q1_error_label = Label(
            inner,
            text="",
            font=("Helvetica", 13),
            fg=ERROR_COLOUR,
            bg=CARD_COLOUR
        )
        self.q1_error_label.pack(pady=(0, 10))

        self._make_primary_button(inner, "Continue",
                                  lambda: self.save_q1_answer("q1", "q2")).pack(pady=(4, 12))
        self._make_secondary_button(inner, "Back", lambda: self.show_frame("home")).pack()

    def create_q2_frame(self) -> None:
        """Create the question 2 page."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["q2"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=30)
        inner.pack(fill="both", expand=True)

        label = Label(
            inner,
            text="Question 2",
            font=("Helvetica", 26, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        label.pack(pady=(0, 16))

        question = Label(
            inner,
            text="What genres do you usually enjoy? Pick as many as you like.",
            font=("Helvetica", 16),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT
        )
        question.pack(pady=(0, 18))

        options_frame = Frame(inner, bg=CARD_COLOUR)
        options_frame.pack(pady=(0, 12))

        self.q2_error_label = Label(
            inner,
            text="",
            font=("Helvetica", 13),
            fg=ERROR_COLOUR,
            bg=CARD_COLOUR
        )
        self.q2_error_label.pack(pady=(0, 8))

        for genre in GENRE:
            var = BooleanVar()
            self.q2_vars[genre] = var

            cb = Checkbutton(
                options_frame,
                text=genre,
                variable=var,
                font=("Helvetica", 14),
                bg=CARD_COLOUR,
                fg=PRIMARY_TEXT,
                activebackground=CARD_COLOUR,
                activeforeground=PRIMARY_TEXT,
                selectcolor="#dceefa",
                anchor="w"
            )
            cb.pack(anchor="w")

        self._make_primary_button(inner, "Continue", self.save_q2_answers).pack(pady=(8, 12))
        self._make_secondary_button(inner, "Back", partial(self.show_frame, "q1")).pack()

    def create_q3_frame(self) -> None:
        """Create the budget question page."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["q3"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=30)
        inner.pack(fill="both", expand=True)

        label = Label(
            inner,
            text="Question 3",
            font=("Helvetica", 26, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        label.pack(pady=(0, 16))

        question = Label(
            inner,
            text="What is your budget. The wider the range the more steams games can be searched.",
            font=("Helvetica", 16),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=620,
            justify="center"
        )
        question.pack(pady=(0, 18))

        self.min_budget = IntVar(value=0)
        self.max_budget = IntVar(value=250)

        Label(inner, text="Minimum price", bg=CARD_COLOUR, fg=PRIMARY_TEXT, font=("Helvetica", 14, "bold")).pack()
        Scale(
            inner,
            from_=0,
            to=250,
            orient="horizontal",
            variable=self.min_budget,
            length=420,
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT,
            highlightthickness=0,
            troughcolor="#dcecf8",
            activebackground=ACCENT_COLOUR
        ).pack(pady=(6, 10))

        Label(inner, text="Maximum price", bg=CARD_COLOUR, fg=PRIMARY_TEXT, font=("Helvetica", 14, "bold")).pack()
        Scale(
            inner,
            from_=0,
            to=250,
            orient="horizontal",
            variable=self.max_budget,
            length=420,
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT,
            highlightthickness=0,
            troughcolor="#dcecf8",
            activebackground=ACCENT_COLOUR
        ).pack(pady=(6, 10))

        self.q3_error_label = Label(
            inner,
            text="",
            fg=ERROR_COLOUR,
            bg=CARD_COLOUR,
            font=("Helvetica", 13)
        )
        self.q3_error_label.pack()

        self._make_primary_button(inner, "See Results", self.save_q3_answer).pack(pady=(10, 12))
        self._make_secondary_button(inner, "Back", partial(self.show_frame, "q2")).pack()

    def create_result_visual_frame(self) -> None:
        """Create page that displays results and allow option to show visualization."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["result"] = frame
        self.result_frame = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame, width=720)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=34)
        inner.pack(fill="both", expand=True)

        label = Label(
            inner,
            text="Your Steam Picks Are Ready",
            font=("Helvetica", 26, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        label.pack(pady=(0, 14))

        question = Label(
            inner,
            text="You can review the top recommendations here and open the Steam-style graph visualisation next.",
            font=("Helvetica", 15),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=620,
            justify="center"
        )
        question.pack(pady=(0, 18))

        self.result_games_label = Label(
            inner,
            text="Finish the survey to see your Steam recommendations here.",
            font=("Helvetica", 14),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT,
            wraplength=620,
            justify="left"
        )
        self.result_games_label.pack(pady=(0, 8))

        text_frame = Frame(inner, bg=CARD_COLOUR)
        text_frame.pack(pady=(0, 18))

        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side="right", fill="y")

        self.result_text_widget = Text(
            text_frame,
            width=64,
            height=14,
            font=("Helvetica", 12),
            bg="#f3f8fc",
            fg=PRIMARY_TEXT,
            wrap="word",
            relief="flat",
            bd=1,
            yscrollcommand=scrollbar.set
        )
        self.result_text_widget.pack(side="left", fill="both", expand=True)
        self.result_text_widget.insert("1.0", "Your recommendation details will appear here.")
        self.result_text_widget.config(state="disabled")
        scrollbar.config(command=self.result_text_widget.yview)

        self._make_primary_button(inner, "Open Visual Graph", self.open_visual_page).pack(pady=(8, 12))
        self._make_secondary_button(inner, "Back", partial(self.show_frame, "q3")).pack(pady=(0, 10))
        self._make_secondary_button(inner, "Back to Home", self.reset_survey).pack()

    def create_visual_frame(self) -> None:
        """Create the visualisation page."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["visual"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame, width=680)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=34)
        inner.pack(fill="both", expand=True)

        label = Label(
            inner,
            text="Steam Recommendation Graph",
            font=("Helvetica", 24, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        label.pack(pady=(0, 12))

        subtitle = Label(
            inner,
            text="You can open the interactive graph in your browser. Alternatively, "
                 "you can see user comments on the recommended games in the next page "
                 "or open the positive ratio to compare game quality based on reviews. ",
            font=("Helvetica", 15),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=560,
            justify="center"
        )
        subtitle.pack(pady=(0, 18))

        self.visual_status_label = Label(
            inner,
            text="Click the button below to open the recommendation graph in your browser.",
            font=("Helvetica", 14),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=560,
            justify="center"
        )
        self.visual_status_label.pack(pady=(0, 18))

        self._make_primary_button(inner, "Open Graph in Browser", self.open_visualization).pack(pady=(0, 12))
        self._make_secondary_button(inner, "Open Positive Ratio Chart", self.open_positive_ratio_chart).pack(
            pady=(0, 12)
        )
        self._make_secondary_button(inner, "Open Comments page", partial(self.show_frame, "comments")).pack(
            pady=(0, 12)
        )

        self._make_secondary_button(inner, "Back", partial(self.show_frame, "result")).pack(pady=(0, 10))
        self._make_secondary_button(inner, "Back to Home", self.reset_survey).pack()

    def create_last_page(self) -> None:
        """Create the last page containing user comments on the recommended games"""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["comments"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        card = self._build_card(frame, width=680)
        inner = Frame(card, bg=CARD_COLOUR, padx=40, pady=34)
        inner.pack(fill="both", expand=True)

        comments_label = Label(
            inner,
            text="Comments from previous users who played the selected and recommended games:",
            font=("Helvetica", 14, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        comments_label.pack(pady=(8, 8))

        comments_frame = Frame(inner, bg=CARD_COLOUR)
        comments_frame.pack(pady=(0, 18))

        comments_scrollbar = Scrollbar(comments_frame)
        comments_scrollbar.pack(side="right", fill="y")

        self.visual_comments_text_widget = Text(
            comments_frame,
            width=62,
            height=12,
            font=("Helvetica", 11),
            bg="#f3f8fc",
            fg=PRIMARY_TEXT,
            wrap="word",
            relief="flat",
            bd=1,
            yscrollcommand=comments_scrollbar.set
        )
        self.visual_comments_text_widget.pack(side="left", fill="both", expand=True)
        self.visual_comments_text_widget.insert("1.0", "Open this page from the "
                                                       "results screen to view comments.")
        self.visual_comments_text_widget.config(state="disabled")
        comments_scrollbar.config(command=self.visual_comments_text_widget.yview)

        self._make_secondary_button(inner, "Back", partial(self.show_frame, "visual")).pack(pady=(0, 10))
        self._make_secondary_button(inner, "Back to Home", self.reset_survey).pack()

    def show_frame(self, name: str) -> None:
        """Bring the selected frame to the front."""
        frame = self.frames[name]
        frame.tkraise()

    def save_q1_answer(self, current_question: str, next_frame: str) -> None:
        """Save the user's answer, generate keywords, and move to next frame."""
        text = self.entries[current_question].get().strip()

        if text == "":
            self.q1_error_label.config(text="Please enter a game!")
            return
        self.q1_error_label.config(text="")

        self.answers[current_question] = {
            "raw": text,
            "keywords": self.extract_keywords(text)
        }

        print(f'Q1 answer: {self.answers[current_question]}')
        self.show_frame(next_frame)

    def extract_keywords(self, text: str) -> list[str]:
        """Return the best-matching cleaned game title from user input.

        If multiple consecutive word groups match game titles, prefer the
        longest matching title instead of the first short partial match.
        """
        game_names = read_file(self.game_data)

        user_words = text.lower().replace(",", " ").replace(".", " ").split()
        best_match = ''

        for i in range(len(user_words)):
            for j in range(i + 1, len(user_words) + 1):
                candidate = ''
                for word in user_words[i:j]:
                    candidate += clean_up_line(word)
                if candidate in game_names and len(candidate) > len(best_match):
                    best_match = candidate

        if best_match == '':
            return []
        else:
            return [best_match]

    def save_q2_answers(self) -> None:
        """Save the selected genres."""
        selected = []

        for genre, var in self.q2_vars.items():
            if var.get():
                selected.append(genre)

        if not selected:
            self.q2_error_label.config(text="Please choose at least one genre!")
            return

        self.q2_error_label.config(text="")

        self.answers["q2"] = {
            "keywords": selected
        }

        print(f'Q2 answer: {self.answers["q2"]}')
        self.show_frame("q3")

    def save_q3_answer(self) -> None:
        """Save the selected budget range."""
        min_val = self.min_budget.get()
        max_val = self.max_budget.get()

        if min_val >= max_val:
            self.q3_error_label.config(text="minimum price cannot be greater than or equal to maximum price!")
            return

        self.q3_error_label.config(text="")

        self.answers["q3"] = {
            "min": min_val,
            "max": max_val
        }

        print(f'Q3 answer: {self.answers["q3"]}')
        self.displays_graph_results()
        self.show_frame("result")

    def reset_survey(self) -> None:
        """Clear all user inputs and stored answers."""
        for entry in self.entries.values():
            entry.delete(0, "end")

        for var in self.q2_vars.values():
            var.set(False)

        if self.min_budget:
            self.min_budget.set(0)
        if self.max_budget:
            self.max_budget.set(250)

        self.answers.clear()
        self.current_result_ids = []
        self.selected_game = None
        self.selection_message = ''

        if self.q1_error_label:
            self.q1_error_label.config(text="")
        if self.q2_error_label:
            self.q2_error_label.config(text="")
        if self.q3_error_label:
            self.q3_error_label.config(text="")

        self.show_frame("home")

    def get_user_answers(self) -> dict[str, dict[str, Any]]:
        """Return the stored survey answers."""
        return self.answers

    def _filter_results_by_genre(self, names: list[str], ids: list[int],
                                 genres: list[str]) -> tuple[list[str], list[int]]:
        """Return only the recommended games that match at least one selected genre."""
        filtered_names = []
        filtered_ids = []

        for name, game_id in zip(names, ids):
            one_game = self.graph.get_game(game_id)
            matches_genre = False
            for genre in one_game.get_game_genre():
                if genre in genres:
                    matches_genre = True

            if matches_genre:
                filtered_names.append(name)
                filtered_ids.append(game_id)

        return filtered_names, filtered_ids

    def _get_fallback_candidates(self, genres: list[str], min_price: int,
                                 max_price: int) -> list:
        """Return possible fallback starting games matching the selected filters."""
        possible_games = []

        for one_game in self.graph.get_games().values():
            matches_genre = False
            for genre in one_game.get_game_genre():
                if genre in genres:
                    matches_genre = True
            matches_price = min_price <= one_game.get_price() <= max_price

            if matches_genre and matches_price and one_game.is_recommendable():
                possible_games.append(one_game)

        return possible_games

    def _fallback_game_key(self, one_game: Any) -> tuple[float, int, int]:
        """Return the sort key for choosing a fallback game."""
        positive_ratio = one_game.get_positive_ratio()
        if positive_ratio is None:
            positive_ratio_value = -1.0
        else:
            positive_ratio_value = positive_ratio

        num_positive = one_game.get_num_positive_review()
        num_negative = one_game.get_num_negative_review()
        if num_positive is None or num_negative is None:
            total_reviews = -1
        else:
            total_reviews = num_positive + num_negative

        return (positive_ratio_value, total_reviews, -one_game.get_app_id())

    def _include_fallback_in_results(self, names: list[str], ids: list[int]) -> tuple[list[str], list[int]]:
        """Return the displayed results with the fallback starting game included first.

        The selected fallback game is added to the front of the displayed list if it
        is not already present. The returned lists are then trimmed to at most 10 items.
        """
        if self.selected_game is None:
            return names, ids

        selected_id = self.selected_game.get_app_id()
        selected_name = self.selected_game.get_game_name()

        updated_names = names[:]
        updated_ids = ids[:]

        if selected_id not in updated_ids:
            updated_names.insert(0, selected_name)
            updated_ids.insert(0, selected_id)

        return updated_names[:10], updated_ids[:10]

    def open_visualization(self) -> None:
        """Open the local recommendation graph in the browser."""
        selected_game = self.selected_game

        if selected_game is None:
            self.visual_status_label.config(text="Could not find the selected game in the graph.")
            return
        if not self.current_result_ids:
            self.visual_status_label.config(
                text="There are no recommended games to visualize for your current filters."
            )
            return

        visual_graph = VisualizationGraph(self.graph, selected_game, self.current_result_ids)
        visual_graph.show()
        self.visual_status_label.config(text=f"Opened the graph for {selected_game.get_game_name()} in your browser.")

    def open_positive_ratio_chart(self) -> None:
        """Open the positive review ratio chart in the browser."""
        selected_game = self.selected_game

        if selected_game is None:
            self.visual_status_label.config(text="Could not find the selected game in the graph.")
            return
        if not self.current_result_ids:
            self.visual_status_label.config(
                text="There are no recommended games to visualize for your current filters."
            )
            return

        visual_graph = VisualizationGraph(self.graph, selected_game, self.current_result_ids)
        visual_graph.show_positive_ratio_chart()
        self.visual_status_label.config(text="Opened the positive review ratio chart in your browser.")

    def open_visual_page(self) -> None:
        """Populate the comments panel and show the visualization page."""
        self.update_visual_comments_panel()
        self.show_frame("visual")

    def update_visual_comments_panel(self) -> None:
        """Update the visualization page comments panel."""
        if self.visual_comments_text_widget is None:
            return

        if self.selected_game is None:
            text = "No selected game is available yet."
        elif self.current_result_ids == []:
            text = "There are no recommended games to show comments for with your current filters."
        else:
            ordered_ids = [self.selected_game.get_app_id()]
            for game_id in self.current_result_ids:
                if game_id not in ordered_ids:
                    ordered_ids.append(game_id)

            blocks = []
            for game_id in ordered_ids:
                one_game = self.graph.get_game(game_id)
                comments = self.graph.get_comments_for_game(game_id)
                if comments:
                    comments_text = '\n'.join(f'- {comment}' for comment in comments)
                else:
                    comments_text = 'No comments available.'

                blocks.append(f'{one_game.get_game_name()}\n{comments_text}')

            text = '\n\n'.join(blocks)

        self.visual_comments_text_widget.config(state="normal")
        self.visual_comments_text_widget.delete("1.0", "end")
        self.visual_comments_text_widget.insert("1.0", text)
        self.visual_comments_text_widget.config(state="disabled")

    def return_graph_results(self, game_name: str, genres: list[str], min_price: int,
                             max_price: int) -> tuple[list[str], list[int]]:
        """Return recommended game names and ids for the current survey answers.

        If the typed game is found in the dataset, use it as the starting point.
        Otherwise, choose a deterministic fallback game that matches the selected
        genres and budget, and then generate recommendations from that game.
        """
        for game in self.graph.get_games().values():
            if clean_up_line(game.get_game_name()) == game_name:
                app_id = game.get_app_id()
                self.selected_game = game
                self.selection_message = (
                    f"We found '{game.get_game_name()}' in our dataset, so we used it as "
                    f"the main starting point for your recommendations, together with the "
                    f"other indicators we asked of you."
                )
                rec_names, rec_ids = self.graph.recommended_ten_top_games(app_id, min_price, max_price)
                return self._filter_results_by_genre(rec_names, rec_ids, genres)

        possible_games = self._get_fallback_candidates(genres, min_price, max_price)

        if possible_games:
            self.selected_game = max(possible_games, key=self._fallback_game_key)
            self.selection_message = (
                f"We could not find your typed game in our dataset, so we used "
                f"'{self.selected_game.get_game_name()}' as the fallback starting point "
                f"for your recommendations. We chose it because it fit the other "
                f"indicators we asked of you, such as your selected genres and budget."
            )
            rec_names, rec_ids = self.graph.recommended_ten_top_games(
                self.selected_game.get_app_id(), min_price, max_price
            )
            filtered_names, filtered_ids = self._filter_results_by_genre(rec_names, rec_ids, genres)
            return self._include_fallback_in_results(filtered_names, filtered_ids)

        self.selected_game = None
        self.selection_message = (
            "We could not find your typed game and there were no fallback games matching "
            "your filters."
        )
        return [], []

    def displays_graph_results(self) -> None:
        """Update the result page with recommended games and their attributes."""
        game_keywords = self.answers["q1"]["keywords"]
        raw_game_name = self.answers["q1"]["raw"]
        if game_keywords == []:
            game_name = clean_up_line(raw_game_name)
        else:
            game_name = game_keywords[0]
        genres = self.answers["q2"]["keywords"]
        min_price = int(self.answers["q3"]["min"])
        max_price = int(self.answers["q3"]["max"])

        list_games, list_ids = self.return_graph_results(game_name, genres, min_price, max_price)
        self.current_result_ids = list_ids

        if not list_games:
            self.result_games_label.config(
                text=f"{self.selection_message}\n\nNo games matched your current filters."
            )
            self.result_text_widget.config(state="normal")
            self.result_text_widget.delete("1.0", "end")
            self.result_text_widget.insert("1.0", "Try widening your budget or choosing different genres.")
            self.result_text_widget.config(state="disabled")
            return

        formatted_lines = []
        for i in range(len(list_games)):
            one_game = self.graph.get_game(list_ids[i])
            genres_text = ', '.join(one_game.get_game_genre())
            price_text = f"${one_game.get_price():.2f}"
            review_text = one_game.get_review_score_description()

            formatted_lines.append(
                f"{i + 1}. {list_games[i]}\n"
                f"Genre: {genres_text}\n"
                f"Price: {price_text}\n"
                f"Review: {review_text}"
            )

        self.result_games_label.config(
            text=f"{self.selection_message}\n\nHere are your top recommended games:"
        )
        self.result_text_widget.config(state="normal")
        self.result_text_widget.delete("1.0", "end")
        self.result_text_widget.insert("1.0", "\n\n".join(formatted_lines))
        self.result_text_widget.config(state="disabled")


if __name__ == '__main__':
    import doctest
    import python_ta

    game_data_path = PROJECT_ROOT / 'Data' / 'filtered_steam_data_4000.csv'
    user_data_path = PROJECT_ROOT / 'Data' / 'sample_user_data_4000.csv'

    doctest.testmod()

    python_ta.check_all(config={
        'max-line-length': 120,
        'disable': ['static_type_checker'],
        'extra-imports': [
            'functools', 'pathlib', 'typing', 'tkinter', 'PIL', 'file_reading',
            'game_user_graph', 'visualization.visualization_graph'
        ],
        'allowed-io': [
            'Interface.open_visualization',
            'Interface.save_q1_answer',
            'Interface.save_q2_answers',
            'Interface.save_q3_answer'
        ]
    })

    games = game_user_graph.load_game_data(str(game_data_path))
    users = game_user_graph.load_user_data(str(user_data_path))
    built_graph = game_user_graph.load_game_user_graph(games, users)

    Interface(built_graph, str(game_data_path))




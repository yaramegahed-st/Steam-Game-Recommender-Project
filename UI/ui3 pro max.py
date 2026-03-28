from tkinter import Tk, Frame, Label, Button, Entry, BooleanVar, Checkbutton, Scale, IntVar
from PIL import Image, ImageTk
from file_reading import read_file, clean_up_line

GENRE = ["Action", "Adventure", "Casual", "Indie", "Massively Multiplayer", "Racing", "RPG", "Simulation", "Sports",
         "Strategy", "Free to Play", "Early Access"]

BG_COLOUR = "#edf4fb"
CARD_COLOUR = "#ffffff"
PRIMARY_TEXT = "#1b2838"
SECONDARY_TEXT = "#4f6b82"
ACCENT_COLOUR = "#66c0f4"
ACCENT_DARK = "#0f4061"
SOFT_BORDER = "#c9dceb"
ERROR_COLOUR = "#c0392b"
BUTTON_TEXT = "#0a1a28"


class Interface:
    """Interface for user to interact with."""

    def __init__(self) -> None:
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

        self.q1_error_label = None
        self.q2_error_label = None
        self.q3_error_label = None

        self.min_budget = None
        self.max_budget = None

        self.frames = {}
        self.entries = {}
        self.answers = {}
        self.q2_vars = {}

        self.create_home_frame()
        self.create_q1_frame()
        self.create_q2_frame()
        self.create_q3_frame()
        self.create_result_visual_frame()
        self.create_visual_frame()

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

        image = Image.open("video_games.jpg")
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
            text="Find Your Next Steam Game",
            font=("Helvetica", 30, "bold"),
            bg=CARD_COLOUR,
            fg=PRIMARY_TEXT
        )
        title.pack(pady=(0, 10))

        subtitle = Label(
            inner,
            text="Answer a few quick questions and get a shortlist of Steam-style recommendations based on your favourite game, genres, and budget.",
            font=("Helvetica", 15),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=650,
            justify="center"
        )
        subtitle.pack(pady=(0, 24))

        image_label = Label(inner, image=self.img, bg=CARD_COLOUR)
        image_label.pack(pady=(0, 24))

        start_button = self._make_primary_button(inner, "Start Survey", lambda: self.show_frame("q1"))
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
            text="What is your favourite Steam game that you are currently playing? Enter only one game.",
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

        self._make_primary_button(inner, "Continue", lambda: self.save_q1_answer("q1", "q2")).pack(pady=(4, 12))
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

        self._make_primary_button(inner, "Continue", lambda: self.save_q2_answers()).pack(pady=(8, 12))
        self._make_secondary_button(inner, "Back", lambda: self.show_frame("q1")).pack()

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
            text="Choose your budget range. If you leave it wide, the recommender can search more of Steam.",
            font=("Helvetica", 16),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=620,
            justify="center"
        )
        question.pack(pady=(0, 18))

        self.min_budget = IntVar(value=0)
        self.max_budget = IntVar(value=200)

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
            to=200,
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

        self._make_primary_button(inner, "See Results", lambda: self.save_q3_answer()).pack(pady=(10, 12))
        self._make_secondary_button(inner, "Back", lambda: self.show_frame("q2")).pack()

    def create_result_visual_frame(self) -> None:
        """Create page that displays results and allow option to show visualization."""
        frame = Frame(self.container, bg=BG_COLOUR)
        self.frames["result"] = frame

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

        # add a helper function to use the input (data from self.answers) to find top 10 game recs and display as bullet points


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

        self._make_primary_button(inner, "Open Visual Graph", lambda: self.show_frame("visual")).pack(pady=(8, 12))
        self._make_secondary_button(inner, "Back", lambda: self.show_frame("q3")).pack(pady=(0, 10))
        self._make_secondary_button(inner, "Back to Home", lambda: self.reset_survey()).pack()

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
            text="The interactive graph can open in your browser once it is connected to the backend recommendations.",
            font=("Helvetica", 15),
            bg=CARD_COLOUR,
            fg=SECONDARY_TEXT,
            wraplength=560,
            justify="center"
        )
        subtitle.pack(pady=(0, 18))

        self._make_secondary_button(inner, "Back to Home", lambda: self.reset_survey()).pack()

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

        print(self.answers[current_question])
        self.show_frame(next_frame)

    def extract_keywords(self, text: str) -> list[str]:
        """Return a simple keyword list from user input."""
        game_names = read_file("filtered_steam_data_4000.csv")

        user_words = text.lower().replace(",", " ").replace(".", " ").split()
        keywords = []

        for i in range(len(user_words)):
            for j in range(i + 1, len(user_words) + 1):
                candidate = ''.join([clean_up_line(w) for w in user_words[i:j]])
                if candidate in game_names and candidate not in keywords:
                    keywords.append(candidate)
                    break
            if keywords:
                break

        return keywords

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

        print(self.answers["q2"])
        self.show_frame("q3")

    def save_q3_answer(self) -> None:
        """Save the selected budget range."""
        min_val = self.min_budget.get()
        max_val = self.max_budget.get()

        if min_val > max_val:
            self.q3_error_label.config(text="Min cannot be greater than Max!")
            return

        self.q3_error_label.config(text="")

        self.answers["q3"] = {
            "min": min_val,
            "max": max_val
        }

        print(self.answers["q3"])
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
            self.max_budget.set(200)

        self.answers.clear()

        if self.q1_error_label:
            self.q1_error_label.config(text="")
        if self.q2_error_label:
            self.q2_error_label.config(text="")
        if self.q3_error_label:
            self.q3_error_label.config(text="")

        self.show_frame("home")

    def get_user_answers(self):
        """Return the stored survey answers."""
        return self.answers


if __name__ == '__main__':
    Interface()

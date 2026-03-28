from tkinter import Tk, Frame, Label, Button, Entry, BooleanVar, Checkbutton, Scale, IntVar
from PIL import Image, ImageTk
from file_reading import read_file, clean_up_line

GENRE = ["Action", "Adventure", "Casual", "Indie", "Massively Multiplayer", "Racing", "RPG", "Simulation", "Sports",
         "Strategy", "Free to Play", "Early Access"]

class Interface:
    """Interface for user to interact with."""

    def __init__(self) -> None:
        self.window = Tk()
        self.window.title("Game Recommendation")
        self.window.geometry("1000x1000")
        self.window.configure(bg="#1210d9")

        # container holds all frames
        self.container = Frame(self.window, bg="#1210d9")
        self.container.pack(fill="both", expand=True)

        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)

        self.q1_error_label = None
        self.q2_error_label = None
        self.q3_error_label = None
        self.q4_error_label = None

        self.min_budget = None
        self.max_budget = None

        self.frames = {}
        self.entries = {}
        self.answers = {}
        self.q2_vars = {}
        self.q3_vars = {}

        self.create_home_frame()
        self.create_q1_frame()
        self.create_q2_frame()
        self.create_q3_frame()
        self.create_q4_frame()
        self.create_result_visual_frame()
        self.create_visual_frame()


        self.show_frame("home")

        self.window.mainloop()

    def create_home_frame(self) -> None:
        """Create the home page."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["home"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        image = Image.open("video_games.jpg")
        image = image.resize((500, 300))
        self.img = ImageTk.PhotoImage(image)

        content = Frame(frame, bg="#1210d9")
        content.pack(expand=True)

        label = Label(
            content,
            text="This is a game recommendation algorithm.\n"
                 "By answering a few questions, we can provide you with a set of games curated to your liking!",
            font=("Times New Roman", 25),
            bg="#ea1136",
            fg="white",
            wraplength=800,
            justify="center"
        )
        label.pack(pady=20, padx=20)

        image_label = Label(frame, image=self.img, bg="#1210d9")
        image_label.pack(pady=100)

        start_button = Button(
            content,
            text="Click to start survey",
            font=("Times New Roman", 25),
            command=lambda: self.show_frame("q1")
        )
        start_button.pack(pady=20)

    def create_q1_frame(self) -> None:
        """Create the question 1 page."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["q1"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = Label(
            frame,
            text="Question 1",
            font=("Times New Roman", 30),
            bg="#ea1136",
            fg="white"
        )
        label.pack(pady=30)

        question = Label(
            frame,
            text="Question 1: What is your favourite game that you are currently playing? Enter only 1 game."
                 "If you enter more than one game name, we will only pick the first one.",
            font=("Times New Roman", 22),
            bg="#1210d9",
            fg="white",
            wraplength=800,
            justify="center"
        )
        question.pack(pady=20)

        entry = Entry(frame, font=("Times New Roman", 20), width=40)
        entry.pack(pady=20)

        self.entries["q1"] = entry

        self.q1_error_label = Label(
            frame,
            text="",
            font=("Times New Roman", 18),
            fg="red",
            bg="#1210d9"
        )
        self.q1_error_label.pack(pady=10)

        forward_button = Button(
            frame,
            text="Enter",
            font=("Times New Roman", 25),
            command=lambda: self.save_q1_answer("q1", "q2")
        )
        forward_button.pack(pady=20)

        back_button = Button(
            frame,
            text="Back",
            font=("Times New Roman", 20),
            command=lambda: self.show_frame("home")
        )
        back_button.pack(pady=20)

    def create_q2_frame(self) -> None:
        """Create the question 2 page."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["q2"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = Label(
            frame,
            text="Question 2",
            font=("Times New Roman", 30),
            bg="#ea1136",
            fg="white"
        )
        label.pack(pady=30)

        question = Label(
            frame,
            text="Question 2: What are your favorite genres?",
            font=("Times New Roman", 22),
            bg="#1210d9",
            fg="white"
        )
        question.pack(pady=20)

        options_frame = Frame(frame, bg="#1210d9")
        options_frame.pack(pady=10)

        self.q2_error_label = Label(
            frame,
            text="",
            font=("Times New Roman", 18),
            fg="red",
            bg="#1210d9"
        )
        self.q2_error_label.pack(pady=10)

        for genre in GENRE:
            var = BooleanVar()
            self.q2_vars[genre] = var

            cb = Checkbutton(
                options_frame,
                text=genre,
                variable=var,
                font=("Times New Roman", 18),
                bg="#1210d9"
            )
            cb.pack(anchor="w")

        forward_button = Button(
            frame,
            text="Enter",
            font=("Times New Roman", 25),
            command=lambda: self.save_q2_answers()
        )
        forward_button.pack(pady=20)

        back_button = Button(
            frame,
            text="Back",
            font=("Times New Roman", 20),
            command=lambda: self.show_frame("q1")
        )
        back_button.pack(pady=20)

    def create_q3_frame(self) -> None:
        """Create the question 3 page."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["q3"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = Label(
            frame,
            text="Question 3",
            font=("Times New Roman", 30),
            bg="#ea1136",
            fg="white"
        )
        label.pack(pady=30)

        question = Label(
            frame,
            text="Question 3: Do you prefer mainstream or indie games?",
            font=("Times New Roman", 22),
            bg="#1210d9",
            fg="white"
        )
        question.pack(pady=20)

        options_frame = Frame(frame, bg="#1210d9")
        options_frame.pack(pady=10)

        self.q3_error_label = Label(
            frame,
            text="",
            font=("Times New Roman", 18),
            fg="red",
            bg="#1210d9"
        )
        self.q3_error_label.pack(pady=10)

        for choice in [True, False]:
            var = BooleanVar()
            self.q3_vars[choice] = var

            cb = Checkbutton(
                options_frame,
                text= "Yes" if choice else "No",
                variable=var,
                font=("Times New Roman", 18),
                bg="#1210d9"
            )
            cb.pack(anchor="w")

        forward_button = Button(
            frame,
            text="Enter",
            font=("Times New Roman", 25),
            command=lambda: self.save_q3_answers()
        )
        forward_button.pack(pady=20)

        back_button = Button(
            frame,
            text="Back",
            font=("Times New Roman", 20),
            command=lambda: self.show_frame("q2")
        )
        back_button.pack(pady=20)

    def create_q4_frame(self) -> None:
        """Create the question 1 page."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["q4"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = Label(
            frame,
            text="Question 4",
            font=("Times New Roman", 30),
            bg="#ea1136",
            fg="white"
        )
        label.pack(pady=30)

        question = Label(
            frame,
            text="Question 4: What is your budget range? "
                 "If you don't pick any values, it will automate to the minimum and maximum prices on the sliders ",
            font=("Times New Roman", 22),
            bg="#1210d9",
            fg="white",
            wraplength=800,
            justify="center"
        )
        question.pack(pady=20)

        self.min_budget = IntVar(value=0)
        self.max_budget = IntVar(value=200)

        Label(frame, text="Minimum price", bg="#1210d9").pack()
        Scale(
            frame,
            from_=0,
            to=200,
            orient="horizontal",
            variable=self.min_budget,
            length=400
        ).pack(pady=10)

        Label(frame, text="Maximum price", bg="#1210d9").pack()
        Scale(
            frame,
            from_=0,
            to=200,
            orient="horizontal",
            variable=self.max_budget,
            length=400
        ).pack(pady=10)

        self.q4_error_label = Label(
            frame,
            text="",
            fg="red",
            bg="#1210d9",
            font=("Times New Roman", 16)
        )
        self.q4_error_label.pack()

        forward_button = Button(
            frame,
            text="Enter",
            font=("Times New Roman", 25),
            command=lambda: self.save_q4_answer()
        )
        forward_button.pack(pady=20)

        back_button = Button(
            frame,
            text="Back",
            font=("Times New Roman", 20),
            command=lambda: self.show_frame("q3")
        )
        back_button.pack(pady=20)

    def create_result_visual_frame(self) -> None:
        """Create page that displays results and allow option to show visualization."""
        frame = Frame(self.container, bg="#1210d9")
        self.frames["result"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = Label(
            frame,
            text="Here are the results for the top ten most suitable games for you!",
            font=("Times New Roman", 30),
            bg="#1210d9",
            fg="white"
        )
        label.pack(pady=30)

        question = Label(
            frame,
            text="Do you want to access the graph visualisation?",
            font=("Times New Roman", 22),
            bg="#1210d9",
            fg="white"
        )
        question.pack(pady=20)

        forward_button = Button(
            frame,
            text="Yes Please!",
            font=("Times New Roman", 25),
            command=lambda: self.show_frame("visual")
        )
        forward_button.pack(pady=20)

        back_button = Button(
            frame,
            text="Back",
            font=("Times New Roman", 20),
            command=lambda: self.show_frame("q4")
        )
        back_button.pack(pady=20)

        back_home_button = Button(
            frame,
            text="Back to Home",
            font=("Times New Roman", 20),
            command=lambda: self.reset_survey()
        )
        back_home_button.pack(pady=20)

    def create_visual_frame(self) -> None:
        frame = Frame(self.container, bg="#1210d9")
        self.frames["visual"] = frame

        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        back_button = Button(
            frame,
            text="Back to Home",
            font=("Times New Roman", 20),
            command=lambda: self.reset_survey()
        )
        back_button.pack(pady=20)

    def show_frame(self, name: str) -> None:
        """Bring the selected frame to the front."""
        frame = self.frames[name]
        frame.tkraise()

    def save_q1_answer(self, current_question: str, next_frame: str) -> None:
        """Save the user's answer, generate keywords, and move to next frame."""
        text = self.entries[current_question].get().strip()

        if text == "":
            self.q1_error_label.config(text= "Please enter a game!")
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
        game_names = read_file("medium_game_sample_300.csv")

        user_words = text.lower().replace(",", " ").replace(".", " ").split()

        keywords = []

        for i in range(len(user_words)):
            for j in range(i + 1, len(user_words) + 1):
                candidate = ''.join([clean_up_line(w) for w in user_words[i:j]])
                if candidate in game_names and candidate not in keywords:
                    keywords.append(candidate)
                    break  # take first match starting at position i
            if keywords:  # stop after first match if you only want 1 game
                break

        return keywords

    def save_q2_answers(self) -> None:
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

    def save_q3_answers(self) -> None:
        selected = []

        for genre, var in self.q3_vars.items():
            if var.get():
                selected.append(genre)

        if not selected:
            self.q3_error_label.config(text="Please select an option!")
            return

        self.q3_error_label.config(text="")

        self.answers["q3"] = {
            "keywords": selected
        }

        print(self.answers["q3"])
        self.show_frame("q4")

    def save_q4_answer(self) -> None:
        min_val = self.min_budget.get()
        max_val = self.max_budget.get()

        if min_val > max_val:
            self.q4_error_label.config(text="Min cannot be greater than Max!")
            return

        self.q4_error_label.config(text="")

        self.answers["q4"] = {
            "min": min_val,
            "max": max_val
        }

        print(self.answers["q4"])
        self.show_frame("result")

    def reset_survey(self) -> None:
        """Clear all user inputs and stored answers."""
        for entry in self.entries.values():
            entry.delete(0, "end")

        self.answers.clear()
        self.show_frame("home")

    def get_user_answers(self):
        return self.answers




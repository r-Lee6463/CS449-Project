"""CS449 Ryan Lee 3/6/25; Developed and tested in conjuncture with ChatGPT (model GPT-4o) following Google's Python Style Guide."""

import tkinter as tk
from tkinter import messagebox


class SOSGameGUI:
    """GUI for the SOS game using Tkinter."""

    def __init__(self, root):
        """Initializes the SOS game GUI."""
        self.root = root
        self.root.title("SOS Game")

        # Default board size
        self.n = 5
        self.current_player = "Blue"
        self.buttons = []

        # Player options
        self.blue_player_type = tk.StringVar(value="Human")
        self.red_player_type = tk.StringVar(value="Human")
        self.letter_choice = tk.StringVar(value="S")
        self.record_var = tk.BooleanVar()
        self.board_size_var = tk.IntVar(value=5)
        self.game_mode = tk.StringVar(value="Simple")

        self._create_widgets()

    def _create_widgets(self):
        """Creates and organizes widgets for the game."""
        self.turn_label = tk.Label(
            self.root, text=f"{self.current_player} Player's Turn", font=("Arial", 14)
        )
        self.turn_label.pack()

        # Create board size selection dropdown
        self._create_board_size_selector()
        
        # Create game mode selection
        self._create_game_mode_selector()
        
        # Create game board
        self._create_board()
        
        # Create player options (Human/Computer, S/O selection)
        self._create_player_options()

        # Checkbox for recording the game
        self.record_checkbox = tk.Checkbutton(
            self.root, text="Record Game", variable=self.record_var
        )
        self.record_checkbox.pack()

    def _create_board_size_selector(self):
        """Creates a dropdown menu to select board size."""
        size_frame = tk.Frame(self.root)
        size_frame.pack()

        tk.Label(size_frame, text="Board Size: ").pack(side=tk.LEFT)
        size_dropdown = tk.OptionMenu(
            size_frame, self.board_size_var, *range(3, 9), command=self._update_board_size
        )
        size_dropdown.pack(side=tk.LEFT)

    def _create_game_mode_selector(self):
        """Creates radio buttons to select the game mode (Simple or General)."""
        mode_frame = tk.Frame(self.root)
        mode_frame.pack()

        tk.Label(mode_frame, text="Game Mode: ").pack(side=tk.LEFT)
        tk.Radiobutton(
            mode_frame, text="Simple", variable=self.game_mode, value="Simple"
        ).pack(side=tk.LEFT)
        tk.Radiobutton(
            mode_frame, text="General", variable=self.game_mode, value="General"
        ).pack(side=tk.LEFT)

    def _update_board_size(self, size):
        """Updates the board size and resets the game."""
        self.n = int(size)
        self._create_board()

    def _create_board(self):
        """Creates the game board grid."""
        # Destroy the previous board if it exists
        if hasattr(self, "board_frame"):
            self.board_frame.destroy()
        
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # Create a 2D list of buttons for the board
        self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]

        for i in range(self.n):
            for j in range(self.n):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    width=4,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                )
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

    def _create_player_options(self):
        """Creates radio buttons for player options."""
        options_frame = tk.Frame(self.root)
        options_frame.pack()

        # Blue Player options (Human/Computer)
        tk.Label(options_frame, text="Blue Player:").grid(row=0, column=0)
        tk.Radiobutton(
            options_frame, text="Human", variable=self.blue_player_type, value="Human"
        ).grid(row=0, column=1)
        tk.Radiobutton(
            options_frame, text="Computer", variable=self.blue_player_type, value="Computer"
        ).grid(row=0, column=2)

        # Red Player options (Human/Computer)
        tk.Label(options_frame, text="Red Player:").grid(row=1, column=0)
        tk.Radiobutton(
            options_frame, text="Human", variable=self.red_player_type, value="Human"
        ).grid(row=1, column=1)
        tk.Radiobutton(
            options_frame, text="Computer", variable=self.red_player_type, value="Computer"
        ).grid(row=1, column=2)

        # Player letter choice (S or O)
        tk.Label(options_frame, text="Choose Letter:").grid(row=2, column=0)
        tk.Radiobutton(
            options_frame, text="S", variable=self.letter_choice, value="S"
        ).grid(row=2, column=1)
        tk.Radiobutton(
            options_frame, text="O", variable=self.letter_choice, value="O"
        ).grid(row=2, column=2)

    def make_move(self, row, col):
        """Handles a player's move on the board."""
        if self.buttons[row][col]["text"] == "":
            # Place the chosen letter in the selected cell
            self.buttons[row][col]["text"] = self.letter_choice.get()
            self._switch_player()
        else:
            # Warn the player if the cell is already occupied
            messagebox.showwarning("Invalid Move", "Cell already occupied!")

    def _switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"
        self.turn_label.config(text=f"{self.current_player} Player's Turn")


if __name__ == "__main__":
    root = tk.Tk()
    game = SOSGameGUI(root)
    root.mainloop()

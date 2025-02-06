"""CS449 Ryan Lee 2/5/25; Developed and tested in conjuncture with ChatGPT (model GPT-4o) following Google's Python Style Guide."""

import tkinter as tk
from tkinter import messagebox


class SOSGameGUI:
    """GUI for the SOS game using Tkinter."""

    def __init__(self, root):
        """Initializes the SOS game GUI."""
        self.root = root
        self.root.title("SOS Game")

        self.n = 5  # Default board size (can be adjusted for larger boards)
        self.current_player = "Blue"  # Blue always starts first
        self.buttons = [[None for _ in range(self.n)] for _ in range(self.n)]

        # Variables to track player types and choices
        self.blue_player_type = tk.StringVar(value="Human")
        self.red_player_type = tk.StringVar(value="Human")
        self.letter_choice = tk.StringVar(value="S")
        self.record_var = tk.BooleanVar()

        self._create_widgets()

    def _create_widgets(self):
        """Creates and organizes widgets for the game."""
        # Label to indicate which player's turn it is
        self.turn_label = tk.Label(
            self.root, text=f"{self.current_player} Player's Turn", font=("Arial", 14)
        )
        self.turn_label.pack()

        self._create_board()  # Create the game board
        self._create_player_options()  # Create player selection options

        # Checkbox to allow recording the game session
        self.record_checkbox = tk.Checkbutton(
            self.root, text="Record Game", variable=self.record_var
        )
        self.record_checkbox.pack()

    def _create_board(self):
        """Creates the game board grid."""
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack()

        # Generate buttons for each cell in the grid
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

        # Blue player type selection (Human or Computer)
        tk.Label(options_frame, text="Blue Player:").grid(row=0, column=0)
        tk.Radiobutton(
            options_frame, text="Human", variable=self.blue_player_type, value="Human"
        ).grid(row=0, column=1)
        tk.Radiobutton(
            options_frame, text="Computer", variable=self.blue_player_type, value="Computer"
        ).grid(row=0, column=2)

        # Red player type selection (Human or Computer)
        tk.Label(options_frame, text="Red Player:").grid(row=1, column=0)
        tk.Radiobutton(
            options_frame, text="Human", variable=self.red_player_type, value="Human"
        ).grid(row=1, column=1)
        tk.Radiobutton(
            options_frame, text="Computer", variable=self.red_player_type, value="Computer"
        ).grid(row=1, column=2)

        # Letter selection for moves (S or O)
        tk.Label(options_frame, text="Choose Letter:").grid(row=2, column=0)
        tk.Radiobutton(
            options_frame, text="S", variable=self.letter_choice, value="S"
        ).grid(row=2, column=1)
        tk.Radiobutton(
            options_frame, text="O", variable=self.letter_choice, value="O"
        ).grid(row=2, column=2)

    def make_move(self, row, col):
        """Handles a player's move on the board."""
        # Check if the selected cell is empty
        if self.buttons[row][col]["text"] == "":
            self.buttons[row][col]["text"] = self.letter_choice.get()
            self._switch_player()
        else:
            # Show warning if the cell is already occupied
            messagebox.showwarning("Invalid Move", "Cell already occupied!")

    def _switch_player(self):
        """Switches the turn to the other player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"
        self.turn_label.config(text=f"{self.current_player} Player's Turn")

    # TODO:
    # - Board size changer (dropdown? int input w/ cap?)
    # - Replay button + functionality
    # - New game button + functionality
    # - Simple/General game radio buttons


if __name__ == "__main__":
    """Program execution begins and ends here."""
    root = tk.Tk()
    game = SOSGameGUI(root)
    root.mainloop()

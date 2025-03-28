"""CS449 Ryan Lee 3/27/25; Developed and tested in conjuncture with ChatGPT (model GPT-4o and GPT-4o mini) following Google's Python Style Guide."""

import tkinter as tk
from tkinter import messagebox


# Base class for handling common game logic
class BaseGame:
    def __init__(self, board_size, game_mode):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [["" for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Blue"
        self.blue_points = 0
        self.red_points = 0
        self.total_moves = 0

    def reset_board(self):
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Blue"
        self.blue_points = 0
        self.red_points = 0
        self.total_moves = 0

    def switch_player(self):
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def award_points(self, points):
        """Awards points to the current player."""
        if self.current_player == "Blue":
            self.blue_points += points
        else:
            self.red_points += points

    def check_game_over(self):
        """Checks if the game is over based on the current game mode."""
        raise NotImplementedError

    def get_winner(self):
        """Determines the winner of the game."""
        raise NotImplementedError


# Specialized class for SOS game logic
class SOSGameLogic(BaseGame):
    def __init__(self, board_size, game_mode):
        super().__init__(board_size, game_mode)

    def make_move(self, row, col, letter):
        if self.board[row][col] == "":
            self.board[row][col] = letter
            self.total_moves += 1
            points_awarded = self.check_for_sos(row, col, letter)
            if points_awarded:
                self.award_points(points_awarded)
                return f"{points_awarded} SOS's formed"
            return True
        return False

    def check_for_sos(self, row, col, letter):
        """Checks if placing a letter at (row, col) forms an SOS."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        points_awarded = 0
        for dr, dc in directions:
            if self.is_sos(row, col, dr, dc, letter):
                points_awarded += 1
        return points_awarded

    def is_sos(self, row, col, dr, dc, letter):
        """Checks if an SOS pattern is formed in a specific direction."""
        try:
            if letter == "S":
                if self.board[row][col] == "S" and self.board[row + dr][col + dc] == "O" and self.board[row + 2 * dr][col + 2 * dc] == "S":
                    return True
            elif letter == "O":
                if self.board[row - dr][col - dc] == "S" and self.board[row][col] == "O" and self.board[row + dr][col + dc] == "S":
                    return True
                if self.board[row + dr][col + dc] == "S" and self.board[row][col] == "O" and self.board[row - dr][col - dc] == "S":
                    return True
        except IndexError:
            return False
        return False

    def check_game_over(self):
        """Checks if the game is over based on the current game mode."""
        if self.game_mode == "Simple":
            if self.blue_points > 0 or self.red_points > 0:
                return True
            elif self.total_moves == self.board_size ** 2:
                return True
        elif self.game_mode == "General":
            if self.total_moves == self.board_size ** 2:
                return True
        return False

    def get_winner(self):
        """Determines the winner of the game."""
        if self.game_mode == "Simple":
            if self.blue_points > 0:
                return "Blue"
            elif self.red_points > 0:
                return "Red"
            else:
                return "Draw"
        elif self.game_mode == "General":
            if self.blue_points > self.red_points:
                return "Blue"
            elif self.red_points > self.blue_points:
                return "Red"
            else:
                return "Draw"


# Base class for GUI handling
class BaseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")
        self.logic = None
        self.turn_label = None
        self.score_label = None
        self.board_frame = None

    def _create_widgets(self):
        """Create common GUI widgets like score labels, and turn labels."""
        self.turn_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.turn_label.pack()

        self.score_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.score_label.pack(pady=10)

    def _create_board(self):
        """Create the game board, to be overridden by specific games."""
        raise NotImplementedError

    def make_move(self, row, col):
        """Handles making a move, to be overridden by specific games."""
        raise NotImplementedError

    def highlight_sos(self, row, col, letter):
        """Highlights the SOS in the turn player's color, to be overridden by specific games."""
        raise NotImplementedError

    def end_game(self):
        """End game, to be overridden by specific games."""
        raise NotImplementedError


class SOSGameGUI:
    """GUI for the SOS game using Tkinter."""
    def __init__(self, root):
        self.awarded_sos = set()  # Set to track awarded SOS sequences
        self.root = root
        self.root.title("SOS Game")

        self.n = 8 # Max board size
        self.board = [["" for _ in range(self.n)] for _ in range(self.n)]  # Initialize an empty board
        self.game_mode = "Simple"
        self.logic = SOSGameLogic(self.n, self.game_mode)
        self.blue_letter_choice = tk.StringVar(value="S")
        self.red_letter_choice = tk.StringVar(value="S")
        self.board_size_var = tk.IntVar(value=5)  # Default value for board size
        self.game_mode_var = tk.StringVar(value="Simple")

        self._create_widgets()
        self._start_new_game()

    def _create_widgets(self):
        self.turn_label = tk.Label(self.root, text=f"{self.logic.current_player} Player's Turn", font=("Arial", 14))
        self.turn_label.pack()

        self._create_board_size_selector()  # Add board size selector to the GUI
        self._create_game_mode_selector()

        self.score_label = tk.Label(self.root, text=f"Blue: {self.logic.blue_points} | Red: {self.logic.red_points}", font=("Arial", 12))
        self.score_label.pack(pady=10)

        # Initialize main_frame here, before using it
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack()

        self._create_player_options("left", "Blue")
        self._create_board()
        self._create_player_options("right", "Red")

        self.new_game_button = tk.Button(self.root, text="New Game", command=lambda: [self._start_new_game(), self._start_new_game()])
        self.new_game_button.pack(pady=10)

    def _create_board_size_selector(self):
        size_frame = tk.Frame(self.root)
        size_frame.pack()
        tk.Label(size_frame, text="Board Size: ").pack(side=tk.LEFT)
        # Update this to change board size when selected
        tk.OptionMenu(size_frame, self.board_size_var, *range(3, 9)).pack(side=tk.LEFT)

    def _create_game_mode_selector(self):
        mode_frame = tk.Frame(self.root)
        mode_frame.pack()
        tk.Label(mode_frame, text="Game Mode: ").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="Simple", variable=self.game_mode_var, value="Simple").pack(side=tk.LEFT)
        tk.Radiobutton(mode_frame, text="General", variable=self.game_mode_var, value="General").pack(side=tk.LEFT)

    def _create_board(self):
        # Ensure the board size is taken from the selected value
        self.n = self.board_size_var.get()
        if hasattr(self, "board_frame") and self.board_frame is not None:
            self.board_frame.destroy()  # Only destroy if the frame already exists
        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack()
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

    def _set_game_mode(self):
        self.logic.game_mode = self.game_mode_var.get()  # Update the game mode in the logic

    def _start_new_game(self):
        """Starts a new game with a fresh board."""
        # Reset the game logic and board size
        self.logic = SOSGameLogic(self.n, self.game_mode_var.get())  # Update game logic with the new board size and mode
        self.logic.reset_board()

        # Reset the UI to reflect the new game
        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")
        self.score_label.config(text=f"Blue: {self.logic.blue_points} | Red: {self.logic.red_points}")

        # Reset all buttons on the board
        for i in range(self.n):
            for j in range(self.n):
                self.buttons[i][j].config(text="", bg="SystemButtonFace")

        # Reinitialize the board frame (if needed) to reflect the new board size
        self._create_board()

    def _create_player_options(self, side, player):
        """Create the options for each player."""
        frame = tk.Frame(self.main_frame)
        frame.pack(side=side, padx=10)
        letter_choice_var = self.blue_letter_choice if player == "Blue" else self.red_letter_choice
        tk.Label(frame, text=f"{player} Player:").pack()
        tk.Label(frame, text="Choose Letter:").pack()
        tk.Radiobutton(frame, text="S", variable=letter_choice_var, value="S").pack()
        tk.Radiobutton(frame, text="O", variable=letter_choice_var, value="O").pack()

    def make_move(self, row, col):
        letter = self.blue_letter_choice.get() if self.logic.current_player == "Blue" else self.red_letter_choice.get()
        result = self.logic.make_move(row, col, letter)
        if result:
            self.buttons[row][col]["text"] = letter
            self.highlight_sos(row, col, letter)
            self.logic.switch_player()
            self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")
            self.score_label.config(text=f"Blue: {self.logic.blue_points} | Red: {self.logic.red_points}")
            if self.logic.check_game_over():
                self.end_game()
        else:
            messagebox.showwarning("Invalid Move", "Cell already occupied!")

    def highlight_sos(self, row, col, letter):
        """Highlights the SOS in the turn player's color and awards points correctly."""
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        player_color = "blue" if self.logic.current_player == "Blue" else "red"
        claimed = "blue" if player_color == "red" else "red"

        awarded_sequences = set()

        for dr, dc in directions:
            sequence = self.find_sos_sequence(row, col, dr, dc, player_color, claimed)
            if sequence and sequence not in awarded_sequences:
                self.highlight_sequence(sequence, player_color)
                awarded_sequences.add(sequence)

    def find_sos_sequence(self, row, col, dr, dc, player_color, claimed):
        """Helper to find SOS sequences."""
        first_s_row, first_s_col = row + dr, col + dc
        second_s_row, second_s_col = row - dr, col - dc

        if self.is_valid_position(first_s_row, first_s_col) and self.is_valid_position(second_s_row, second_s_col):
            if self.is_sos_sequence(first_s_row, first_s_col, second_s_row, second_s_col, row, col, player_color, claimed):
                return frozenset([(first_s_row, first_s_col), (second_s_row, second_s_col), (row, col)])
        return None

    def is_valid_position(self, row, col):
        """Checks if a position is within board bounds."""
        return 0 <= row < self.n and 0 <= col < self.n

    def is_sos_sequence(self, s1_row, s1_col, s2_row, s2_col, row, col, player_color, claimed):
        """Checks if a sequence is SOS and matches."""
        return (
            self.board[s1_row][s1_col] == "S"
            and self.board[s2_row][s2_col] == "S"
            and self.board[row][col] == "O"
            and self.logic.current_player == claimed
        )
    
    def highlight_sequence(self, sequence, player_color):
        """Highlights the SOS sequence in color and updates it."""
        for row, col in sequence:
            self.buttons[row][col].config(bg=player_color)

    def end_game(self):
        """Ends the game and displays the winner."""
        winner = self.logic.get_winner()
        messagebox.showinfo("Game Over", f"Winner: {winner}")


if __name__ == "__main__":
    root = tk.Tk()
    game = SOSGameGUI(root)
    root.mainloop()
    

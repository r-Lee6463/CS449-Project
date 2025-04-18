"""CS449 Ryan Lee 4/17/25; Developed and tested in conjuncture with ChatGPT (o4-mini-high) following Google's Python Style Guide."""
import tkinter as tk
from tkinter import messagebox
import random


class BaseGame:
    """Handles the core SOS game logic."""
    def __init__(self, board_size, game_mode):
        self.board_size = board_size
        self.game_mode = game_mode
        self.board = [["" for _ in range(board_size)] for _ in range(board_size)]
        self.current_player = "Blue"
        self.total_moves = 0
        self.blue_points = 0
        self.red_points = 0

    def reset_board(self):
        """Resets the game state to start a new match."""
        self.board = [["" for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.current_player = "Blue"
        self.total_moves = 0
        self.blue_points = 0
        self.red_points = 0

    def switch_player(self):
        """Switches turn to the other player."""
        self.current_player = "Red" if self.current_player == "Blue" else "Blue"

    def make_move(self, row, col, letter):
        """Attempts to place a letter; returns True if successful."""
        if self.board[row][col] == "":
            self.board[row][col] = letter
            self.total_moves += 1
            sequences = self.check_for_sos(row, col)
            if sequences:
                points = len(sequences)
                if self.current_player == "Blue":
                    self.blue_points += points
                else:
                    self.red_points += points
            return True
        return False

    def check_for_sos(self, row, col):
        """Returns list of SOS sequences formed by the last move, handling both S and O placements."""
        sequences = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        letter = self.board[row][col]
        for dr, dc in directions:
            # For O placed, check S-O-S pattern
            if letter == 'O':
                r1, c1 = row - dr, col - dc
                r2, c2 = row + dr, col + dc
                if (0 <= r1 < self.board_size and 0 <= c1 < self.board_size and
                    0 <= r2 < self.board_size and 0 <= c2 < self.board_size):
                    if self.board[r1][c1] == 'S' and self.board[r2][c2] == 'S':
                        sequences.append([(r1, c1), (row, col), (r2, c2)])
            # For S placed, check both S-S-O and O-S-S
            elif letter == 'S':
                # Check O before S
                o_r, o_c = row - dr, col - dc
                s_r, s_c = row - 2*dr, col - 2*dc
                if (0 <= o_r < self.board_size and 0 <= o_c < self.board_size and
                    0 <= s_r < self.board_size and 0 <= s_c < self.board_size):
                    if self.board[o_r][o_c] == 'O' and self.board[s_r][s_c] == 'S':
                        sequences.append([(s_r, s_c), (o_r, o_c), (row, col)])
                # Check S before O
                o2_r, o2_c = row + dr, col + dc
                s2_r, s2_c = row + 2*dr, col + 2*dc
                if (0 <= o2_r < self.board_size and 0 <= o2_c < self.board_size and
                    0 <= s2_r < self.board_size and 0 <= s2_c < self.board_size):
                    if self.board[o2_r][o2_c] == 'O' and self.board[s2_r][s2_c] == 'S':
                        sequences.append([(row, col), (o2_r, o2_c), (s2_r, s2_c)])
        # Deduplicate sequences
        unique = []
        seen = set()
        for seq in sequences:
            key = tuple(sorted(seq))
            if key not in seen:
                seen.add(key)
                unique.append(seq)
        return unique

    def check_game_over(self):
        """Returns True if the game should end."""
        if self.game_mode == "Simple":
            if self.blue_points > 0 or self.red_points > 0:
                return True
            return self.total_moves == self.board_size ** 2
        return self.total_moves == self.board_size ** 2

    def get_winner(self):
        """Determines and returns the winner or 'Draw'."""
        if self.game_mode == "Simple":
            if self.blue_points > 0:
                return "Blue"
            if self.red_points > 0:
                return "Red"
            return "Draw"
        if self.blue_points > self.red_points:
            return "Blue"
        if self.red_points > self.blue_points:
            return "Red"
        return "Draw"


class SOSGameLogic(BaseGame):
    """Alias for BaseGame, used to ensure correct SOS detection in GUI."""
    pass


class SOSGameGUI:
    """GUI for the SOS game using Tkinter."""
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")

        # UI Variables
        self.board_size_var = tk.IntVar(value=5)
        self.game_mode_var = tk.StringVar(value="Simple")
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")
        self.blue_type = tk.StringVar(value="Human")
        self.red_type = tk.StringVar(value="Human")

        # Game logic and state
        self.logic = None
        self.n = 0
        self.buttons = []
        self.game_active = False

        self._create_widgets()
        self._start_new_game()

    def _create_widgets(self):
        # Turn label
        self.turn_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.turn_label.pack(pady=5)

        # Control frame
        ctrl = tk.Frame(self.root)
        ctrl.pack(pady=5)
        tk.Label(ctrl, text="Board Size:").pack(side=tk.LEFT)
        tk.OptionMenu(ctrl, self.board_size_var, *range(3, 9)).pack(side=tk.LEFT)
        tk.Label(ctrl, text="Game Mode:").pack(side=tk.LEFT, padx=(10,0))
        tk.Radiobutton(ctrl, text="Simple", variable=self.game_mode_var, value="Simple").pack(side=tk.LEFT)
        tk.Radiobutton(ctrl, text="General", variable=self.game_mode_var, value="General").pack(side=tk.LEFT)

        # Main frame: player options and board
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(pady=10)

        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side=tk.LEFT, padx=20)
        self._create_player_options(self.left_frame, "Blue")

        self.board_frame = tk.Frame(self.main_frame)
        self.board_frame.pack(side=tk.LEFT)

        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side=tk.LEFT, padx=20)
        self._create_player_options(self.right_frame, "Red")

        # New Game button
        tk.Button(self.root, text="New Game", command=self._start_new_game).pack(pady=10)

    def _create_player_options(self, parent, player):
        tk.Label(parent, text=f"{player} Player", font=("Arial",10,'bold')).pack(pady=(0,5))
        var = self.blue_letter if player=='Blue' else self.red_letter
        tk.Radiobutton(parent, text="S", variable=var, value="S").pack(anchor='w')
        tk.Radiobutton(parent, text="O", variable=var, value="O").pack(anchor='w')
        tvar = self.blue_type if player=='Blue' else self.red_type
        tk.Radiobutton(parent, text="Human", variable=tvar, value="Human").pack(anchor='w')
        tk.Radiobutton(parent, text="Computer", variable=tvar, value="Computer").pack(anchor='w')

    def _get_player_type(self, player):
        """Returns 'Human' or 'Computer' for given player."""
        return self.blue_type.get() if player == 'Blue' else self.red_type.get()

    def _start_new_game(self):
        # Initialize logic with SOSGameLogic
        self.n = self.board_size_var.get()
        self.logic = SOSGameLogic(self.n, self.game_mode_var.get())
        self.logic.reset_board()
        self.game_active = True

        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")

        # Clear board frame
        for widget in self.board_frame.winfo_children():
            widget.destroy()

        # Build new grid of buttons
        self.buttons = [[None]*self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                btn = tk.Button(self.board_frame, text="", width=4, height=2,
                                command=lambda r=i,c=j: self.make_move(r,c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        # If computer goes first, schedule its move
        if self._get_player_type(self.logic.current_player) == 'Computer':
            self.root.after(500, self._computer_move)

    def make_move(self, row, col):
        """Handles a human or computer move based on turn and type."""
        if not self.game_active:
            return
        # Lock out human during computer turn
        if self._get_player_type(self.logic.current_player) != 'Human':
            return

        player = self.logic.current_player
        letter = self.blue_letter.get() if player == 'Blue' else self.red_letter.get()
        if not self.logic.make_move(row, col, letter):
            return
        self._update_button(row, col, letter)

        if self.logic.check_game_over():
            self._end_game()
            return
        self.logic.switch_player()
        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")

        # If next is computer, schedule move
        if self._get_player_type(self.logic.current_player) == 'Computer':
            self.root.after(500, self._computer_move)

    def _update_button(self, row, col, letter):
        """Update button text and highlight any SOS sequences."""
        btn = self.buttons[row][col]
        btn.config(text=letter)
        sequences = self.logic.check_for_sos(row, col)
        for seq in sequences:
            for r, c in seq:
                color = 'blue' if self.logic.current_player == 'Blue' else 'red'
                self.buttons[r][c].config(fg=color)

    def _computer_move(self):
        """Performs a basic random move for the computer."""
        if not self.game_active:
            return
        empties = [(i, j) for i in range(self.n) for j in range(self.n)
                   if self.logic.board[i][j] == ""]
        if not empties:
            return
        row, col = random.choice(empties)
        letter = random.choice(['S', 'O'])
        self.logic.make_move(row, col, letter)
        self._update_button(row, col, letter)

        if self.logic.check_game_over():
            self._end_game()
            return
        self.logic.switch_player()
        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")
        # Chain if next is also computer
        if self._get_player_type(self.logic.current_player) == 'Computer':
            self.root.after(500, self._computer_move)

    def _end_game(self):
        """Handles end-of-game dialog and reset."""
        self.game_active = False
        winner = self.logic.get_winner()
        if winner == 'Draw':
            messagebox.showinfo("Game Over", "Game ended in a draw!")
        else:
            messagebox.showinfo("Game Over", f"{winner} Player Wins!")


if __name__ == '__main__':
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()

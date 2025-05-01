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
        """Returns list of SOS sequences formed by the last move."""
        sequences = []
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        letter = self.board[row][col]
        for dr, dc in directions:
            # O-center check
            if letter == 'O':
                r1, c1 = row - dr, col - dc
                r2, c2 = row + dr, col + dc
                if (0 <= r1 < self.board_size and 0 <= c1 < self.board_size and
                    0 <= r2 < self.board_size and 0 <= c2 < self.board_size):
                    if self.board[r1][c1] == 'S' and self.board[r2][c2] == 'S':
                        sequences.append([(r1, c1), (row, col), (r2, c2)])
            # S-centered checks
            elif letter == 'S':
                # O before S
                r_o, c_o = row - dr, col - dc
                r_s, c_s = row - 2*dr, col - 2*dc
                if (0 <= r_o < self.board_size and 0 <= c_o < self.board_size and
                    0 <= r_s < self.board_size and 0 <= c_s < self.board_size):
                    if self.board[r_o][c_o] == 'O' and self.board[r_s][c_s] == 'S':
                        sequences.append([(r_s, c_s), (r_o, c_o), (row, col)])
                # S before O
                r_o2, c_o2 = row + dr, col + dc
                r_s2, c_s2 = row + 2*dr, col + 2*dc
                if (0 <= r_o2 < self.board_size and 0 <= c_o2 < self.board_size and
                    0 <= r_s2 < self.board_size and 0 <= c_s2 < self.board_size):
                    if self.board[r_o2][c_o2] == 'O' and self.board[r_s2][c_s2] == 'S':
                        sequences.append([(row, col), (r_o2, c_o2), (r_s2, c_s2)])
        # Deduplicate
        unique, seen = [], set()
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

# Alias for clarity in GUI
class SOSGameLogic(BaseGame):
    pass

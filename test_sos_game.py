import unittest
import tkinter as tk
from sos_game_gui import SOSGameGUI


class TestSOSGameGUI(unittest.TestCase):
    def setUp(self):
        """Initialize the Tkinter root and game GUI with a 3x3 board for tests."""
        self.root = tk.Tk()
        self.game = SOSGameGUI(self.root)
        self.game.board_size_var.set(3)
        self.game._start_new_game()

    def tearDown(self):
        """Destroy the Tkinter root after each test."""
        self.root.destroy()

    def test_choose_board_size(self):
        """Board size selector updates the grid dimensions correctly."""
        self.game.board_size_var.set(6)
        self.game._start_new_game()
        self.assertEqual(self.game.n, 6)
        self.assertEqual(len(self.game.buttons), 6)
        self.assertEqual(len(self.game.buttons[0]), 6)

    def test_choose_game_mode(self):
        """Game mode selector updates correctly."""
        self.game.game_mode_var.set("General")
        self.game._start_new_game()
        self.assertEqual(self.game.game_mode_var.get(), "General")
        self.game.game_mode_var.set("Simple")
        self.game._start_new_game()
        self.assertEqual(self.game.game_mode_var.get(), "Simple")

    def test_make_move_simple(self):
        """Making a move in Simple mode places the correct letter."""
        self.game.game_mode_var.set("Simple")
        self.game._start_new_game()
        self.game.blue_letter.set("S")
        self.game.make_move(0, 0)
        self.assertEqual(self.game.buttons[0][0]["text"], "S")

    def test_make_move_general(self):
        """Making a move in General mode places the correct letter."""
        self.game.game_mode_var.set("General")
        self.game._start_new_game()
        self.game.blue_letter.set("O")
        self.game.make_move(1, 1)
        self.assertEqual(self.game.buttons[1][1]["text"], "O")

    def test_start_new_game(self):
        """Start New Game resets to selected board size and mode."""
        self.game.board_size_var.set(4)
        self.game.game_mode_var.set("General")
        self.game._start_new_game()
        self.assertEqual(self.game.n, 4)
        self.assertEqual(self.game.game_mode_var.get(), "General")

    def test_simple_game_over(self):
        """Simple mode ends when the board is full."""
        self.game.game_mode_var.set("Simple")
        self.game._start_new_game()
        # Fill every cell (all “S”)
        for i in range(self.game.n):
            for j in range(self.game.n):
                self.game.make_move(i, j)
        self.assertTrue(self.game.logic.check_game_over())

    def test_general_game_over(self):
        """General mode ends when the board is full."""
        self.game.game_mode_var.set("General")
        self.game._start_new_game()
        # Fill board without forming SOS
        for i in range(self.game.n):
            for j in range(self.game.n):
                self.game.blue_letter.set("S")
                self.game.make_move(i, j)
        self.assertTrue(self.game.logic.check_game_over())

    # ---- Computer Opponent Tests ----
    def test_computer_move_makes_progress(self):
        """Computer move reduces the number of empty cells."""
        self.game.blue_type.set("Computer")
        self.game.board_size_var.set(3)
        self.game._start_new_game()
        empties_before = sum(
            1 for i in range(self.game.n) for j in range(self.game.n)
            if self.game.logic.board[i][j] == ""
        )
        self.game._computer_move()
        empties_after = sum(
            1 for i in range(self.game.n) for j in range(self.game.n)
            if self.game.logic.board[i][j] == ""
        )
        self.assertLess(empties_after, empties_before)

    def test_human_locked_during_computer_turn(self):
        """Human cannot place a letter when it's computer's turn."""
        self.game.blue_type.set("Computer")
        self.game.board_size_var.set(3)
        self.game._start_new_game()
        # Attempt human move on computer's turn
        self.game.make_move(0, 0)
        self.assertEqual(self.game.buttons[0][0]["text"], "")

    def test_chained_computer_moves(self):
        """Two computer players make two moves in sequence without human intervention."""
        self.game.blue_type.set("Computer")
        self.game.red_type.set("Computer")
        self.game.board_size_var.set(3)
        self.game._start_new_game()
        # First computer move
        self.game._computer_move()
        # Second computer move (after turn switch)
        self.game._computer_move()
        moves_count = sum(
            1 for i in range(self.game.n) for j in range(self.game.n)
            if self.game.logic.board[i][j] != ""
        )
        self.assertGreaterEqual(moves_count, 2)


if __name__ == "__main__":
    unittest.main()

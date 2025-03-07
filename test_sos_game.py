import unittest
import tkinter as tk
from sos_game_gui import SOSGameGUI  # Ensure this module is correctly named and accessible


class TestSOSGameGUI(unittest.TestCase):
    def setUp(self):
        """Set up the test case by initializing the Tkinter root and game GUI."""
        self.root = tk.Tk()
        self.game = SOSGameGUI(self.root)

    def tearDown(self):
        """Destroy the Tkinter root after each test."""
        self.root.destroy()

    def test_choose_board_size(self):
        """Test changing the board size updates the board correctly."""
        self.game._update_board_size(6)
        self.assertEqual(self.game.n, 6, "Board size should update to 6.")
        self.assertEqual(len(self.game.buttons), 6, "Board should have 6 rows.")
        self.assertEqual(len(self.game.buttons[0]), 6, "Board should have 6 columns.")

    def test_choose_game_mode(self):
        """Test selecting a game mode updates the variable correctly."""
        self.game.game_mode.set("General")
        self.assertEqual(self.game.game_mode.get(), "General", "Game mode should be set to General.")
        self.game.game_mode.set("Simple")
        self.assertEqual(self.game.game_mode.get(), "Simple", "Game mode should be set to Simple.")

    def test_make_move_simple_game(self):
        """Test making a move in a simple game."""
        self.game.game_mode.set("Simple")
        self.game.make_move(0, 0)
        self.assertIn(self.game.buttons[0][0]["text"], ["S", "O"], "Cell should contain an S or O after a move.")

    def test_make_move_general_game(self):
        """Test making a move in a general game."""
        self.game.game_mode.set("General")
        self.game.make_move(1, 1)
        self.assertIn(self.game.buttons[1][1]["text"], ["S", "O"], "Cell should contain an S or O after a move.")


if __name__ == "__main__":
    unittest.main()

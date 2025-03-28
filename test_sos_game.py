import unittest
import tkinter as tk
from tkinter import messagebox
from sos_game_gui import SOSGameGUI  # Make sure to import your actual module here

class TestSOSGameGUI(unittest.TestCase):
    def setUp(self):
        """Set up the test case by initializing the Tkinter root and game GUI."""
        self.root = tk.Tk()
        self.game = SOSGameGUI(self.root)
        # Set the board size to 3x3 for testing
        
    def tearDown(self):
        """Destroy the Tkinter root after each test."""
        self.root.destroy()

    def test_choose_board_size(self):
        """Test changing the board size updates the board correctly."""
        # Simulating a change in board size (via the OptionMenu)
        self.game.board_size_var.set(6)  # Select board size 6
        self.game._start_new_game()  # Reinitialize the game with the new board size
        self.assertEqual(self.game.n, 6, "Board size should update to 6.")
        self.assertEqual(len(self.game.buttons), 6, "Board should have 6 rows.")
        self.assertEqual(len(self.game.buttons[0]), 6, "Board should have 6 columns.")

    def test_choose_game_mode(self):
        """Test selecting a game mode updates the variable correctly."""
        # Changing the game mode
        self.game.game_mode_var.set("General")  # Select 'General' mode
        self.game._start_new_game()  # Reinitialize the game with the selected game mode
        self.assertEqual(self.game.game_mode_var.get(), "General", "Game mode should be set to General.")

        self.game.game_mode_var.set("Simple")  # Select 'Simple' mode
        self.game._start_new_game()  # Reinitialize the game with the selected game mode
        self.assertEqual(self.game.game_mode_var.get(), "Simple", "Game mode should be set to Simple.")

    def test_make_move_simple_game(self):
        """Test making a move in a simple game."""
        self.game.game_mode_var.set("Simple")  # Set game mode to Simple
        self.game._start_new_game()  # Reinitialize the game
        self.game.make_move(0, 0)  # Make a move at (0, 0)
        self.assertIn(self.game.buttons[0][0]["text"], ["S", "O"], "Cell should contain an S or O after a move.")

    def test_make_move_general_game(self):
        """Test making a move in a general game."""
        self.game.game_mode_var.set("General")  # Set game mode to General
        self.game._start_new_game()  # Reinitialize the game
        self.game.make_move(1, 1)  # Make a move at (1, 1)
        self.assertIn(self.game.buttons[1][1]["text"], ["S", "O"], "Cell should contain an S or O after a move.")

    def test_start_new_game(self):
        """Test starting a new game with the chosen board size and game mode."""
        self.game.board_size_var.set(6)  # Set board size to 6
        self.game.game_mode_var.set("General")  # Set game mode to General
        self.game._start_new_game()  # Start a new game

        # Assert the correct board size and game mode have been applied
        self.assertEqual(self.game.n, 6, "Board size should be 6.")
        self.assertEqual(self.game.game_mode_var.get(), "General", "Game mode should be General.")

    def test_simple_game(self):
        """Test making moves in a simple game and ensuring the board is filled."""
        self.game.game_mode_var.set("Simple")  # Set game mode to Simple
        self.game._start_new_game()  # Reinitialize the game

        # Simulate moves to fill the board with 'S'
        for i in range(self.game.n):
            for j in range(self.game.n):
                # Fill each cell with 'S'
                self.game.make_move(i, j)  # Make the move at position (i, j)
                self.assertEqual(self.game.buttons[i][j]["text"], "S", 
                                f"Cell ({i}, {j}) should contain 'S' after the move.")

        # Check that the board is full of 'S'
        full_board = True
        for i in range(self.game.n):
            for j in range(self.game.n):
                if self.game.buttons[i][j]["text"] != "S":
                    full_board = False
                    break
            if not full_board:
                break

        self.assertTrue(full_board, "The board should be full with 'S'.")

    def test_general_game_over(self):
        """Test making moves in a general game and ensuring the board is filled."""
        self.game.game_mode_var.set("General")  # Set game mode to General
        self.game._start_new_game()  # Reinitialize the game

        # Simulate moves to fill the board with 'S'
        for i in range(self.game.n):
            for j in range(self.game.n):
                # Fill each cell with 'S'
                self.game.make_move(i, j)  # Make the move at position (i, j)
                self.assertEqual(self.game.buttons[i][j]["text"], "S", 
                                f"Cell ({i}, {j}) should contain 'S' after the move.")

        # Check that the board is full of 'S'
        full_board = True
        for i in range(self.game.n):
            for j in range(self.game.n):
                if self.game.buttons[i][j]["text"] != "S":
                    full_board = False
                    break
            if not full_board:
                break

        self.assertTrue(full_board, "The board should be full with 'S'.")

if __name__ == "__main__":
    unittest.main()

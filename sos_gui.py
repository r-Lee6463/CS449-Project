"""CS449 Ryan Lee 5/1/25; Developed and tested in conjuncture with ChatGPT (o4-mini-high) following Google's Python Style Guide."""
import tkinter as tk
from tkinter import messagebox
from sos_logic import SOSGameLogic  # business logic separated
import random


class Player:
    """Abstract base class for players."""
    def __init__(self, color):
        self.color = color

    def take_turn(self, gui):
        """Called by GUI when it's this player's turn."""
        raise NotImplementedError


class HumanPlayer(Player):
    """Human player: waits for GUI clicks."""
    def take_turn(self, gui):
        # No automatic action; GUI click enables move
        pass


class ComputerPlayer(Player):
    """Computer player: schedules a random move."""
    def take_turn(self, gui):
        gui.root.after(500, gui._computer_move)


class SOSGameGUI:
    """GUI for the SOS game with optional recording and replay."""
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Game")

        # UI variables
        self.board_size_var = tk.IntVar(value=5)
        self.game_mode_var = tk.StringVar(value="Simple")
        self.blue_letter = tk.StringVar(value="S")
        self.red_letter = tk.StringVar(value="S")
        self.blue_type = tk.StringVar(value="Human")
        self.red_type = tk.StringVar(value="Human")
        self.record_var = tk.BooleanVar()

        # Game state
        self.logic = None
        self.n = 0
        self.buttons = []
        self.game_active = False
        self.record_moves = []

        # Replay buffer
        self._replay_moves = []
        self._replay_index = 0

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
        tk.Checkbutton(ctrl, text="Record Game", variable=self.record_var).pack(side=tk.LEFT, padx=(10,0))
        tk.Button(ctrl, text="Replay", command=self._replay_game).pack(side=tk.LEFT, padx=(10,0))

        # Main frame: player panels and board
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
        letter_var = self.blue_letter if player=='Blue' else self.red_letter
        tk.Radiobutton(parent, text="S", variable=letter_var, value="S").pack(anchor='w')
        tk.Radiobutton(parent, text="O", variable=letter_var, value="O").pack(anchor='w')
        type_var = self.blue_type if player=='Blue' else self.red_type
        tk.Radiobutton(parent, text="Human", variable=type_var, value="Human").pack(anchor='w')
        tk.Radiobutton(parent, text="Computer", variable=type_var, value="Computer").pack(anchor='w')

    def _setup_players(self):
        """Instantiate player objects based on UI selection."""
        self.blue_player = HumanPlayer('Blue') if self.blue_type.get()=='Human' else ComputerPlayer('Blue')
        self.red_player  = HumanPlayer('Red')  if self.red_type.get()=='Human'  else ComputerPlayer('Red')

    def _start_new_game(self):
        # Initialize logic and state
        self.n = self.board_size_var.get()
        self.logic = SOSGameLogic(self.n, self.game_mode_var.get())
        self.logic.reset_board()
        self.game_active = True
        self.record_moves.clear()

        # Setup player objects
        self._setup_players()

        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")

        # Build board
        for w in self.board_frame.winfo_children():
            w.destroy()
        self.buttons = [[None]*self.n for _ in range(self.n)]
        for i in range(self.n):
            for j in range(self.n):
                btn = tk.Button(self.board_frame, text="", width=4, height=2,
                                command=lambda r=i,c=j: self.make_move(r,c))
                btn.grid(row=i, column=j)
                self.buttons[i][j] = btn

        # First player's turn
        current = self.logic.current_player
        player_obj = self.blue_player if current=='Blue' else self.red_player
        player_obj.take_turn(self)

    def make_move(self, row, col):
        """Handle a human move; ignore if not human turn or game over."""
        if not self.game_active:
            return
        current = self.logic.current_player
        player_obj = self.blue_player if current=='Blue' else self.red_player
        if not isinstance(player_obj, HumanPlayer):
            return

        letter = self.blue_letter.get() if current=='Blue' else self.red_letter.get()
        if not self.logic.make_move(row, col, letter):
            return

        # Record move
        if self.record_var.get():
            self.record_moves.append((current, letter, row, col))

        self._update_button(row, col)
        if self.logic.check_game_over():
            self._end_game()
            return

        # Switch turn
        self.logic.switch_player()
        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")
        next_obj = self.blue_player if self.logic.current_player=='Blue' else self.red_player
        next_obj.take_turn(self)

    def _update_button(self, row, col):
        btn = self.buttons[row][col]
        letter = self.logic.board[row][col]
        btn.config(text=letter)
        for seq in self.logic.check_for_sos(row, col):
            for r,c in seq:
                color = 'blue' if self.logic.current_player=='Blue' else 'red'
                self.buttons[r][c].config(fg=color)

    def _computer_move(self):
        """Perform a random move for the computer."""
        if not self.game_active:
            return
        empties = [(i,j) for i in range(self.n) for j in range(self.n)
                   if self.logic.board[i][j]==""]
        if not empties:
            return
        r,c = random.choice(empties)
        letter = random.choice(['S','O'])
        self.logic.make_move(r, c, letter)

        # Record
        if self.record_var.get():
            self.record_moves.append((self.logic.current_player, letter, r, c))

        self._update_button(r, c)
        if self.logic.check_game_over():
            self._end_game()
            return
        self.logic.switch_player()
        self.turn_label.config(text=f"{self.logic.current_player} Player's Turn")
        next_obj = self.blue_player if self.logic.current_player=='Blue' else self.red_player
        next_obj.take_turn(self)

    def _end_game(self):
        self.game_active = False
        # Write record file if needed
        if self.record_var.get() and self.record_moves:
            self._write_record_file()
        winner = self.logic.get_winner()
        if winner=='Draw':
            messagebox.showinfo("Game Over","Game ended in a draw!")
        else:
            messagebox.showinfo("Game Over",f"{winner} Player Wins!")

    def _write_record_file(self):
        """Writes recorded moves to 'sos_replay.txt'."""
        with open('sos_replay.txt','w') as f:
            f.write(f"{self.n},{self.game_mode_var.get()}\n")
            for p,l,r,c in self.record_moves:
                f.write(f"{p},{l},{r},{c}\n")

    def _replay_game(self):
        """Loads 'sos_replay.txt' and replays moves step by step."""
        try:
            with open('sos_replay.txt') as f:
                header = f.readline().strip().split(',')
                # ignore header for now
                moves = []
                for line in f:
                    p,l,r,c = line.strip().split(',')
                    moves.append((p,l,int(r),int(c)))
        except FileNotFoundError:
            return

        # Prepare board
        self.game_active = False
        for i in range(self.n):
            for j in range(self.n):
                btn = self.buttons[i][j]
                btn.config(text='', fg='black')
        self._replay_moves = moves
        self._replay_index = 0
        self._do_replay_step()

    def _do_replay_step(self):
        if self._replay_index >= len(self._replay_moves):
            return
        p,l,r,c = self._replay_moves[self._replay_index]
        btn = self.buttons[r][c]
        btn.config(text=l, fg='blue' if p=='Blue' else 'red')
        self._replay_index += 1
        self.root.after(500, self._do_replay_step)


if __name__=='__main__':
    root = tk.Tk()
    app = SOSGameGUI(root)
    root.mainloop()

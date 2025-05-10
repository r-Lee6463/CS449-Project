import random
import json
import urllib.request
from sos_logic import BaseGame


class PlayerStrategy:
    """Abstract base for move‐selection strategies."""
    def choose_move(self, board, board_size, letter_choices, player_color):
        """Return (row, col, letter)."""
        raise NotImplementedError

class RandomStrategy(PlayerStrategy):
    """Picks a random empty cell and random letter."""
    def choose_move(self, board, board_size, letter_choices, player_color):
        empties = [(r, c)
                   for r in range(board_size)
                   for c in range(board_size)
                   if board[r][c] == ""]
        row, col = random.choice(empties)
        letter = random.choice(['S', 'O'])
        return row, col, letter
    
class SmartStrategy(PlayerStrategy):
    """First try a quick SOS heuristic, then call the tuned LLM."""
    def __init__(self, model="llama3.2-vision", temp=0.3):
        self.llm = OllamaStrategy(model=model, temperature=temp)

    def choose_move(self, board, board_size, letter_choices, player_color):
        from sos_logic import BaseGame  # adjust import if needed

        logic = BaseGame(board_size, game_mode="General")
        logic.board = [row.copy() for row in board]
        empties = [(r, c) for r in range(board_size)
                          for c in range(board_size)
                          if board[r][c] == ""]

        # 1) Immediate self-SOS
        for r, c in empties:
            for letter in ['S', 'O']:
                logic.board[r][c] = letter
                if logic.check_for_sos(r, c):
                    return r, c, letter
                logic.board[r][c] = ""

        # 2) Block opponent SOS
        opponent = "Red" if player_color == "Blue" else "Blue"
        for r, c in empties:
            for letter in ['S', 'O']:
                logic.board[r][c] = letter
                logic.current_player = opponent
                if logic.check_for_sos(r, c):
                    return r, c, letter
                logic.board[r][c] = ""
        logic.current_player = player_color

        # 3) Delegate to LLM
        return self.llm.choose_move(board, board_size, letter_choices, player_color)

class OllamaStrategy(PlayerStrategy):
    """Calls your local Ollama HTTP API (OpenAI-compatible) for a move."""
    def __init__(self, model: str = "llama3.2-vision", temperature: float = 0.3, timeout: int = 30):
        self.model = model
        self.temperature = temperature
        self.timeout = timeout
        self.endpoint = "http://127.0.0.1:11434/v1/chat/completions"

    def choose_move(self, board, board_size, letter_choices, player_color):
        # Build text-board
        rows = ["".join(cell or "." for cell in row) for row in board]
        board_str = "\n".join(rows)
        system_msg = {
            "role": "system",
            "content": (
                "You are an expert SOS player. "
                "Try to make SOS when possible, block opponent SOS, "
                "and set up future SOS opportunities."
            )
        }
        user_msg = {
            "role": "user",
            "content": (
                f"SOS on a {board_size}x{board_size} board.\n"
                f"Player: {player_color}\n"
                f"Board ('.' empty):\n{board_str}\n"
                "Respond ONLY as row,col,letter."
            )
        }
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [system_msg, user_msg]
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            self.endpoint,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
                print("[Ollama] Raw response:", raw)
                parsed = json.loads(raw)
                text = parsed["choices"][0]["message"]["content"].strip().splitlines()[-1]
                r, c, letter = text.split(",")
                print(f"[Ollama] Parsed move: {r},{c},{letter}")
                return int(r), int(c), letter.strip().upper()
        except Exception as e:
            err_msg = getattr(e, "reason", e)
            print(f"[Ollama] Error talking to server: {err_msg}")
            print(f"[Ollama] Falling back to RandomStrategy.")
            return RandomStrategy().choose_move(board, board_size, letter_choices, player_color)
        
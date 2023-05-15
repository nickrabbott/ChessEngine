import chess
import random

class Game(object):
    """Game object stores the state of the chess game. It takes computer_color, and user_color as arguments to initialize the game board."""
    def __init__(self, computer_color, user_color):
        self.board = chess.Board()  
        self.last_move = ""
        self.computer = computer_color
        self.user = user_color
        self.player_turn = True

    def fen(self) -> str:
        return self.board.fen()

    def reset(self) -> None:
        self.board.reset()

    def legal_move(self, source, target) -> bool:
        move = chess.Move.from_uci(f"{source}{target}")
        return move in self.board.legal_moves

    def null_move(self, source, target) -> bool:
        return chess.Move.from_uci(f"{source}{target}").null()

    def push_move(self, source, target) -> None:
        self.board.push(chess.Move.from_uci(f"{source}{target}"))
        if self.board.is_game_over():
            return
        self.player_turn = not self.player_turn
        # Computer move:
        self.board.push(random.choice(list(self.board.legal_moves)))
        if self.board.is_game_over():
            return
        self.player_turn = not self.player_turn

if __name__ == "__main__":
    pass

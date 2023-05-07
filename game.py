import chess

# Stores the state of the game

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.engine_color = None
        self.turn = 0

    # will allow user to select color
    def set_engine_color(self, color):
        self.engine_color = color

    def reset_game(self):
        self.board.reset()

    def to_move(self, uci):
        return chess.Move.from_uci(uci)

    def legal_move(self, move):
        return move in self.board.legal_moves

    def null_move(move):
        return move.null()

    def push_move(move):
        self.board.push(move)

    def fen(self):
        return self.board.fen()

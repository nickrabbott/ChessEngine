import chess
import random

def generate_legal_moves(board):
    '''work around chess.Board.legal_moves generating a NoneType at end of legal moves'''
    for move in board.legal_moves:
        if move is not None:
            yield move

def minimax(board, depth, maxPlayer):
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return Evaluator(board).eval, None
    if maxPlayer:
        maxEvaluation = -99999
        maxMove = None
        for move in generate_legal_moves(board):
            board.push(move)
            evalboard, evalmove = minimax(board, depth-1, False)
            board.pop()
            if evalboard > maxEvaluation:
                maxMove = move
                maxEvaluation = evalboard 

        return maxEvaluation, maxMove
    
    else:
        minEvaluation = 99999
        minMove = None
        for move in generate_legal_moves(board):
            board.push(move)
            evalboard, evalmove = minimax(board, depth-1, True)
            board.pop()
            if evalboard < minEvaluation:
                minMove = move
                minEvaluation = evalboard

        return minEvaluation, minMove
    

class Evaluator():
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = 99999
    def __init__(self, board):
        self.board = board
        self.baseboard = chess.BaseBoard(self.board.board_fen())
        self.eval = self._evaluate()

    def _material(self):
        fenstr = self.board.fen()
        w = fenstr.count('P')*self.PAWN + fenstr.count('N')*self.KNIGHT + fenstr.count('B')*self.BISHOP + fenstr.count('R')*self.ROOK + fenstr.count('Q')*self.QUEEN 
        b = fenstr.count('p')*self.PAWN + fenstr.count('n')*self.KNIGHT + fenstr.count('b')*self.BISHOP + fenstr.count('r')*self.ROOK + fenstr.count('q')*self.QUEEN 
        return w - b
    
    def _centercontrol(self):
        attackw = 0.25
        occupyw = 0.5
        wattackers = (len(self.baseboard.attackers(chess.WHITE, chess.E4)) +  len(self.baseboard.attackers(chess.WHITE, chess.E5)) + len(self.baseboard.attackers(chess.WHITE, chess.D4)) + len(self.baseboard.attackers(chess.WHITE, chess.D5))) * attackw
        battackers = (len(self.baseboard.attackers(chess.BLACK, chess.E4)) +  len(self.baseboard.attackers(chess.BLACK, chess.E5)) + len(self.baseboard.attackers(chess.BLACK, chess.D4)) + len(self.baseboard.attackers(chess.BLACK, chess.D5))) * attackw
        return wattackers + battackers

    def _attackedpieces(self):
        wattackers = len([self.baseboard.attackers(chess.WHITE, square) for square in chess.SQUARES])
        battackers = len([self.baseboard.attackers(chess.BLACK, square) for square in chess.SQUARES]) 
        return wattackers - battackers

    def _ischeckmate(self):
        if self.board.is_checkmate():
            if self.board.result() == "1-0":
                return float(99999)
            elif self.board.result() == "0-1":
                return float(-99999)
        
        return 0

    def _evaluate(self):
        return self._material()*0.75 + self._centercontrol()*0.1 + self._attackedpieces()*0.15 + self._ischeckmate()

class Game(object):
    """Game object stores the state of the chess game. It takes computer_color, and user_color as arguments to initialize the game board."""
    def __init__(self, computer_color, user_color, starting_fen):
        self.board = chess.Board()
        if starting_fen is not None: self.board.set_fen(starting_fen)
        self.last_move = ""
        self.computer = computer_color
        self.user = user_color
        self.player_turn = True
        self.depth = 3

    def fen(self) -> str:
        return self.board.fen()

    def reset(self, state) -> None:
        if state is None:
            self.board.reset()
        else:
            self.board.set_fen(state)

    def legal_move(self, source, target) -> bool:
        move = chess.Move.from_uci(f"{source}{target}")
        return move in self.board.legal_moves

    def null_move(self, source, target) -> bool:
        return chess.Move.from_uci(f"{source}{target}").null()


    def push_move(self, source, target) -> None:
        promotion = None
        print("user move: ", chess.Move.from_uci(f"{source}{target}"))
        self.board.push(chess.Move.from_uci(f"{source}{target}"))
        if self.board.is_game_over():
            return Evaluator(self.board).eval
        self.player_turn = not self.player_turn
        # Computer move:
        besteval, bestmove = minimax(self.board, self.depth, False)
        print("computer move:", bestmove)
        if bestmove is not None:
            self.board.push(bestmove)
        if self.board.is_game_over():
            return Evaluator(self.board).eval
        self.player_turn = not self.player_turn
        return Evaluator(self.board).eval, promotion

    def result(self):
        if self.board.result() == "1-0":
            return f"White Wins 1-0"
        elif self.board.result() == "0-1":
            return f"Black Wins 0-1"
        elif self.board.result() == "1/2-1/2":
            return f"Draw 1/2-1/2"
        elif self.board.result() == "*":
            return f"Game in progress"




if __name__ == "__main__":
    board = chess.Board()
    Evaluator(board)

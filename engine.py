import chess
import random

def generate_legal_moves(board):
    '''
    work around chess.Board.legal_moves generating a NoneType at end of legal moves
    '''
    for move in board.legal_moves:
        if move is not None:
            yield move

def minimax_alpha_beta_pruning(board, depth, maxPlayer, alpha, beta):
    if depth == 0 or board.is_checkmate() or board.is_stalemate():
        return Evaluator(board).eval, None
    if maxPlayer:
        maxEvaluation = -99999
        maxMove = None
        for move in generate_legal_moves(board):
            board.push(move)
            evalboard, evalmove = minimax_alpha_beta_pruning(board, depth-1, False, alpha, beta)
            board.pop()
            if evalboard > maxEvaluation:
                maxMove = move
                maxEvaluation = evalboard 
            if alpha < maxEvaluation:
                alpha = maxEvaluation
            if beta <= alpha:
                break

        return maxEvaluation, maxMove
    
    else:
        minEvaluation = 99999
        minMove = None
        for move in generate_legal_moves(board):
            board.push(move)
            evalboard, evalmove = minimax_alpha_beta_pruning(board, depth-1, True, alpha, beta)
            board.pop()
            if evalboard < minEvaluation:
                minMove = move
                minEvaluation = evalboard
            if beta > minEvaluation:
                beta = minEvaluation
            if beta <= alpha:
                break

        return minEvaluation, minMove
    

class Evaluator():
    PAWN = 1
    KNIGHT = 3
    BISHOP = 3
    ROOK = 5
    QUEEN = 9
    KING = 99999

    WEIGHTS = {
            "material": 0.9,
            "center_control": 0.1,
            "opening": 0.3,
            "attacked_pieces": 0.15
    }

    def __init__(self, board):
        self.board = board
        self.baseboard = chess.BaseBoard(self.board.board_fen())
        self.eval = self._evaluate()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return (
            f"Evaluation: {self.eval}\n"
            "==========\n"
            f"Material Eval = {self._material() * self.WEIGHTS['material']}\n"
            f"Center Control = {self._centercontrol() * self.WEIGHTS['center_control']}\n"
            f"Attacked Pieces = {self._attackedpieces() * self.WEIGHTS['attacked_pieces']}\n"
            f"Opening = {self._opening() * self.WEIGHTS['opening']}"
        )
                 
    def _material(self):
        fenstr = self.board.fen()
        w = (fenstr.count('P')*self.PAWN +
             fenstr.count('N')*self.KNIGHT +
             fenstr.count('B')*self.BISHOP + 
             fenstr.count('R')*self.ROOK + 
             fenstr.count('Q')*self.QUEEN)
        b = (fenstr.count('p')*self.PAWN +
             fenstr.count('n')*self.KNIGHT +
             fenstr.count('b')*self.BISHOP +
             fenstr.count('r')*self.ROOK +
             fenstr.count('q')*self.QUEEN)
        return w - b
    
    def _centercontrol(self):
        attackw = 0.25
        occupyw = 0.5
        wattackers = (len(self.baseboard.attackers(chess.WHITE, chess.E4)) +
                      len(self.baseboard.attackers(chess.WHITE, chess.E5)) + 
                      len(self.baseboard.attackers(chess.WHITE, chess.D4)) + 
                      len(self.baseboard.attackers(chess.WHITE, chess.D5))) * attackw
        battackers = (len(self.baseboard.attackers(chess.BLACK, chess.E4)) +
                      len(self.baseboard.attackers(chess.BLACK, chess.E5)) +
                      len(self.baseboard.attackers(chess.BLACK, chess.D4)) + 
                      len(self.baseboard.attackers(chess.BLACK, chess.D5))) * attackw
        # We're in the opening
        if len(self.board.move_stack) < 10:
            return wattackers + battackers
        else:
            return 0


    def _attackedpieces(self):
        wattackers = len([self.baseboard.attackers(chess.WHITE, square) for square in chess.SQUARES])
        battackers = len([self.baseboard.attackers(chess.BLACK, square) for square in chess.SQUARES])
        return wattackers - battackers

    #'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
    # NEEDS IMPROVEMENT
    def _opening(self):
        if len(self.board.move_stack) < 10: #opening phase
            wlknight = self.board.board_fen().split('/')[7][1] == "N"
            wrknight = self.board.board_fen().split('/')[7][-2] == "N"
            wlbishop = self.board.board_fen().split('/')[7][2] == "B"
            wrbishop = self.board.board_fen().split('/')[7][-3] == "B"
            blknight = self.board.board_fen().split('/')[0][1] == "n"
            brknight = self.board.board_fen().split('/')[0][-2] == "n"
            blbishop = self.board.board_fen().split('/')[0][2] == "b"
            brbishop = self.board.board_fen().split('/')[0][-3] == "b"
            wopened = (1 - wlknight) - (1 - wrknight) - (1 - wlbishop) - (1 - wrbishop) 
            bopened = blknight + brknight + blbishop + brbishop
            return bopened - wopened
        else:
            return 0 

    def _ischeckmate(self):
        if self.board.is_checkmate():
            if self.board.result() == "1-0":
                return float(99999)
            elif self.board.result() == "0-1":
                return float(-99999)
        
        return 0

    def _evaluate(self):
        return (
                self._material() * self.WEIGHTS["material"] +
                self._centercontrol() * self.WEIGHTS["center_control"] +
                self._opening() * self.WEIGHTS["opening"] +
                self._attackedpieces() * self.WEIGHTS["attacked_pieces"] +
                self._ischeckmate() #
                )

class Game(object):
    standard_starting_fen = chess.STARTING_FEN

    """
    Game object stores the state of the chess game. 
    It takes computer_color, and user_color as arguments to initialize the game board.
    """
    def __init__(self, computer_color, user_color, starting_fen):
        self.board = chess.Board()
        if starting_fen is not None: self.board.set_fen(starting_fen)
        self.last_move = ""
        self.computer = computer_color
        self.user = user_color
        self.player_turn = True
        self.move_number = 1
        self.depth = 4 
        self.colors_switched = False 

    def switch_colors(self):
        if not self.colors_switched:
            self.computer = not self.computer
            self.user = not self.user
            self.player_turn = not self.player_turn
            self.colors_switched = not self.colors_switched
            return True
        else:
            return False

    def fen(self) -> str:
        return self.board.fen()

    def reset(self, state) -> None:
        if state is None:
            self.board.reset()
            self.move_number = 1
        else:
            self.board.set_fen(state)

    def good_move(self, source, target) -> bool:
        return self.legal_move(source, target) and not self.null_move(source, target) 

    def legal_move(self, source, target) -> bool:
        try:
            move = self.board.find_move(chess.parse_square(source), chess.parse_square(target))
            print(move in self.board.legal_moves)
        except chess.IllegalMoveError:
            return False

        return move in self.board.legal_moves

    def null_move(self, source, target) -> bool:
        return chess.Move.from_uci(f"{source}{target}").null()

    def computer_move(self) -> None:
        promotion = None
        besteval, bestmove = minimax_alpha_beta_pruning(self.board, self.depth, self.computer, -99999, 99999)
        print("computer move:", bestmove)
        if bestmove is not None:
            self.board.push(bestmove)
        if self.board.is_game_over():
            return Evaluator(self.board).eval, promotion
        if self.computer is False:
            self.move_number += 1
        self.player_turn = not self.player_turn
        return Evaluator(self.board), promotion

    def push_move(self, source, target) -> None:
        print("user move: ", chess.Move.from_uci(f"{source}{target}"))
        self.board.push(self.board.find_move(chess.parse_square(source), chess.parse_square(target)))
        if self.board.is_game_over():
            return Evaluator(selfc.board).eval
        if self.user is False:
            self.move_number += 1
        self.player_turn = not self.player_turn
        # Computer move:
        return self.computer_move()

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

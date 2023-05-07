from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import Response
import logging
import json
import chess
from game import Game

# initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format="%(asctime)s:%(name)s:%(levelname)s: %(message)s")

# initialize flask app
app = Flask(__name__)

#Starting board state
board = chess.Board()
last_move = ""

#game = Game()

# is run when a request is sent to the root
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    global board
    if request.method=='GET':
        board.reset()
        logger.info("Reset game board. Board state: {}".format(board.fen()))
        return render_template("index.html")
    if request.method=='POST':
        logger.info(request.get_json())
        return render_template("index.html")

#Handles POST including FEN string of board
#Returns board state
@app.route('/board', methods = ['GET', 'POST'])
def boardstate():
    global board
    if request.method=='GET':
        logger.info("Board state: {}".format(board.fen()))
        return json.dumps(board.fen())
    if request.method=='POST':
        global last_move
        logger.info("Prior board state: {}".format(board.fen()))
        source, target = request.get_json().split(',')
        move = chess.Move.from_uci("{}{}".format(source,target))
        if move in board.legal_moves:
            if not move.null():
                board.push(move)
                logger.info("Legal Move. New Fen: {}".format(board.fen()))
            resp = json.dumps(board.fen())
            return resp
        else:
            logger.info("Illegal move: {}{}. Fen: {}".format(source,target,board.fen()))
            resp = Response(response=board.fen(),status=418)
            return resp

# Below here silly

# @app.route('/', methods = ['GET', 'POST'])
# def homepage():
#     global game
#     if request.method=='GET':
#         game.reset_game()
#         logger.info("Reset game board. Board state: {}".format(game.fen()))
#         return render_template("index.html")
#     if request.method=='POST':
#         logger.info(request.get_json())
#         return render_template("index.html")

# @app.route('/board', methods = ['GET', 'POST'])
# def boardstate():
#     global game
#     if request.method=='GET':
#         logger.info("Board state: {}".format(game.fen()))
#         return json.dumps(board.fen())
#     if request.method=='POST':
#         global last_move
#         logger.info("Prior board state: {}".format(game.fen()))
#         source, target = request.get_json().split(',')
#         move = game.to_move(f"{source}{target}")
#         if game.legal_move(move):
#             if not game.null_move():
#                 game.push_move(move)
#                 logger.info("Legal Move. New Fen: {}".format(game.fen()))
#             resp = json.dumps(game.fen())
#             return resp
#         else:
#             logger.info("Illegal move: {}{}. Fen: {}".format(source,target,game.fen()))
#             resp = Response(response=game.fen(),status=418)
#             return resp





if __name__ == "__main__":
    app.run()

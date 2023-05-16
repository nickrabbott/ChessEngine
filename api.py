from flask import Flask
from flask import render_template
from flask import send_from_directory
from flask import request
from flask import Response
import logging
import argparse
import json
import chess
from engine import Game

parser = argparse.ArgumentParser()
parser.add_argument('--debug', type=str)
args = parser.parse_args()
print(args.debug)

# initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,format="%(asctime)s:%(name)s:%(levelname)s: %(message)s")

# initialize flask app
app = Flask(__name__)

#For now, user can only be white
game = Game(False, True, args.debug)

# is run when a request is sent to the root
@app.route('/', methods = ['GET', 'POST'])
def homepage():
    global game
    if request.method=='GET':
        game.reset(args.debug)
        logger.info("Reset game board. Board state: {}".format(game.fen()))
        return render_template("index.html")
    if request.method=='POST':
        logger.info(request.get_json())
        return render_template("index.html")

#Handles POST including FEN string of board
#Returns board state
@app.route('/board', methods = ['GET', 'POST'])
def boardstate():
    global game
    if request.method=='GET':
        logger.info("Board state: {}".format(game.fen()))
        return json.dumps(game.fen())
    if request.method=='POST':
        logger.info("Prior board state: {}".format(game.fen()))
        source, target = request.get_json().split(',')
        logger.info(f"{source}, {target}")
        if game.legal_move(source, target) and not game.null_move(source, target):
            evaluation, promotion = game.push_move(source, target)
            if promotion is not None:
                logger.info(f"Need to handle pawn promotion here in api.py\n@app.route('/board/, methods = ['GET', 'POST']\n def boardstate():")
            logger.info(f"Legal Move. New Fen: {game.fen()}. Evaluation: {evaluation}")
            resp = json.dumps(game.fen())
            if game.result() != "Game in progress" : logger.info(game.result())
            return resp
        else:
            logger.info("Illegal move: {}{}. Fen: {}".format(source,target,game.fen()))
            resp = Response(response=game.fen(),status=418)
            return resp


if __name__ == "__main__":
    app.run(port='8080', debug=True)

from controller import Controller
from rules import Game
import math


class MiniMax(Controller):

    def __init__(self):
        self.DEPTH = 3
        self.player = None

    def decideNextMove(self, board, possibleMoves):
        self.player = board.currentPlayer
        best_move = self.maxi(board, self.DEPTH)[1] # get best move, other elem of tuple is score
        return best_move

    def mini(self, board, depth):
        if(depth <= 0):
            return (self.evaluate(board), None)
        mini_moves = board.getPossibleMoves()
        best_score = math.inf
        best_move = None
        for mm in mini_moves:
            curr = self.maxi(board.getAppliedBoard(mm), depth - 1)[0]
            if(curr < best_score):
                best_score = curr
                best_move = mm
        return (best_score, best_move)

    def maxi(self, board, depth):
       if(depth <= 0):
           return (self.evaluate(board), None)
       maxi_moves = board.getPossibleMoves()
       best_score = -1*math.inf
       best_move = None
       for mm in maxi_moves:
           curr = self.mini(board.getAppliedBoard(mm), depth - 1)[0]
           if(curr > best_score):
               best_score = curr
               best_move = mm
       return (best_score, best_move)

    def evaluate(self, game):
        board = game.data
        white_players = 0
        black_players = 0
        for row in board:
            for p in row:
                if(p != None and p.color == 0):
                    white_players += 1
                elif(p != None and p.color == 1):
                    black_players += 1
        we = self.player
        if(we == 0):
            return white_players - black_players
        elif(we == 1):
            return black_players - white_players
        else:
            raise "Current player must be either black or white"



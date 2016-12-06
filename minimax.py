import Controller from controller
import math


class MiniMax(Controller):

    def __init__(self):
        self.DEPTH = 5

    def decideNextMove(self, board, possibleMoves):
        best_move = maxi(self, board, DEPTH)[1] # get best move, other elem of tuple is score 
        return best_move

    def mini(self, board, depth):
        if(depth <= 0)
            return self.evaluate(board)
        mini_moves = board.getPossibleMoves()
        best_score = math.inf
        best_move = None
        for mm in mini_moves:
            curr = maxi(board.getAppliedData(mm), depth - 1)[0]
            if(curr < best_score):
                best_score = curr
                best_move = mm
        return (best_score, best_move)

     def maxi(self, board, depth):
        if(depth <= 0)
            return self.evaluate(board)
        maxi_moves = board.getPossibleMoves()
        best_score = -1*math.inf
        best_move = None
        for mm in maxi_moves:
            curr = mini(board.getAppliedData(mm), depth - 1)[0]
            if(curr > best_score):
                best_score = curr
                best_move = mm
        return (best_score, best_move)

    def evaluate(self, game):
        board = game.getData()
        white_players = 0
        black_players = 0
        for p in board:
            if(p.type == 0):
                white_players += 1
            elif(p.type == 1):
                black_players += 1
        we = game.currentPlayer
        if(we == 0):
            return white_players - black_players
        elif(we == 1):
            return black_players - white_players
        else:
            raise "Current player must be either black or white"



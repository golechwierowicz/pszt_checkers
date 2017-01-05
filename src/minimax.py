from controller import Controller
from rules import Game
import random


class MiniMax(Controller):

    def __init__(self, depth=3):
        self.depth = depth
        self.player = None

    def decideNextMove(self, board, possibleMoves):
        assert len(possibleMoves) > 0
        random.shuffle(possibleMoves)
        self.player = board.currentPlayer
        # get best move, other elem of tuple is score
        best_move = self.maxi(board, self.depth)[1]
        return best_move

    def getBoardScore(self, board):
        self.player = board.currentPlayer
        return self.maxi(board, self.depth)[0]

    def mini(self, board, depth):
        if(depth <= 0):
            return (self.evaluate(board), None)
        mini_moves = board.getPossibleMoves()
        best_score = float('inf')
        best_move = None
        for mm in mini_moves:
            curr = self.maxi(board.getAppliedBoard(mm), depth - 1)[0]
            if(curr <= best_score):
                best_score = curr
                best_move = mm
        return (best_score, best_move)

    def maxi(self, board, depth):
        if(depth <= 0):
            return (self.evaluate(board), None)
        maxi_moves = board.getPossibleMoves()
        best_score = -1 * float('inf')
        best_move = None
        for mm in maxi_moves:
            curr = self.mini(board.getAppliedBoard(mm), depth - 1)[0]
            if(curr >= best_score):
                best_score = curr
                best_move = mm
        assert best_move in maxi_moves or len(maxi_moves) == 0
        return (best_score, best_move)

    def evaluate(self, game):
        return self.evaluate2(game)

    def getBoardScoreDelta(self, game):
        '''
        How much this state can be improved in future moves
        '''
        self.player = game.currentPlayer
        ret = self.maxi(game, self.depth)[0]
        return ret - self.evaluate2(game)

    def evaluate1(self, game):
        """
        Simple heuristic evalutation,
        Just count checkers
        """
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

    def evaluate2(self, game):
        """
        Simple heuristic evalutation,
        Count checkers with weights depending on checker type
        (normal or queen)
        """
        board = game.data
        score = [0.0, 0.0]  # score for each color
        for row in board:
            for p in row:
                if p == None:
                    continue
                score[p.color] += (1 if p.type == 0 else 2.1)

        we = self.player
        assert we in (0, 1)
        if(we == 0):
            return score[0] - score[1]
        elif(we == 1):
            return score[1] - score[0]

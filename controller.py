import random
class Controller:

    def decideNextMove(self, board, possibleMoves):
        raise 'Controller is abstract'
        pass


class AIEvolution(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


class AIMiniMax(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise


class AIRandom(Controller):

    def decideNextMove(self, board, possibleMoves):
        return random.choice(possibleMoves)


class Human(Controller):

    def decideNextMove(self, board, possibleMoves):
        # TODO: implement
        raise

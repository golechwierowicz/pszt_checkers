from collections import namedtuple
import os

# classic version
EDGE_SIZE = 8  # must be even
HOW_MANY_ROWS_OF_CHECKERS = 3  # must be smaller than EDGE_SIZE/2


Checker = namedtuple('Checker', [
    'color', 'type'
])
Move = namedtuple('Move', [
    'p1', 'p2', 'removedCheckers',
])
Move.__str__ = lambda x: (str(x.p1) + ' -> ' + str(x.p2) + (('\n  removed: ' +
                                                             ','.join(map(str, x.removedCheckers))) if len(x.removedCheckers) > 0 else ''))
Point = namedtuple('Point', [
    'r', 'c',
])
Point.__str__ = lambda x: '(' + str(x.r) + ',' + str(x.c) + ')'
Point.__add__ = lambda p1, p2: Point(p1.r + p2.r, p1.c + p2.c)
Point.__mul__ = lambda p, k: Point(p.r * k, p.c * k)


class Game:

    def __init__(self, controller1, controller2):
        self.currentPlayer = 0
        self.controller1 = controller1
        self.controller2 = controller2

        self.data = [[None for a in range(EDGE_SIZE)]
                     for b in range(EDGE_SIZE)]

        # place starting checkers
        for r in range(HOW_MANY_ROWS_OF_CHECKERS):
            for c in range(r % 2, EDGE_SIZE, 2):
                self.data[r][c] = Checker(0, 0)
            for c in range(EDGE_SIZE - 1 - (r) % 2, -1, -2):
                r1 = EDGE_SIZE - 1 - r
                self.data[r1][c] = Checker(1, 0)

    def copyDataOnly(self):
        newone = type(self)(None, None)
        # newone.__dict__.update(self.__dict__)
        newone.data = [d.copy() for d in self.data]
        return newone

    def getBoard(self):
        return self.data

    def printBoard(self):
        class col:
            PURPLE = '\033[95m'
            BLUE = '\033[94m'
            OKGREEN = '\033[92m'
            ORANGE = '\033[93m'
            FAIL = '\033[91m'
            ENDC = '\033[0m'
            BOLD = '\033[1m'
            UNDERLINE = '\033[4m'
        os.system('clear')
        print('   ', end='')
        print(col.PURPLE, end='')
        print(' '.join(map(str, range(EDGE_SIZE))))
        print(col.ENDC, end='')
        for r in range(EDGE_SIZE):
            print(col.PURPLE, end='')
            print(r, end='  ')
            print(col.ENDC, end='')
            for c in range(EDGE_SIZE):
                d = self.data[r][c]
                if type(d) == Checker:
                    if d.color == 0:
                        if d.type == 0:
                            # is queen
                            print(col.BLUE + 'W ' + col.ENDC, end='')
                        else:
                            print(col.BLUE + 'Q ' + col.ENDC, end='')
                    elif d.color == 1:
                        if d.type == 0:
                            print(col.ORANGE + 'B ' + col.ENDC, end='')
                        else:
                            print(col.ORANGE + 'Q ' + col.ENDC, end='')
                    else:
                        raise 'unknown color'
                else:
                    # empty field
                    print('. ', end='')
            print()

        print('current player:', 'W' if self.currentPlayer == 0 else 'B')
        pm = self.getPossibleMoves()
        print('possible Moves:', len(self.getPossibleMoves()))
        print('\n'.join(map(str, pm)))

    def getCheckersCount(self):
        ret = [[0, 0], [0, 0]]
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                d = self.data[r][c]
                if d != None:
                    ret[d.color][d.type] += 1
        return ret

    def getPossibleMoves(self):
        data = self.data

        def insideBoard(p):
            return (p[0] >= 0 and p[1] >= 0
                    and p[0] < EDGE_SIZE and p[1] < EDGE_SIZE)

        def empty(p):
            return insideBoard(p) and self.data[p[0]][p[1]] == None

        def findBeatingPaths(r, c):
            ret = []
            actualBeaten = []
            startingPos = Point(r, c)
            checkerType = data[r][c].type

            # just an recursive DFS
            def dfs(p):
                foundAnyPossibleBeating = False
                for delta in (Point(a, b) for a in [-1, 1] for b in [-1, 1]):
                    afterPoses = []
                    if checkerType == 0:
                        # normal checker
                        beatenPos = p + delta
                        afterPoses = [p + delta * 2]
                    else:
                        # queen
                        beatenPos = p + delta
                        found = False
                        while(insideBoard(beatenPos)):
                            d = data[beatenPos.r][beatenPos.c]
                            if d != None and d.color != self.currentPlayer:
                                found = True
                                break
                            beatenPos += delta
                        if found:
                            afterPos = beatenPos + delta
                            while(insideBoard(afterPos)):
                                d = data[afterPos.r][afterPos.c]
                                if d != None:
                                    break
                                afterPoses.append(afterPos)
                                afterPos += delta

                    for afterPos in afterPoses:
                        if (not insideBoard(beatenPos)) or (not insideBoard(afterPos)):
                            continue
                        if beatenPos in actualBeaten:
                            # already beaten checker in this path
                            continue
                        d1 = data[beatenPos.r][beatenPos.c]
                        d2 = data[afterPos.r][afterPos.c]
                        if d1 == None or d2 != None or d1.color == self.currentPlayer:
                            continue

                        # can beat
                        actualBeaten.append(beatenPos)
                        foundAnyPossibleBeating = True
                        dfs(afterPos)

                if not foundAnyPossibleBeating and len(actualBeaten) > 0:
                    ret.append(Move(startingPos, p, actualBeaten.copy()))
                    actualBeaten.pop()
                    pass
            dfs(startingPos)
            return ret

        ret = []
        for r in range(EDGE_SIZE):
            for c in range(EDGE_SIZE):
                d = data[r][c]
                if d == None:
                    continue
                if d.color != self.currentPlayer:
                    continue
                ret += findBeatingPaths(r, c)
                p1 = Point(r, c)
                if d.type == 0:
                    if d.color == 0:
                        directions = (Point(1, 1), Point(1, -1))
                    else:
                        directions = (Point(-1, 1), Point(-1, -1))
                else:
                    directions = (Point(a, b)
                                  for a in (-1, 1) for b in (-1, 1))
                for di in directions:
                    if d.type == 0:
                        p2 = p1 + di
                        if empty(p2):
                            ret.append(Move(p1, p2, ()))
                    else:
                        p2 = p1 + di
                        while empty(p2):
                            ret.append(Move(p1, p2, ()))
                            p2 += di

        if len(ret) == 0:
            return ret
        maxLen = max(len(r.removedCheckers) for r in ret)
        ret = list(filter(lambda x: len(x.removedCheckers) == maxLen, ret))
        return ret

    def applyMove(self, move):
        p1 = move.p1
        p2 = move.p2
        data = self.data
        for ch in move.removedCheckers:
            assert data[ch[0]][ch[1]] != None
            data[ch[0]][ch[1]] = None
        assert data[p1[0]][p1[1]] != None
        assert data[p2[0]][p2[1]] == None
        data[p2[0]][p2[1]] = data[p1[0]][p1[1]]
        data[p1[0]][p1[1]] = None

    def getAppliedData(self, move):
        ret = self.copyDataOnly()
        ret.applyMove(move)
        return ret.data

    # check if any checker reached end of the board
    # and evolve it into queen if it's true
    def evolveCheckers(self):
        data = self.data
        for c in range(EDGE_SIZE):
            d = data[0][c]
            if d != None and d.color == 1:
                data[0][c] = Checker(d.color, 1)

            d = data[EDGE_SIZE - 1][c]
            if d != None and d.color == 0:
                data[EDGE_SIZE - 1][c] = Checker(d.color, 1)

    def nextMove(self):
        possibleMoves = self.getPossibleMoves()
        assert len(possibleMoves) > 0
        if self.currentPlayer == 0:
            nextMove = self.controller1.decideNextMove(
                self, possibleMoves)
        else:
            nextMove = self.controller2.decideNextMove(
                self, possibleMoves)
        self.currentPlayer = not self.currentPlayer
        assert nextMove in possibleMoves
        self.applyMove(nextMove)
        self.evolveCheckers()

    def finished(self):
        # TODO: implement draw (for example if game leasts too long)
        # or AI will not be wise enough?
        return len(self.getPossibleMoves()) == 0

    def getWinner(self):
        return not self.currentPlayer

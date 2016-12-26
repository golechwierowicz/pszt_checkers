#!/bin/env pypy3


def testMatmul():
    from controllerEvolution2 import matmul
    a = [[3, 0],
         [0, 3]]
    b = [[2, 0],
         [0, 2]]
    c = [[6, 0],
         [0, 6]]
    assert c == list(map(list, matmul(a, b)))
    for r in matmul(a, b):
        print(list(r))
    print()

    a = [[3, 1],
         [0, 3]]
    b = [[1],
         [0]]
    c = [[3],
         [0]]
    assert c == list(map(list, matmul(a, b)))
    for r in matmul(a, b):
        print(list(r))
    print()

    a = [[1, 2, 3, 4]]
    b = [[1],
         [2],
         [3],
         [4]]
    c = [[sum(a * a for a in range(1, 5))]]
    assert c == list(map(list, matmul(a, b)))
    for r in matmul(a, b):
        print(list(r))
    print()

    a = [[3, 1],
         [0, 3]]
    b = [[1],
         [0]]
    c = [[1]]
    d = [[6]]
    res = matmul(matmul(matmul(a, b), c), d)
    res = list(map(list, res))
    assert res == [[18], [0]]
    for r in res:
        print(r)


##################################################################


def testStateGenerator():
    """
    Manual test for checking minimax state evalutaion
    """
    from StateGenerator import StateGenerator, LearningSetGenerator

    assert iter(StateGenerator(5)) is not None
    assert StateGenerator(5) is not None
    assert type(StateGenerator(5)) != type(None)
    print(type(StateGenerator(5)))
    print(type(iter(StateGenerator(5))))

    # for state in StateGenerator(10):
    #    state.printBoard()
    #    #print('score:',score)
    #    input()

    for state, score in LearningSetGenerator(10, depth=5):
        state.printBoard(False)
        print('score:', score)
        input()


if __name__ == '__main__':
    testMatmul()
    testStateGenerator()

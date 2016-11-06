from white_checker import WhiteChecker
from black_checker import BlackChecker
from king_checker import KingChecker

def foo():
	x = WhiteChecker(1, 2)
	y = BlackChecker(1, 1)
	z = KingChecker(5,6)
	x.move('right')
	x.move('left')
	print "x: " + str(x.position.x) + " y: " + str(x.position.y)

foo()
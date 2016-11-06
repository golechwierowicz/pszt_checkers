from base_checker import BaseChecker

class KingChecker(BaseChecker):
	"""Here we assume that the white checker is moving up the board"""
	def move(self, x, y):
		if(int(x) == int(y) and x > 0 and x < 9 and y > 0 and y < 9):
			self.position.update(x,y)
		else:
			raise ValueError("King can move only via diagonals.")

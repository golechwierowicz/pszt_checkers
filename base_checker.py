from position import Position

class BaseChecker:
	def __init__(self, x, y):
		self.position = Position(x, y)

	def move(self):
		raise NotImplementedError("Subclass must implement this method.")

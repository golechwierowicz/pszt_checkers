from base_checker import BaseChecker

class BlackChecker(BaseChecker):
	"""Here we assume that the white checker is moving up the board"""
	def move(self, direction):
		if(direction == 'right'):
			if(self.position > 7):
				raise ValueError("Cannot get out of the board.")
			
			self.position.update(self.position.x + 1, self.position.y - 1)
		elif(direction == 'left'):
			if(self.position < 1):
				raise ValueError("Cannot get out of the board.")
			
			self.position.update(self.position.x - 1, self.position.y - 1)
		else:
			raise ValueError("Direction must be either left or right")

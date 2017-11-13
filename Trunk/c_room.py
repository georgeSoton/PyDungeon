class room():

	def __init__(self, origin):
		self.origin = origin
		self.cells = [(0, 0)]

	def extend(self, cell):
		self.cells.append(cell)

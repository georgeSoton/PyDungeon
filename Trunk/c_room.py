class room():

	def __init__(self, origin):
		self.origin = origin
		self.cells = [(0, 0)]

	def extend(self, cell):
		self.cells.append(cell)

	def cell_borders(self, cell):
		up, down, left, right = (0, 0, 0, 0)

		if (cell[0], cell[1] + 1) in self.cells:
			up = 1

		if (cell[0], cell[1] - 1) in self.cells:
			down = 1

		if (cell[0] - 1, cell[1]) in self.cells:
			left = 1

		if (cell[0] + 1, cell[1]) in self.cells:
			right = 1

		return tuple([up, down, left, right])

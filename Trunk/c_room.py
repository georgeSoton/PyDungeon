class Room:

	def __init__(self, origin):
		self.coords = [origin]

	def extend(self, coord):
		self.coords.append(coord)

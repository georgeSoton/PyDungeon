import c_room
import c_cell
import string
import random


class Dungeon:
	rooms = []
	cells = {}

	@property
	def filledcells(self):
		return set(self.cells.keys())

	@staticmethod
	def neighbours(coord, diagonal=False):
		cx, cy = coord
		offsets = [(1, 0), (0, -1), (0, 1), (-1, 0)]
		if diagonal:
			offsets += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		for xoff, yoff in offsets:
				yield cx + xoff, cy + yoff

	def empty_neighbours(self, coords, diagonal=False):
		filled = self.filledcells
		neighs_flat = {val for coord in coords for val in self.neighbours(coord, diagonal=diagonal) if val not in filled}
		return neighs_flat

	def add_room(self, loc=(0, 0), size=1):
		room = c_room.Room(loc)
		self.cells[loc] = c_cell.Cell()

		for i in range(size - 1):
			if len(self.empty_neighbours(room.coords)) > 0:
				newloc = random.choice(tuple(self.empty_neighbours(room.coords)))
				self.cells[newloc] = c_cell.Cell()
				room.extend(newloc)
			else:
				break
		self.rooms.append(room)

	@property
	def bounds(self):
		coords = self.filledcells
		xmin = min([coord[0] for coord in coords])
		xmax = max([coord[0] for coord in coords])
		ymin = min([coord[1] for coord in coords])
		ymax = max([coord[1] for coord in coords])
		return (xmin, ymin, xmax, ymax)

	def coord_repr(self, coord):
		xc, yc = coord
		room = [r for r in self.rooms if coord in r.coords]
		assert(len(room) == 1)
		room = room[0]

		up, down, left, right = '', '', '', ''

		if (xc, yc + 1) in room.coords:
			up = '+   +'
		else:
			up = '+---+'

		if (xc, yc - 1) in room.coords:
			down = '+   +'
		else:
			down = '+---+'

		if (xc - 1, yc) in room.coords:
			left = ' '
		else:
			left = '|'

		if (xc + 1, yc) in room.coords:
			right = ' '
		else:
			right = '|'

		return (up, down, left, right)

	def __repr__(self):
		xmin, ymin, xmax, ymax = self.bounds
		width = xmax - xmin + 1
		height = ymax - ymin + 1

		def rebase(coord):
			xo, yo = coord
			return (xo - xmin, yo - ymin)

		output_array = [[[' ' * 5 for i in range(3)] for w in range(width)] for h in range(height)]

		for room, symbol in zip(self.rooms, string.ascii_lowercase + string.punctuation):
			for coord in room.coords:
				xr, yr = rebase(coord)
				up, down, left, right = self.coord_repr(coord)
				output_array[yr][xr] = [up, '{} {} {}'.format(left, symbol, right), down]

		output_array = reversed(output_array)

		output_string = ''

		for row in output_array:
			for ascii_row in range(len(row[0])):
				output_string += ''.join([col[ascii_row] for col in row])
				output_string += '\n'

		return output_string

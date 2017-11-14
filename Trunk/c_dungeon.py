import c_room
import itertools
import string
import random
from collections import Iterable


class dungeon():
	rooms = []

	@property
	def filledcells(self):
		return {x for room in self.rooms for x in self.room_cells_global(room)}

	@staticmethod
	def neighbours(coord, diagonal=False):
		cx, cy = coord
		offsets = [(1, 0), (0, -1), (0, 1), (-1, 0)]
		if diagonal:
			offsets += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		for xoff, yoff in offsets:
				yield cx + xoff, cy + yoff

	def empty_neighbours(self, cells, diagonal=False):
		filled = self.filledcells
		neighs_flat = {val for cell in cells for val in self.neighbours(cell, diagonal=diagonal) if val not in filled}

		return neighs_flat

	def add_room(self, loc=(0, 0), size=1):
		room = c_room.room(loc)
		for i in range(size - 1):
			if len(self.empty_neighbours(self.room_cells_global(room))) > 0:
				newloc = random.choice(tuple(self.empty_neighbours(self.room_cells_global(room))))
				room.extend(self.glob_to_loc(newloc, room))
			else:
				break
		self.rooms.append(room)

	@staticmethod
	def room_cells_global(room):
		"""
		Takes a room and returns the globalised coordinations of all the cells
		within it
		"""
		cells = room.cells

		return {dungeon.loc_to_glob(cell,room) for cell in cells}


	@staticmethod
	def loc_to_glob(cell, room):
		xo, yo = room.origin
		return cell[0] + xo, cell[1] + yo

	@staticmethod
	def glob_to_loc(cell, room):
		ox, oy = room.origin
		return cell[0] - ox, cell[1] - oy

	@property
	def bounds(self):
		cells = self.filledcells
		xmin = min([cell[0] for cell in cells])
		xmax = max([cell[0] for cell in cells])
		ymin = min([cell[1] for cell in cells])
		ymax = max([cell[1] for cell in cells])
		return (xmin, ymin), (xmax, ymax)

	def __repr__(self):
		def cell_repr(u, d, l, r, tag):
			output = ['' for i in range(3)]
			if u:
				output[0] = '·   ·'
			else:
				output[0] = '·---·'

			if d:
				output[2] = '·   ·'
			else:
				output[2] = '·---·'

			lwall, rwall = ('|', '|')

			if l:
				lwall = ' '
			if r:
				rwall = ' '

			output[1] = '{} {} {}'.format(lwall, tag, rwall)

			return output

		bounds = self.bounds
		xmin, ymin = bounds[0]
		xmax, ymax = bounds[1]

		width = xmax - xmin + 1
		height = ymax - ymin + 1

		blankbox = [' ' * 5 for i in range(3)]

		printmap = [[blankbox for i in range(width)] for j in range(height)]

		for room, symbol in zip(self.rooms, string.ascii_lowercase + string.punctuation):
			for cell in self.room_cells_global(room):
				roomrepr = room.cell_borders(self.glob_to_loc(cell, room))
				xc, yc = cell
				x_local = xc - xmin
				y_local = yc - ymin

				if self.glob_to_loc(cell, room) == (0, 0):
					printmap[y_local][x_local] = cell_repr(*roomrepr, symbol.upper())
				else:
					printmap[y_local][x_local] = cell_repr(*roomrepr, symbol)

		printmap_r = printmap[::-1]

		repr_out = ''

		for row in printmap_r:
			for i in range(len(row[0])):
				line = ''.join([item[i] for item in row])
				repr_out += line
				repr_out += '\n'
		return repr_out

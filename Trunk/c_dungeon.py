import c_room
import itertools
import string
import random
from collections import Iterable


class dungeon():
	rooms = []

	@property
	def filledcells(self):
		pass

	@filledcells.getter
	def filledcells(self):
		return tuple(itertools.chain.from_iterable([self.room_cells_global(room) for room in self.rooms]))

	@staticmethod
	def neighbours(coord, diagonal=False):
		cx, cy = coord
		offsets = [(1, 0), (0, -1,), (0, 1), (-1, 0)]
		if diagonal:
			offsets += [(1, 1), (1, -1), (-1, 1), (-1, -1)]
		for xoff, yoff in offsets:
				yield tuple([cx + xoff, cy + yoff])
		return

	def empty_neighbours(self, cells, diagonal=False):
		if not isinstance(cells[0], Iterable):
			cells = [cells]

		filled = self.filledcells
		neighs_flat = [val for cell in cells for val in self.neighbours(cell, diagonal=diagonal) if val not in filled]

		return tuple(set(neighs_flat))

	def add_room(self, loc=(0, 0), size=1):
		room = c_room.room(loc)
		for i in range(size - 1):
			newloc = random.choice(self.empty_neighbours(self.room_cells_global(room)))
			room.extend(self.global_cd_to_room(newloc, room)[0])

		self.rooms.append(room)

	@staticmethod
	def room_cells_global(room):
		"""
		Takes a room and returns the globalised coordinations of all the cells
		within it
		"""
		xo, yo = room.origin
		cells = room.cells

		return tuple(tuple([x + xo, y + yo]) for x, y in cells)

	@staticmethod
	def global_cd_to_room(cells, room):
		ox, oy = room.origin
		if not isinstance(cells[0], Iterable):
			cells = [cells]
		return tuple([(lx - ox, ly - oy) for lx, ly in cells])

	@property
	def bounds(self):
		pass

	@bounds.getter
	def bounds(self):
		cells = self.filledcells
		xmin = min([cell[0] for cell in cells])
		xmax = max([cell[0] for cell in cells])
		ymin = min([cell[1] for cell in cells])
		ymax = max([cell[1] for cell in cells])
		return tuple([(xmin, ymin), (xmax, ymax)])

	def __repr__(self):
		bounds = self.bounds
		xmin, ymin = bounds[0]
		xmax, ymax = bounds[1]

		width = xmax - xmin + 1
		height = ymax - ymin + 1

		printmap = [[' ' for i in range(width)] for j in range(height)]

		for room, symbol in zip(self.rooms, string.ascii_lowercase):
			for cell in self.room_cells_global(room):
				xc, yc = cell
				x_local = xc - xmin
				y_local = yc - ymin
				printmap[y_local][x_local] = symbol

		printmap[-ymin][-xmin] = printmap[-ymin][-xmin].upper()

		printmap_r = printmap[::-1]
		printmap_r_s = [''.join(x) for x in printmap_r]
		return '\n'.join(printmap_r_s)

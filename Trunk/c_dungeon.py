import c_room
import itertools


class dungeon():
	rooms = []

	@property
	def filledcells(self):
		pass

	@filledcells.getter
	def filledcells(self):
		return list(itertools.chain.from_iterable([self.room_cd_to_global(room) for room in self.rooms]))

	def add_room(self, loc=(0, 0)):
		self.rooms.append(c_room.room(loc))

	@staticmethod
	def room_cd_to_global(room):
		xo, yo = room.origin
		cells = room.cells

		return [tuple([x + xo, y + yo]) for x, y in cells]

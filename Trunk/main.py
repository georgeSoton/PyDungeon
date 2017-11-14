import c_dungeon
import random

dungeon = c_dungeon.dungeon()

dungeon.add_room((0, 0), random.randint(1, 10))
for i in range(35):
	start = random.choice(tuple(dungeon.empty_neighbours(dungeon.filledcells)))
	dungeon.add_room(start, random.randint(1, 10))

print(dungeon)

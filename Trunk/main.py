import c_dungeon

dungeon = c_dungeon.dungeon()

dungeon.add_room()
dungeon.add_room((1, 1))
print(dungeon.filledcells)

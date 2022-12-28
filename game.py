
""" everything is controlled through the game """

import items, classes

class Game:

	def __init__(self):
		""" player is Player object, mmaps is list of MMap objects, items is list of Items object, inventory is 
		Inventory object """

		self.set_player(classes.Player('You are the player.'))
		self.mmaps = []
		self.items = []
		self.inventory = classes.Inventory()

		self.mmap = None

	def set_player(self, player):
		""" add the Player to game """
		self.player = player
		self.player.game = self

	def add_item(self, item):
		""" add Item to game """
		if not item in self.items:
			self.items.append(item)
			item.set_game(self)

	def set_mmaps(self, mmaps):
		""" set list of mmaps """
		self.mmaps = mmaps

	def add_mmap(self, mmap, idx=None):
		""" add mmap to list of mmaps """
		if idx == None: idx = len(self.mmaps)
		self.mmaps.append(mmap)

	def set_mmap(self, mmap):
		""" set current mmap """
		self.mmap = mmap
		self.player.location = self.mmap.starting_room

		
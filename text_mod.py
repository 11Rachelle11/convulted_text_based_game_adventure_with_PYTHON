

import helpers

class Player:

	def __init__(self, description):
		self.description = description  # description of Player

	def examine(self):
		""" examine self """
		return self.description


class MMap:

	def __init__(self, name):
		self.name = name  # a string that is the name of the mmap
		self.mmap = [] # a multidimensional list with Rooms and blank spaces
		self.starting_room = None # a tuple of coordinates for the room to start at

	def __repr__(self):
		""" return mmap shown like a list """
		return str(self.mmap)

	def set_mmap(self, mmap, starting_room):
		""" add the map content to the object and choose the starting room on it """
		self.mmap = mmap

		#  get starting room from coordinates of columns and rows in tuple
		self.starting_room = starting_room

		self.xspace = len(self.mmap[0][0])
		self.yspace = len(self.mmap[0])
		self.zspace = len(self.mmap)


class Room:

	def __init__(self, name, mmap, description, exits=[], items=[], people=[]):
		self.name = name  # name as string
		self.mmap = mmap  # MMap object that room is in
		self.description = description # what room looks like
		self.exits = exits # directions in a list ex. [NORTH, DOWN]
		self.items = items  # a list of Item objects that are in room
		self.people = people # a list of People objects that are in room

	def __repr__(self):
		""" return the name of the room """
		return self.name

	def examine(self):
		""" return description, exits, items and people """
		out = self.name + '\n'
		if len(self.description) != 0:
			out += self.description + '\n'
		if len(self.exits) != 0:
			out += 'Exits: '
			for exit in self.exits:
				out += exit + ', '
			out = out[:-2] + '\n'
		if len(self.items) != 0:
			out += 'Items: '
			for item in self.items:
				out += item + ', '
			out = out[:-2] + '\n'
		if len(self.people) != 0:
			out += 'People: '
			for person in self.people:
				out += person + ', '
			out = out[:-2] + '\n'
		return out


class Inventory:

	def __init__(self, items=[]):
		self.items = items  # Items in a list

	def show(self):
		""" return inventory """

		if len(self.items) == 0:
			return "Your inventory is currently empty."

		output = 'Your inventory:\n'
		for item in self.items:
			output = output + item + '\n'
		return output[:-1]

	def add_Item(self, item):
		""" add an Item to the inventory """
		self.items.append(item)

	def remove_Item(self, item):
		""" remove Item from inventory """
		self.items.remove(item) # beware of error


class Item:

	def __init__(self, names, description, mobile=True):

		self.names = names # names as a list of possible string names
		self.description = description # description of item
		self.mobile = mobile # boolean whether item can be added to inventory


	def __repr__(self):
		""" return the first name of the item """
		return self.names[0]

	def __add__(self, other):
		""" return the name of the room added """
		return self.names[0] + other

	def __radd__(self, other):
		""" return the name of the room """
		return other + self.names[0]

	def take(self):
		""" add to inventory """


class Containers(Item):

	def __init__(self, names, description, mobile=True, items=[]):

		Parent.__init__(self, names, description, mobile)
		self.items = items  # items that the Container is holding


class Person:

	def __init__(self, names, room, description):
		self.names = names # name as a list of possible string names
		self.room = room  # Room object that Person is in
		self.description = description  # description of person



class CommandLine:

	def __init__(self):
		pass

	def take_input(self):
		""" take input """
		return input(' < ')

	def process_command(self):
		""" figure out what the command is saying """



class Game:

	def __init__(self, mmaps=[], items=[], inventory=Inventory(), player=None):

		self.player = player

		self.mmaps = mmaps # a list of mmaps in the world
		self.items = items # a list of items in the world

		self.mmap = None # the current mmap
		self.room_coords = None # the current room in coordiantes
		self.room = None

		self.inventory = inventory # the Inventory

		self.commands = {'e': self.east, 'east': self.east, 'go east': self.east, 'move east': self.east,
			'w': self.west, 'west': self.west, 'go west': self.west, 'move west': self.west,
			'n': self.north, 'north': self.north, 'go north': self.north, 'move north': self.north,
			's': self.south, 'south': self.south, 'go south': self.south, 'move south': self.south,
			'u': self.up, 'up': self.up, 'go up': self.up, 'move up': self.up, 'climb up': self.up, 
				'ascend': self.up,
			'd': self.down, 'down': self.down, 'go down': self.down, 'move down': self.down, 'descend': self.down}

	def main_loop(self, mmap):
		""" the main game loop. Before starting this, make sure mmaps, 
		items, and player are set """

		helpers.pprint(self.set_current_MMap(mmap))

		while True:
			command = self.take_input()
			helpers.pprint(self.process_command(command)())
			self.update()

	""" main loop functions """

	def take_input(self):
		""" let player input command """
		return input(' > ').lower()

	def process_command(self, command):
		""" return the right command """
		if command in self.commands:
			return self.commands[command]
		else:
			return self.dontexist

	def update(self):
		""" update events that exist indepently from the command """
		pass


	""" editing data functions """

	def add_MMap(self, name, mmap, starting_room):
		""" add a map to the world """
		self.mmaps.append(MMap(name, mmap, starting_room))

	def set_Player(self, description):
		""" set the player to a Player """
		self.player = Player(description)

	def set_current_MMap(self, mmap):
		""" set the current MMap """
		self.mmap = mmap
		return self.set_current_Room(self.mmap.starting_room)


	""" command functions """

	""" going commands """

	def east(self):
		""" move EAST"""
		if ('EAST' in self.room.exits and self.room_coords[2] != self.mmap.xspace-1 and 
				self.mmap.mmap[self.room_coords[0]][self.room_coords[1]][self.room_coords[2]+1] != None):
			new_coords = (self.room_coords[0], self.room_coords[1], self.room_coords[2]+1)
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	def west(self):
		""" move WEST"""
		if ('WEST' in self.room.exits and self.room_coords[2] != 0 and 
				self.mmap.mmap[self.room_coords[0]][self.room_coords[1]][self.room_coords[2]-1] != None):
			new_coords = (self.room_coords[0], self.room_coords[1], self.room_coords[2]-1)
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	def north(self):
		""" move NORTH"""
		if ('NORTH' in self.room.exits and self.room_coords[1] != 0 and 
				self.mmap.mmap[self.room_coords[0]][self.room_coords[1]-1][self.room_coords[2]] != None):
			new_coords = (self.room_coords[0], self.room_coords[1]-1, self.room_coords[2])
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	def south(self):
		""" move SOUTH"""
		if ('SOUTH' in self.room.exits and self.room_coords[1] != self.mmap.yspace and 
				self.mmap.mmap[self.room_coords[0]][self.room_coords[1]+1][self.room_coords[2]] != None):
			new_coords = (self.room_coords[0], self.room_coords[1]+1, self.room_coords[2])
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	def up(self):
		""" move UP"""
		if ('UP' in self.room.exits and self.room_coords[0] != self.mmap.zspace and 
				self.mmap.mmap[self.room_coords[0]+1][self.room_coords[1]][self.room_coords[2]] != None):
			new_coords = (self.room_coords[0]+1, self.room_coords[1], self.room_coords[2])
			print(new_coords)
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	def down(self):
		""" move down"""
		if ('DOWN' in self.room.exits and self.room_coords[0] != 0 and 
				self.mmap.mmap[self.room_coords[0]-1][self.room_coords[1]][self.room_coords[2]] != None):
			new_coords = (self.room_coords[0]-1, self.room_coords[1], self.room_coords[2])
			return self.set_current_Room(new_coords)
		else: return "You can't to go that way.\n"

	""" other functions"""
	def set_current_Room(self, coords):
		""" set the current Room using coordinates, only do if mmap is set """
		self.room_coords = coords
		self.room = helpers.tuple_indexing(self.room_coords, self.mmap.mmap)
		return self.room.examine()

	def dontexist(self):
		return "This command doesn't exist.\n"

			

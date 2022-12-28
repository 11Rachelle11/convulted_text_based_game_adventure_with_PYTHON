
import conditionsCommands, items

class Player(conditionsCommands.Base):

	def __init__(self, description):
		self.description = description  # description of Player
		self.game = None
		self.location = None
		self.rtrns = {}

	def __repr__(self):
		return self.description

	def examine(self):
		""" examine self """
		return self.description

	def move(self, dir):
		""" move in the direction of dir, which is either "NORTH", "SOUTH", "WEST", "EAST", "UP", 
		"DOWN" """
		if isinstance(self.location, Item): return 'You are still in the ' + self.location + '.'
		room = self.location.getRoom(dir)
		if room == None:
			return 'There is no exit.'
		self.location = room
		return room.examine()

	def get_room(self):
		""" get the room that the player is in """
		location = self.location
		while isinstance(location, items.Item):
			location = location.location
		return location


class Location(conditionsCommands.Base):

	def __init__(self, items, ID):
		self.items = items
		self.ID = ID

	def __repr__(self):
		return self.ID

	def add_item(self, item):
		self.items.append(item)

	def remove_item(self, item):
		self.items.remove(item)


class Inventory(Location):

	def __init__(self, items=[], ID='inventory'):
		Location.__init__(self, items, ID)

	def show(self):
		""" return inventory """
		if len(self.items) == 0:
			return "Your inventory is currently empty."

		output = 'Your inventory:\n'
		for item in self.items:
			if item.whole == None:
				output = output + item.ID + '\n'
		return output[:-1]


class Room(Location):

	directions = {'UP': [-1, 0, 0], 'DOWN': [1, 0, 0], 'NORTH': [0, -1, 0], 'SOUTH': [0, 1, 0], 
		'WEST': [0, 0, -1], 'EAST': [0, 0, 1]}

	def __init__(self, description, ID, exits):
		self.description = description
		self.ID = ID
		self.items = []
		self.mmap = None
		self.coords = ()
		self.exits = exits

	def examine(self):
		""" return description of the room """      
		out = self.ID + '\n'
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
				if item.whole == None:                     
					out += item.ID + ', '
			out = out[:-2]
		return out

	def getRoom(self, dir):
		""" return the room in the direction """
		idx = Room.directions[dir]
		idx[0] += self.coords[0]
		idx[1] += self.coords[1]
		idx[2] += self.coords[2]
		
		if ((idx[0] < 0 or idx[0] >= len(self.mmap.mmap)) or (idx[1] < 0 or 
				idx[0] >= len(self.mmap[self.coords[0]])) or (idx[2] < 0 or 
				idx[2] >= len(self.mmap[self.coords[0]][self.coords[1]]))):
			return None
		
		return self.mmap[idx[0]][idx[1]][idx[2]]



class MMap():

	def __init__(self, ID):
		self.ID = ID
		self.mmap = None
		self.starting_room = None

	def __getitem__(self, ud):
		""" indexes """
		return self.mmap[ud]

	def set_mmap(self, mmap, starting_room):
		""" set the three dimensional list mmap filled with rooms
		self.mmap[up/down][north/south][west/east], None is where there is no room
		starting_room is room it starts at """

		self.mmap = mmap
		self.starting_room = starting_room

		# get exits
		for ud in range(len(self.mmap)):
			for ns in range(len(self.mmap[0])):
				for we in range(len(self.mmap[0][0])):
					room = self.mmap[ud][ns][we]
					room.mmap = self
					room.coords = (ud, ns, we)



from random import choice
from helpers import do_nothing
from conditionsCommands import *

""" * * * * * * * * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * ** * """

class Item(Base):

	def __init__(self, names, location,
		description='There is nothing special about it.', takable=False, container=False, 
		openable=False, opened=False, items=[], plate = False, turnonable=False, on=None, wearable=False,
		worn=None, enterable=False, edible=False, thesmell='It has no particular smell.', button=True, 
		buttonaction=do_nothing, switchable=False, switch_val=False, switchonaction=do_nothing, 
		switchoffaction=do_nothing, whole=None, inventory_cannots=['open', 'close', 'look_inside', 'put_in', 'put_on', 'wear', 
		'eat'], location_cannots=['examine', 'turn_on', 'turn_off', 'smell', 'press', 'flip', 'enter', 'exit']):

		# names
		self.names = names + list(map(lambda name: 'the ' + name , names))
		self.ID = self.names[0]

		# associations
		self.location = location # location object
		self.location.add_item(self)
		self.game = None

		# attributes
		self.description = description
		self.takable = takable
		self.container = container
		self.openable = openable
		self.opened = opened
		self.plate = plate
		self.items = []
		self.plate_items = []
		self.turnonable = turnonable
		self.on = on
		self.wearable = wearable
		self.worn = worn
		self.enterable = enterable
		self.edible = edible
		self.thesmell = thesmell
		self.button = button
		self.buttonaction = buttonaction
		self.switchable = switchable
		self.switch_val = switch_val
		self.switchonaction = switchonaction
		self.switchoffaction = switchoffaction
		self.whole = whole
		self.components = []

		if self.whole != None:
			self.takable = False
			self.whole.components.append(self)

		self.exextensions = []

		# return statements
		self.retrns = {
			'take': 'You take it.', 'drop': 'You drop it.', 'close': 'You close it.', 'turn_on': 'You turn it on.',  
			'turn_off': 'You turn it off.', 'wear': 'You wear it.', 'take_off': 'You take it off.', 
			'eat': 'You eat it.', 'smell': lambda: self.thesmell, 'enter': 'You are now in it.', 
			'exit': 'You are no longer in it.'}

		# cannot do if
		self.inventory_cannots = inventory_cannots # cannot use these functions unless item is in inventory
		self.location_cannots = location_cannots # cannot use these functions unless item is in same location as player
		# or item is in an open container in the same room

	def __str__(self):
		""" return name """
		return self.ID

	def set_game(self, game):
		""" set game to game """
		self.game = game

		not_in_inventory = make_decorator(lambda: not self.location == self.game.inventory, 'It is not in your inventory.')
		multiwrap({self: self.inventory_cannots}, not_in_inventory)
		not_in_location = make_decorator(lambda: not (self.get_room() == self.game.player.get_room() or 
			self.get_room() == self.game.inventory) or (isinstance(self.location, Item) and self.location.openable and 
			not self.location.opened), "You can't see that here!")
		multiwrap({self: self.location_cannots}, not_in_location)

	def get_room(self):
		""" get the room the the item is in """
		location = self.location
		while isinstance(location, Item):
			location = location.location
		return location

	def examine(self):
		""" return description """
		out = self.description
		for ex in self.exextensions:
			out += ' ' + ex
		return out

	def take(self):
		""" take item """
		if self.game == None or not self.takable: return choice(Item.cannot_phrases)
		if self.location == self.game.inventory: return 'You already have it.'
		self.location.remove_item(self)
		self.location = self.game.inventory
		self.game.inventory.add_item(self)
		for c in self.components:
			c.take()
		self.exextensions = []
		return 'You take it.'

	def drop(self):
		""" drop item in room """
		if self.game == None or not self.takable: return choice(Item.cannot_phrases)
		if self.location != self.game.inventory: return 'It is not in your inventory.'
		self.game.inventory.remove_item(self)
		self.location = self.game.player.location
		self.game.player.location.add_item(self)
		for c in self.components:
			c.drop()
		return 'You drop it.'

	def open(self):
		""" open item """
		if not self.container or not self.openable: return choice(Item.cannot_phrases)
		if self.opened: return 'It is already opened.'
		self.opened = True
		return 'You open it.', self.look_inside

	def close (self):
		""" close item """
		if not self.container or not self.openable: return choice(Item.cannot_phrases)
		if not self.opened: return 'It is already closed.'
		self.opened = False
		return self.retrns['close']

	def look_inside(self):
		""" returns items """
		if (not self.container) or self.items == None: return choice(Item.cannot_phrases)
		if self.openable and not self.opened: return 'It is not opened.'
		if len(self.items) == 1:
			return 'Inside there is a:', self.items
		if len(self.items) > 1:
			return 'Inside there are:', self.items
		return 'There is nothing inside.'

	def add_item(self, item):
		""" add item to items """
		if not self.container: return choice(Item.cannot_phrases)
		self.items.append(item)

	def remove_item(self, item):
		""" remove item from items """
		if not self.container or not item in self.items: return choice(Item.cannot_phrases)
		self.items.remove(item)

	def put_in(self, item):
		""" put self in a container Item """
		if self in item.items: return 'The item is already in it.'
		if not item.container: return choice(Item.cannot_phrases)
		if not item.opened: return 'It is not open.'

		item.add_item(self)
		self.location.remove_item(self)
		self.location = item
		return 'You put the item in it.'

	def put_on(self, item):
		""" put self on item that is a plate """
		if self in item.plate_items: return 'The item is already on it.'
		if not item.plate: return choice(Item.cannot_phrases)
		if item.location == item.game.inventory: return 'You must drop it.'
		item.plate_items.append(self)
		item.exextensions.append('The ' + self.ID + ' is on it.')
		return 'You put the item on it.'
	
	def turn_on(self):
		""" turn on """
		if not self.turnonable: return choice(Item.cannot_phrases)
		if self.on: return 'It is already on.'
		self.on = True
		return self.retrns['turn_on']

	def turn_off(self):
		""" turn off """
		if not self.turnonable: return choice(Item.cannot_phrases)
		if not self.on: return 'It is already off.'
		self.on = False
		return self.retrns['turn_off']

	def wear(self):
		""" wear """
		if not self.wearable: return choice(Item.cannot_phrases)
		if self.worn: return 'You are already wearing it.'
		self.worn = True
		return self.retrns['wear']


	def take_off(self):
		""" take off """
		if self.wearable and self.worn:
			self.worn = False
			return self.retrns['take_off']
		else:
			return 'You are not wearing it.'

	def eat(self):
		""" eat """
		if not self.edible: return choice(Item.cannot_phrases)
		# put in invisible room coming soon
		return self.retrns['eat']

	def smell(self):
		""" smell """
		return self.retrns['smell']

	def press(self):
		""" push if a button """
		if not self.button: 'Return nothing happens.'
		return self.buttonaction()

	def flip(self):
		""" flip if switch """
		if not self.switchable: return choice(Item.cannot_phrases)
		if self.switch_val:
			self.switch_val = False
			return self.switchoffaction()
		else:
			self.switch_val = True
			return self.switchonaction()
	
	def enter(self):
		""" player enters the object """
		if not (self.enterable and self.container): return choice(Item.cannot_phrases)
		if self.game.player.location == self: return 'You are already in it.'
		self.game.player.location = self
		self.add_item(self.game.player)
		return self.retrns['enter']

	def exit(self):
		""" player enters the object """
		if not (self.enterable and self.container): return choice(Item.cannot_phrases)
		if self.game.player.location != self: return 'You are not in it.'
		self.game.player.location = self.location
		self.remove_item(self.game.player)
		return self.retrns['exit']



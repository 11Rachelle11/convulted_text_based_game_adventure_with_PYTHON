
import items, classes, game
from helpers import pprint
from conditionsCommands import *

myGame = game.Game()
i = myGame.inventory

player = classes.Player('You are Arthur Dent.')
player.add_attr('can_see', False)
myGame.set_player(player)

myRoom = classes.Room('This is a room with a bunch of random stuff.', 'My Room', ['SOUTH'])
anotherRoom = classes.Room('This is an empty room. Nothing particularly interesting or special about it.', 'Empty Room',
	['NORTH'])

myHouse = classes.MMap('House')
myHouse.set_mmap(	[[[myRoom],
					  [anotherRoom]]
				 	], myRoom)

myGame.add_mmap(myHouse)
myGame.set_mmap(myHouse)

def turn_on_light(self):
	rtrn = items.Item.turn_on(self)
	if rtrn == self.retrns['turn_on']:
		player.can_see = True
	return rtrn

def turn_off_light(self):
	rtrn = items.Item.turn_off(self)
	if rtrn == self.retrns['turn_off']:
		player.can_see = False
	return rtrn

light = items.Item(['lamp', 'light'], myRoom, 'It is a yellow lamp with a switch on it.', takable=True, turnonable=True,
	on=False)
light.modify_method('turn_on', turn_on_light, 'It turns on. You can see.')
light.modify_method('turn_off', turn_off_light, 'It turns off. You can no longer see.')
myGame.add_item(light)


switch = items.Item(['switch', 'light switch'], myRoom, takable=False, switchable=True, switch_val=False, 
	switchoffaction=light.turn_off, switchonaction=light.turn_on, whole=light)
myGame.add_item(switch)

def frost(self):
	if cake.frosted: return 'The cake is already frosted.'
	cake.frosted = True
	cake.description = 'It is chocolate cake with frosting on it.'
	return 'You frost the cake.'

cake = items.Item(['cake', 'chocolate cake'], myRoom, 'It is chocolate cake with no frosting on it.', takable=True, edible=True, 
	thesmell='It smells chocolatey and delicious.')
cake.add_attr('frosted', False)
cake.add_method('frost', frost)
myGame.add_item(cake)

box = items.Item(['box'], myRoom, 'It is a wooden box.', takable=True, container=True, openable=True, opened=False, 
	plate=True)
myGame.add_item(box)

shirt = items.Item(['shirt', 't-shirt'], box, 'It is a white t-shirt with red stripes.', takable=True, wearable=True)
myGame.add_item(shirt)

# def cannot_see(func, *args, **kwargs):
# 	def wrapper(*args, **kwargs):
# 		if not player.can_see:
# 			return 'You try, but you cannot see anything.'
# 		return func(*args, **kwargs)
# 	return wrapper

cannot_see = make_decorator(lambda: not player.can_see, 'You try, but you cannot see anything.')

multiwrap({light: ['examine', 'put_on', 'take'], cake: ['examine', 'frost', 'eat', 'put_on', 'take'], 
	box: ['examine', 'open', 'close', 'take'],  shirt: ['examine', 'wear', 'take_off', 'put_on', 'take'], myRoom: ['examine'], 
	player: ['move']}, cannot_see)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

pprint(light.turn_on())
pprint(shirt.examine())
pprint(box.take())
pprint(box.open())
pprint(shirt.examine())


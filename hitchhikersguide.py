
import items, classes, game
from helpers import pprint, do_nothing
from conditionsCommands import make_decorator, multi_wrap

myGame = game.Game()
player = classes.Player('You are Arthur Dent.')

bedroom = classes.Room('You are in the bed. The bedroom is a mess.\nIt is a small bedroom with a faded carpet and old wallpaper. '
	'There is a washbasin, a chair with a tatty dressing gown slung over it, and a window with the curtains drawn. Near the exit '
	'leading south is a phone. There is a flathead screwdriver here. There is a toothbrush here.', 'Bedroom', ['SOUTH'])

MMap = classes.MMap('Part One')
MMap.set_mmap([[[bedroom]]], bedroom)
myGame.add_mmap(MMap)
myGame.set_mmap(MMap)

light = items.Item(['light', 'lamp'], bedroom, turnonable=True, on=False)
myGame.add_item(light)
light.retrns['turn_on'] = "Good start to the day. Pity it's going to be the worst one of your life. The light is now on."

def exit_bed(self):
	retrn = items.Item.exit(self)
	if retrn == self.retrns['exit']:
		self.exextensions = []
	return retrn

bed = items.Item(['bed'], bedroom, 'It is empty.', container=True, enterable=True)
myGame.add_item(bed)
bed.enter()
bed.modify_method('enter', lambda self: 'Useless. Utterly useless.')
bed.modify_method('exit', exit_bed)
bed.exextensions.append('Except for you.')
print(bed.exextensions)

too_dark = make_decorator(lambda: light.off, 'You cannot see.')
multi_wrap({light: ['examine'], bedroom: ['examine'], bed: ['examine', 'exit', 'enter', 'take']}, too_dark)


pprint("You wake up. The room is spinning very gently round your head. Or at least it would be if you could see, which you "
	"can't.")
pprint('It is pitch black.')

pprint(bed.examine())
pprint(bed.exit())
pprint(bed.enter())
pprint(bed.examine())
pprint(bed.take())

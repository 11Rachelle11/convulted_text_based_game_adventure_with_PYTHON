
def pprint(text, space=True):
	""" print with an enter on top """

	if space: print()

	if isinstance(text, list) or isinstance(text, tuple):
		for item in text:
			pprint(item, False)

	elif callable(text):
		pprint(text(), False)

	else:
		print(text)


def tuple_indexing(t, l):
	""" given a tuple with three numbers index a list """
	return l[t[0]][t[1]][t[2]]


def do_nothing(*args, **kwargs):
	""" do nothing"""
	pass

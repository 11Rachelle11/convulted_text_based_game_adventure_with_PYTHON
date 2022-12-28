
import helpers
from random import choice
from types import MethodType

class Base:

	cannot_phrases = ['That is impossible.', 'Nice try.', 'Not likely.', 'Good luck.', "I don't think so."]

	def add_attr(self, name, value):
		""" add or modify an attribute in a base given the name of the attribute and its value """
		setattr(self, name, value)

	def modify_method(self, name, func, retrn=None):
		""" add a method given the name of the method, the function, and the arguments not including self"""
		setattr(self, name, MethodType(func, self))
		if retrn != None and hasattr(self, 'retrns'):
			self.retrns[name] = retrn

	def add_method(self, name, func):
		"""  modify a method given the name of the method, the function, and the arguments not including self"""
		setattr(self, name, MethodType(func, self))

def make_decorator(condition, retrn):
	""" condition is a function """
	def decorator(func, *args, **kwargs):
		def wrapper(*args, **kwargs):
			if condition(): return retrn
			return func()
		return wrapper
	return decorator

def multiwrap(funcs, wrap):
	""" given a dictionary of objects and their methods, wrap them all """
	for obj in funcs:
		for method in funcs[obj]:
			setattr(obj, method, wrap(getattr(obj, method)))






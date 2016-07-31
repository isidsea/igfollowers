from multiprocessing import Manager
import copy

class StateManager(object):

	def __init__(self):
		self.global_var = {}
		self.manager 	= Manager()
		self.state 		= self.manager.dict()

	def add_state(self, key=None, value=None):
		assert key   is not None, "key is not defined."
		self.state.update({key:value})

	def get_state(self, key=None):
		assert key is not None, "key is not defined."
		return self.state[key]

	def update_state(self, key=None, value=None):
		self.add_state(key,value)

	def add_global_var(self, key=None, value=None):
		assert key   is not None, "key is not defined."
		self.global_var.update({key:value})

	def get_global_var(self, key=None):
		assert key is not None, "key is not defined."
		return self.global_var[key]
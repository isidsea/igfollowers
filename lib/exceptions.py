class TooManyDuplicate(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindElements(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotFindAccount(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class CannotLogin(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class DuplicateFollower(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
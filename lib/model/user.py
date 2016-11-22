class User:
	def __init__(self, **kwargs):
		self.username 	  = kwargs.get("username", None)
		self.link     	  = kwargs.get("link", None)
		self.display_name = kwargs.get("display_name", None)

	def to_dict(self):
		return {
			"username": self.username,
			"user_link": self.link,
			"display_name": self.display_name
		}
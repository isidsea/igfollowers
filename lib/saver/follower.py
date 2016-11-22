from ..exceptions import DuplicateFollower
import pymongo
import arrow
import re

class FollowerSaver:
	def __init__(self, **kwargs):
		self.account = kwargs.get("account", None)

	def save(self, follower=None):
		""" Exceptions:
			- AssertionError
			- DuplicateFollower
		"""
		assert self.account is not None, "account is not defined."
		assert follower     is not None, "follower is not defined."

		account = {
			"username": self.account["userName"],
			"display_name": self.account["displayName"],
			"user_link": self.account["url"],
			"logsdisplay_name": "test"
		}

		conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
		db   = conn["ig"]

		db.data.create_index("followers.username", background=True)
		docs = db.data.find({"followers.username": re.compile(follower["username"], re.IGNORECASE)})

		if docs.count() == 0:
			follower.update({"_insert_time": arrow.utcnow().datetime})
			db.data.update(
				{"username": re.compile(account["username"], re.IGNORECASE)}, 
				{"$set":account, "$push":{
					"followers": follower
				}},
				upsert=True
			)
			conn.close()
		else:
			conn.close()
			raise DuplicateFollower("This %s has already have %s follower" % (account["username"], follower["username"]))
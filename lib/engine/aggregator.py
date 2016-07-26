from pymongo  import MongoClient
from ..       import tools
from ..logger import Logger
import pymongo
import copy

class Engine(object):
	def __init__(self):
		""" This function will create a fresh users collection in the database
		"""
		self.logger          = Logger()
		self.logger.app_name = "user_aggregation"

		self.db = MongoClient("mongodb://220.100.163.132:27017/test")
		self.db = self.db.ig
		self.db.users.drop()
		tools._force_create_index(db=self.db, collection="users", field="username")		

	def aggregate_user(self):
		""" This function will aggregating all followers list in database.
			In short, this is User perspective follower list. Not an Official account perspecitve.
		"""
		assert self.db is not None, "db is not defined"
		
		self.logger.write("Fetching Instragram data...")
		tools._force_create_index(db=self.db, collection="users", field="username")
		data = self.db.data.find({},{"username":1,"followers":1}).batch_size(100)

		for datum in data:
			self.logger.write("[{}] Processing...".format(datum["username"]))

			followers          = copy.deepcopy(datum["followers"])
			total_followers    = len(followers)

			del datum["followers"]
			following_document = copy.deepcopy(datum)

			self.logger.write("[{}] Number of followers: {}".format(datum["username"], total_followers))
			for user in followers:
				try:
					user.update({"following":[]})
					self.db.users.insert(user)
				except pymongo.errors.DuplicateKeyError:
					pass
				# Find duplicate following in this username
				duplicate = [following for following in self.db.users.find({
					"username":user["username"],
					"following.username":following_document["username"]	
				})]
				duplicate = (len(duplicate)>0)
				if not duplicate:
					self.db.users.update_one(
						{"username":user["username"]},
						{"$push":{"following":following_document}}
					)
			self.logger.write("[{}] Processed...".format(datum["username"]))
	#end def
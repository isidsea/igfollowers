from pymongo          import MongoClient
from ..instagram.user import User
from ..               import tools
import arrow
import pymongo

class Engine(object):
	def __init__(self, user=None):
		assert user          is not None, "user is not defined."
		assert type(user)    is dict    , "user should be a dict."
		assert "url"         in user    , "url is not defined."
		assert "userName"    in user    , "userName is not defined."
		assert "displayName" in user    , "displayName is not defined."
		
		# Connecting to database
		self._connect()

		self.account_detail = {
		       "user_link" : user["url"],
		        "username" : user["userName"],
		    "display_name" : user["displayName"],
		       "followers" : [],
		            "logs" : []
		}

		# insert basic user information if user haven been added
		try:
			self.db.data.insert_one(self.account_detail)
		except pymongo.errors.DuplicateKeyError:
			pass

		print("[igfollowers] Indexing...")
		tools._force_create_index(
			        db = self.db,
			collection = "data",
			     field = "username"
		)

	def _connect(self):
		print("[igfollowers] Connecting to database...")
		self.db = MongoClient("mongodb://mongo:27017")
		self.db = self.db.ig

	def delete(self, follower=None):
		success = False
		while not success:
			try:
				assert self.db        is not None, "db is not defined."
				assert follower       is not None, "follower is not defined."
				assert type(follower) is dict    , "follower should be an dict."

				log = 	{
							       "type" : "unfollow",
							   "username" : follower["username"],
							"insert_date" : arrow.utcnow().datetime
						}


				self.db.data.update_one(
					{"username":self.account_detail["username"]},
					{
						"$pull":{"followers":follower},
						"$push":{"logs":log}
					}
				)
				success = True
			except AssertionError:
				# Force exit looping even if the assertion is not satisfied.
				print("[igfollowers] Assertion is not satisfied.")
				success = True
			except pymongo.errors.AutoReconnect:
				self._connect()
			except:
				raise
			#end try
	#end def

	def save(self, follower=None):
		success = False
		while not success:
			try:
				assert self.db        is not None, "db is not defined."
				assert follower       is not None, "follower is not defined."
				assert type(follower) is dict    , "follower should be an dict."

				log      = {
								       "type" : "follow",
								   "username" : follower["username"],
								"insert_date" : arrow.utcnow().datetime
						   }

				# check if any duplicate data on followers
				old_data = self.db.data.find_one({"username":self.account_detail["username"]})
				old_data = old_data["followers"]
				if follower not in old_data:
					self.db.data.update_one(
						{"username":self.account_detail["username"]},
						{"$push":{"followers":follower, "logs":log}}
					)                
				#end if
				success = True
			except AssertionError:
				print("[igfollowers] Assertion is not satisfied.")
				success = True
			except pymongo.errors.AutoReconnect:
				self._connect()
			#end try
	#end def

	def get_user(self, username=None):
		assert username is not None, "username is not defined."
		assert self.db  is not None, "db is not defined."

		print("[igfollowers] Getting users from database...")
		result         = [document for document in self.db.data.find({"username":username})]
		result         = result[0] # TODO: check if result is less than 0
		user           = User(username=username)
		user.crawl     = False
		user.followers = result["followers"]
		return user
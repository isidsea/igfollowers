from pymongo         import MongoClient
from .instagram.user import User
from .               import tools
import arrow

class Engine(object):
	def __init__(self, user=None):
		assert user          is not None, "user is not defined."
		assert type(user)    is dict    , "user should be a dict."
		assert "url"         in user    , "url is not defined."
		assert "userName"    in user    , "userName is not defined."
		assert "displayName" in user    , "displayName is not defined."
		
		self.db = MongoClient("mongodb://mongo:27017")
		self.db = self.db.ig

		self.account_detail = {
		       "user_link" : user["url"],
		        "username" : user["userName"],
		    "display_name" : user["displayName"],
		       "followers" : [],
		            "logs" : []
		}

		# insert basic user information if user haven been added
		old_data = [document for document in self.db.data.find({"username":self.account_detail["username"]})]
		if len(old_data) == 0: self.db.data.insert(self.account_detail)

		tools._force_create_index(
			        db = self.db,
			collection = "data",
			     field = "followers.username"
		)

	def delete(self, follower=None):
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
		except AssertionError:
			print("[igfollowers] Assertion is not satisfied.")
		#end try


	def save(self, follower=None):
		try:
			assert self.db        is not None, "db is not defined."
			assert follower       is not None, "follower is not defined."
			assert type(follower) is dict    , "follower should be an dict."

			# check if any duplicate data on followers
			old_data = [follower for follower in self.db.data.find({"followers.username":follower["username"]})]
			log      = {
							       "type" : "follow",
							   "username" : follower["username"],
							"insert_date" : arrow.utcnow().datetime
					   }

			if len(old_data) == 0:
				self.db.data.update_one(
					{"username":self.account_detail["username"]},
					{"$push":{"followers":follower, "logs":log}}
				)                
			#end if
		except AssertionError:
			print("[igfollowers] Assertion is not satisfied.")
		#end try

	def get_user(self, username=None):
		assert username is not None, "username is not defined."
		assert self.db  is not None, "db is not defined."

		result         = [document for document in self.db.data.find({"username":username})]
		result         = result[0] # TODO: check if result is less than 0
		user           = User(username=username)
		user.crawl     = False
		user.followers = result["followers"]
		return user
from .user import User 
import pymongo

class CrawlingList:
	def __init__(self):
		self.accounts = self.get_accounts()

	def get_accounts(self):
		conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
		db   = conn["ig"]

		docs = db.crawlingList.find({"is_active": True})
		for doc in docs:
			user = User()
			user.username 	  = doc["userName"]
			user.link     	  = doc["url"]
			user.display_name = doc["displayName"]
			yield user


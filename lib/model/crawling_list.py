from .user import User 
import pymongo
import profig

class CrawlingList:
	def __init__(self):
		self.accounts = self.get_accounts()

	def get_accounts(self):
		config = profig.Config(os.path.join(os.getcwd(), "config", "database.cfg"))
		config.init("crawling_list.connectionString", "mongodb://mongo:27017/ig", str)
		config.init("crawling_list.db", "ig", str)
		config.init("crawling_list.collection", "crawlingList", str)
		config.sync()

		conn = pymongo.MongoClient(config["crawling_list.connectionString"])
		db   = conn[config["crawling_list.db"]]

		docs = db[config["crawling_list.collection"]].find({"is_active": True})
		for doc in docs:
			user = User()
			user.username 	  = doc["userName"]
			user.link     	  = doc["url"]
			user.display_name = doc["displayName"]
			yield user


import bson
import pymongo

class Data(object):
	SMALL_MOCK_INPUT = {
        "collectionName": "", 
           "displayName": "", 
             "followers": 0, 
             "following": 0, 
                 "posts": 0, 
                   "url": "https://www.instagram.com/kiainthephilippines/", 
                "userId": 0, 
              "userName": "kiainthephilippines"
    }

	BIG_MOCK_INPUT = {
		"collectionName": "toyotamotorphfollowers", 
		   "displayName": "Toyota Philippines", 
		     "followers": 8165, 
		     "following": 3, 
		         "posts": 163, 
		           "url": "https://www.instagram.com/toyotamotorphilippines/", 
		        "userId": 1512780643, 
		      "userName": "toyotamotorphilippines"
	}

	def connect_to_database(self):
		db = pymongo.MongoClient("mongodb://220.100.163.132:27017/ig")
		db = db["ig"]
		return db

	@property
	def user_list(self):
		# return [Data.SMALL_MOCK_INPUT]
		try:
			db   = self.connect_to_database()
			data = [doc for doc in db.crawlingList.find({"is_active":True})]			
			return data
		except FileNotFoundError:
			return []
	
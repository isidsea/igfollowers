import json

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

	@property
	def user_list(self):
		# return [Data.SMALL_MOCK_INPUT]
		try:
			data_path = "/root/app/data/Data.json"
			data      = open(data_path,"r")
			data      = json.load(data)
			return data
		except FileNotFoundError:
			return []
	
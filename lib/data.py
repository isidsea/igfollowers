class Data(object):
	SMALL_MOCK_INPUT = {
		"collectionName": "toyotamotorvifollowers", 
		   "displayName": "Toyota Vietnam", 
		     "followers": 70, 
		     "following": 69, 
		         "posts": 5, 
		           "url": "https://www.instagram.com/toyotavietnam/", 
		        "userId": 1718775482, 
		      "userName": "toyotavietnam"
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
		return [Data.SMALL_MOCK_INPUT]
	
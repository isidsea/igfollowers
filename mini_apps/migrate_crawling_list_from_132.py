import pymongo

if __name__ == "__main__":
	server_conn = pymongo.MongoClient("mongodb://220.100.163.132/ig")
	server_db   = server_conn["ig"]

	local_conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
	local_db   = local_conn["ig"]

	crawling_list = server_db.crawlingList.find()
	for account in crawling_list:
		local_db.crawlingList.insert_one(account)
	server_conn.close()
	local_conn.close()
from ..exceptions import CannotFindAccount
import pymongo
import re
import profig
import os

class CrawlingListFinder:
	def find(self, username=None):
		""" Exceptions:
			- AssertionError
			- CannotFindAccount
		"""
		assert username is not None, "username is not defined."

		config = profig.Config(os.path.join(os.getcwd(), "config", "database.cfg"))
		config.init("crawling_list.connectionString", "mongodb://mongo:27017/ig", str)
		config.init("crawling_list.db", "ig", str)
		config.init("crawling_list.collection", "crawlingList", str)
		config.sync()

		conn = pymongo.MongoClient(config["crawling_list.connectionString"])
		db   = conn[config["crawling_list.db"]]

		doc = db[config["crawling_list.collection"]].find_one({"$and":[
			{"userName": re.compile(username, re.IGNORECASE)},
			{"is_active": True}
		]})
		conn.close()

		if doc is None:
			raise CannotFindAccount("Cannot find %s in crawlingList" % username)
		return doc
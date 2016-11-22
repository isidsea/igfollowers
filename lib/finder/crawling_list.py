from ..exceptions import CannotFindAccount
import pymongo
import re

class CrawlingListFinder:
	def find(self, username=None):
		""" Exceptions:
			- AssertionError
			- CannotFindAccount
		"""
		assert username is not None, "username is not defined."

		conn = pymongo.MongoClient("mongodb://mongo:27017/ig")
		db   = conn["ig"]

		doc = db.crawlingList.find_one({"$and":[
			{"userName": re.compile(username, re.IGNORECASE)},
			{"is_active": True}
		]})
		conn.close()

		if doc is None:
			raise CannotFindAccount("Cannot find %s in crawlingList" % username)
		return doc
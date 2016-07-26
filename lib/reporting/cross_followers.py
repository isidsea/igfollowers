from pymongo  import MongoClient
from ..logger import Logger
import pandas as pd
import os

class Engine(object):
	def __init__(self):
		self.logger           = Logger()
		self.logger.app_name  = "reporting_engine"
		self.report_directory = "./report"
		self.path             = "{}/Cross-Followerx.xlsx".format(self.report_directory)
		self.db               = MongoClient("mongodb://220.100.163.132:27017/test")
		self.db               = self.db.ig
		
		# Making folders for report
		if not os.path.exists(self.report_directory):
			os.makedirs(self.report_directory)

	def generate(self):
		""" A reporting engine that helps to find cross followers.
			After running this reporting engine, a new file under ./report/Cross-Followers.xlsx will be produced
		"""
		try:
			assert self.db   is not None, "db is not defined."
			assert self.path is not None, "path is not defined."
			self.logger.write("[cross_followers] Making up report...")

			data   = []
			writer = pd.ExcelWriter(self.path)
			df     = pd.DataFrame() 
			df.to_excel(writer, sheet_name="Cross Followers", index=False, index_label=False)
			for user in self.db.users.find({"$where":"this.following.length > 1"}):
				following    = user["following"]
				username     = user["username"]
				user_link    = user["user_link"]
				display_name = user["display_name"] if "display_name" in user else ""
				followed_to = ""
				for follow_to in following:
					followed_username = follow_to["username"]
					followed_to       = "{},{}".format(followed_to, followed_username)
				followed_to = followed_to[1:]
				followed_to = "[{}]".format(followed_to)
				data.append([
					username, 
					display_name,
					user_link, 
					len(followed_to.split(",")),
					followed_to
				])
			df = pd.DataFrame(data=data, columns=["Username", "Display Name", "User Link", "Total", "Follow To"])
			df.to_excel(writer, sheet_name="Cross Followers", index=False, index_label=False)
			writer.save()
			self.logger.write("[cross_followers] Report was made in {}".format(self.path))
		except AssertionError:
			self.logger.write("[reporting_engine][cross_followers] Assertion is not passed.")
		except:
			raise
	#end def

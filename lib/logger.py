import os
import bson.json_util
import arrow

class FileEngine(object):
	def __init__(self):
		self.directory = "./log"

		# Making folders for report
		if not os.path.exists(self.directory):
			os.makedirs(self.directory)

	def save(self, file_name=None, document=None):
		assert file_name is not None, "file_name is not defined."
		assert document  is not None, "document is not defined."

		if ".json" not in file_name: 
			file_name = "{}.json".format(file_name)
		file = open("{}/{}".format(self.directory, file_name), "a")
		if type(document) is dict:
			document = bson.json_util.dumps(document)
		assert type(document) is str, "document is not str."
		file.write("{}\n".format(document))


class Logger(object):
	def __init__(self):
		self.engine   = FileEngine()
		self.app_name = None
	
	def _generate_document(self, app_name=None, level=None, text=None):
		assert text     is not None, "text is not defined."
		assert app_name is not None, "app_name is not defined."

		current_date = arrow.utcnow().datetime
		document = {
			"_insert_time" : current_date,
			    "app_name" : app_name,
			       "level" : level,
			        "text" : text
		}
		return document

	def error(self, text=None, app_name=None, level="ERROR", save_engine=None):
		assert text          is not None, "text is not defined."
		assert self.app_name is not None, "app_name is not defined."

		app_name = app_name if app_name is not None else self.app_name
		document = self._generate_document(
			app_name = self.app,
			   level = level,
			    text = text
		)
		if save_engine is None: 
			self.engine.save(app_name, document)

	def debug(self,text=None, app_name=None, level="DEBUG", save_engine=None):
		assert text          is not None, "text is not defined."
		assert self.app_name is not None, "app_name is not defined."

		app_name = app_name if app_name is not None else self.app_name
		document = self._generate_document(
			app_name = self.app,
			   level = level,
			    text = text
		)
		if save_engine is None: 
			self.engine.save(app_name, document)

	def write(self,text=None, app_name=None, level="DEBUG", save_engine=None):
		assert text          is not None, "text is not defined."
		assert self.app_name is not None, "app_name is not defined."

		app_name = app_name if app_name is not None else self.app_name
		document = self._generate_document(
			app_name = self.app,
			   level = level,
			    text = text
		)
		if save_engine is None: 
			self.engine.save(app_name, document)

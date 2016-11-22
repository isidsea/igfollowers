from ..finder.crawling_list import CrawlingListFinder

class FinderFactory:
	CRAWLING_LIST = 0

	@classmethod
	def get_finder(self, finder_name=None):
		""" Exceptions:
			- AssertionError
		"""
		assert finder_name is not None, "finder_name is not defined."

		if finder_name == FinderFactory.CRAWLING_LIST:
			return CrawlingListFinder()
from ..extractor.xpath import XPATHExtractor

class ExtractorFactory:
	XPATH     = 0

	@classmethod
	def get_extractor(self, extractor_name=None):
		""" Exceptions:
			- AssertionError
		"""
		assert extractor_name is not None, "extractor_name is not defined."

		if extractor_name == ExtractorFactory.XPATH:
			return XPATHExtractor()
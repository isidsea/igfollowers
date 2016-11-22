from ..saver.follower import FollowerSaver

class SaverFactory:
	FOLLOWER = 0

	@classmethod
	def get_saver(self, saver_name=None):
		""" Exceptions:
			- AssertionError
		"""

		if saver_name == SaverFactory.FOLLOWER:
			return FollowerSaver()
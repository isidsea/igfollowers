from lib.model.crawling_list import CrawlingList
from lib.engine.followers    import FollowersEngine
from lib.logger 		     import Logger
from lib.exceptions          import TooManyDuplicate

if __name__ == "__main__":
	""" Exceptions:
		- AssertionError (FollowerEngine.login, FollowerEngine.crawl)
		- CannotFindElements (FollowerEngine.login, FollowerEngine.crawl)
		- CannotLogin (FollowerEngine.login)
		- CannotFindAccount (FollowerEngine.crawl)
	"""
	Logger()
	engine = FollowersEngine()
	engine.login("amoure20", "081703706966")

	crawling_list = CrawlingList()

	for account in crawling_list.accounts:
		try:
			engine.crawl(account.username)
		except TooManyDuplicate as ex:
			pass
	engine.browser.close()
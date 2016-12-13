from lib.model.crawling_list import CrawlingList
from lib.engine.followers    import FollowersEngine
from lib.logger 		     import Logger
from lib.exceptions          import TooManyDuplicate
import click
import os
import profig
import copy
import shutil

@click.option("--account", help="Account name on config file", default="account_1")
@click.command()
def run(account):
	""" Exceptions:
		- AssertionError (FollowerEngine.login, FollowerEngine.crawl)
		- CannotFindElements (FollowerEngine.login, FollowerEngine.crawl)
		- CannotLogin (FollowerEngine.login)
		- CannotFindAccount (FollowerEngine.crawl)
	"""
	if os.path.isdir(os.path.join(os.getcwd(), "screenshot")):
		shutil.rmtree(os.path.join(os.getcwd(), "screenshot"))
	os.makedirs(os.path.join(os.getcwd(), "screenshot"))

	config = profig.Config(os.path.join(os.getcwd(), "config", "account.cfg"))
	config.init("%s.username" % account, "", str)
	config.init("%s.password" % account, "", str)
	config.sync()

	username = copy.copy(config["%s.username" % account])
	password = copy.copy(config["%s.password" % account])

	# Logger()	
	engine = FollowersEngine()
	engine.login(username, password)

	crawling_list = CrawlingList()
	for account in crawling_list.accounts:
		try:
			print("[igfollowers][debug] Crawling: %s" % account.username)
			engine.crawl(account.username)
		except TooManyDuplicate as ex:
			print("[igfollowers][debug] %s" % ex)
	engine.browser.close()

if __name__ == "__main__":
	run()
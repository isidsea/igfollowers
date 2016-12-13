from ..model.browser     import Browser
from ..model.user        import User
from ..factory.extractor import ExtractorFactory
from ..factory.finder    import FinderFactory
from ..factory.saver 	 import SaverFactory
from ..exceptions        import CannotFindElements, CannotLogin, DuplicateFollower, TooManyDuplicate
import copy
import os
import selenium

class FollowersEngine:
	def __init__(self):
		self.browser = Browser()

	def login(self, username=None, password=None):
		""" Exceptions:
			- AssertionError (XPATHExtractor)
			- CannotFindElements (XPATHExtractor)
			- CannotLogin
		"""
		assert username is not None, "username is not defined."
		assert password is not None, "password is not defined."
		assert username            , "username is not defined."
		assert password            , "password is not defined."

		self.browser.get("https://instagram.com")
		extractor = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
		self.browser.driver.save_screenshot(os.path.join(os.getcwd(), "screenshot", "before_login.jpg"))

		btn_show_login = extractor.extract(
			browser = self.browser, 
			xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a',
			wait = '//*[@id="react-root"]/section/main/article/div[2]/div[2]/p/a'
		)
		btn_show_login.click()

		txt_username = extractor.extract(
			browser = self.browser,
			xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[1]/input',
			wait = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button'
		)
		txt_username.send_keys(username)

		txt_password = extractor.extract(
			browser = self.browser,
			xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/div[2]/input',
			wait = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button'
		)
		txt_password.send_keys(password)

		btn_login = extractor.extract(
			browser = self.browser,
			xpath = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button',
			wait = '//*[@id="react-root"]/section/main/article/div[2]/div[1]/div/form/span/button'
		)
		btn_login.click()

		try:
			instagram_logo = extractor.extract(
				browser = self.browser,
				xpath = '//*[@id="react-root"]/section/nav/div/div/div/div[1]/div/a',
				wait = '//*[@id="react-root"]/section/nav/div/div/div/div[1]/div/a'
			)
		except CannotFindElements:
			self.browser.driver.save_screenshot(os.path.join(os.getcwd(), "screenshot", "login_error.png"))
			raise CannotLogin("Possibly because of wrong username or password. If username and password is correct, you need to see this screenshot first.")

	def crawl(self, username=None):
		""" Exceptions:
			- AssertionError (CrawlingListFinder, FollowerSaver, Browser.get, XPATHExtractor)
			- CannotFindAccount (CrawlingListFinder)
			- CannotFindElements (XPATHExtractor)
			- TooManyDuplicate
		"""
		assert username is not None, "username is not defined."

		finder    = FinderFactory.get_finder(FinderFactory.CRAWLING_LIST)
		oa_detail = finder.find(username) #oa_detail stands for Official Account Detail

		saver         = SaverFactory.get_saver(SaverFactory.FOLLOWER)
		saver.account = copy.deepcopy(oa_detail)

		self.browser.get("https://instagram.com/%s" % username)

		extractor     = ExtractorFactory.get_extractor(ExtractorFactory.XPATH)
		btn_followers = extractor.extract(
			browser = self.browser,
			xpath = '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a',
			wait = '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a'
		)
		btn_followers.click()

		total_followers = extractor.extract(
			browser = self.browser,
			xpath = '//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span',
			wait ='//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a/span'
		)
		total_followers = total_followers.get_attribute("title")
		total_followers = total_followers.replace(",","")
		total_followers = int(total_followers)

		start_index     = 0
		end_index       = 10
		total_duplicate = 0
		while end_index < total_followers:
			# I do not know how it works, magically it scrolls!!
			if end_index >= total_followers:
				end_index = total_followers
			users_elements = extractor.extract(
				browser = self.browser,
				xpath = '/html/body/div[2]/div/div[2]/div/div[2]/ul/li',
				wait = '/html/body/div[2]/div/div[2]/div/div[2]/ul/li[%s]' % end_index
			)
					
			for element in users_elements[start_index:end_index]:
				try:
					user 			  = User()
					user.username 	  = element.find_element_by_class_name("_4zhc5").text
					user.link     	  = element.find_element_by_class_name("_4zhc5").get_attribute("href")
					user.display_name = element.find_element_by_class_name("_2uju6").text
					saver.save(user.to_dict())
					total_duplicate = 0
					print("[FollowerSaver][%s] Inserted one follower!" % oa_detail["userName"])
				except DuplicateFollower as ex:
					total_duplicate += 1
				except selenium.common.exceptions.StaleElementReferenceException:
					print("Stale")
				if total_duplicate >= 5:
					raise TooManyDuplicate("Threshold is %s. Too many duplicate follower!" % total_duplicate)
			start_index = copy.copy(end_index)
			end_index   = end_index + 10


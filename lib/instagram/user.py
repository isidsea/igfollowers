from ..logger import Logger
import time
import random
import selenium
import copy

class User(object):
	def __init__(self,username=None, session=None):
		assert username      is not None, "username is not defined."

		self.logger     	 = Logger()
		self.logger.app_name = "igfollowers"
		self.session    	 = session
		self.username  	 	 = username
		self.crawl      	 = True
		self._followers 	 = []

	@property
	def followers(self):
		if self.crawl:
			self._followers = self._crawl_followers()
		return self._followers

	@followers.setter
	def followers(self, value):
		self._followers = copy.deepcopy(value)

	def _crawl_followers(self):
		assert self.session is not None, "session is not defined."
		driver = self.session[0]
		wait   = self.session[1]
		
		wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a'))
		btn_show_followers = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a')
		btn_show_followers.click()

		wait.until(lambda driver:driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[2]'))			
		self.logger.debug("[{}] Scrolling...".format(self.username))
		
		dialog      = driver.find_elements_by_class_name('_4gt3b')[0]		
		prev_height = -1
		max_exceed  = False
		while not max_exceed:
			driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
			time.sleep(random.randint(1000,5000)/1000)

			scroll_top    = int(dialog.get_attribute("scrollTop"))
			scroll_height = int(dialog.get_attribute("scrollHeight"))
			offset_height = int(dialog.get_attribute("offsetHeight"))
			
			try:
				loading_bar = driver.find_element_by_class_name("_lm3a0")
			except selenium.common.exceptions.NoSuchElementException:
				if prev_height == scroll_height:
					max_exceed = True
				else:
					max_exceed  = False
					prev_height = int(dialog.get_attribute("scrollHeight"))		
		users     = driver.find_elements_by_class_name("_cx1ua")		
		documents = list()
		self.logger.debug("[{}] Fetching user data...".format(self.username))
		for user in users:			
			username     = user.find_element_by_class_name("_4zhc5")
			username     = username.text
			user_link    = user.find_element_by_class_name("_4zhc5")
			user_link    = user_link.get_attribute("href")
			display_name = user.find_element_by_class_name("_2uju6")
			display_name = user.text.split("\n")[1]
			document     = {
				    "username" : username,
				   "user_link" : user_link,
				"display_name" : display_name
			}
			documents.append(document)
		#end for
		return documents
from tqdm import tqdm
import time
import random
import selenium

class User(object):
	def __init__(self,session=None):
		assert session       is not None, "session is not defined."
		assert type(session) is list    , "session should be list."

		self.driver     = session[0]
		self.wait       = session[1]		

	@property
	def followers(self):
		assert self.driver is not None, "driver is not defined."
		assert self.wait   is not None, "wait is not defined."
		
		self.wait.until(lambda driver:driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a'))
		btn_show_followers = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/header/div[2]/ul/li[2]/a')
		btn_show_followers.click()

		self.wait.until(lambda driver:driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/div/div[2]/ul/li[2]'))	
		print("[igfollowers] Scrolling...")
		
		dialog      = self.driver.find_elements_by_class_name('_4gt3b')[0]		
		prev_height = -1
		max_exceed  = False
		while not max_exceed:
			self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog)
			time.sleep(random.randint(1000,5000)/1000)

			scroll_top    = int(dialog.get_attribute("scrollTop"))
			scroll_height = int(dialog.get_attribute("scrollHeight"))
			offset_height = int(dialog.get_attribute("offsetHeight"))
			
			try:
				loading_bar = self.driver.find_element_by_class_name("_lm3a0")
			except selenium.common.exceptions.NoSuchElementException:
				if prev_height == scroll_height:
					max_exceed = True
				else:
					max_exceed  = False
					prev_height = int(dialog.get_attribute("scrollHeight"))		
		users     = self.driver.find_elements_by_class_name("_cx1ua")
		users     = tqdm(users)
		documents = list()
		for user in users:
			users.set_description("[igfollowers] Fetching user data...")
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
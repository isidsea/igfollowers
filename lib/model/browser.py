from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support.ui                  import WebDriverWait
from selenium   									import webdriver

class Browser:
	def __init__(self, url=None):
		cap                                               = DesiredCapabilities.PHANTOMJS.copy()
		cap["phantomjs.page.settings.userAgent"]          = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		cap["phantomjs.page.settings.loadImages"]         = False
		cap["phantomjs.page.settings.webSecurityEnabled"] = False

		service_args = ['--ignore-ssl-errors=true','--ssl-protocol=tlsv1']
		self.driver  = webdriver.PhantomJS(
			desired_capabilities = cap,
			        service_args = service_args
			)
		self.wait = WebDriverWait(self.driver,30)
		self.driver.set_window_size(1366,768)

		if url is not None:
			self.get(url)

	def get(self, url=None):
		""" Exceptions:
			- AssertionError
		"""
		assert url 		   is not None, "url is not defined."
		assert self.driver is not None, "driver is not defined."

		self.driver.get(url)

	def close(self):
		""" Exceptions:
			- AssertionError
		"""
		assert self.driver is not None, "driver is not defined."
		self.driver.close()
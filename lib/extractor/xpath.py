from ..exceptions import CannotFindElements
import selenium
import os

class XPATHExtractor:
	def extract(self, browser=None, xpath=None, **kwargs):
		""" Exceptions:
			- AssertionError
			- CannotFindElements
		"""
		assert browser        is not None, "browser is not defined."
		assert browser.driver is not None, "browser.driver is not defined."
		assert xpath          is not None, "xpath is not defined."

		wait      = kwargs.get("wait", None)
		max_retry = kwargs.get("max_retry", 10)
		if wait is not None:
			tried   = 0
			success = False
			while not success and tried < max_retry:
				try:
					browser.wait.until(lambda driver: driver.find_element_by_xpath(wait))
					success = True
				except selenium.common.exceptions.TimeoutException:
					tried += 1
					print("Retrying")
					browser.driver.save_screenshot(os.path.join(os.getcwd(), "screenshot", "retry.jpg"))
			if tried >= max_retry:
				raise CannotFindElements("You are waiting %s more than %s times" % (xpath, max_retry))
		elements = browser.driver.find_elements_by_xpath(xpath)
		
		if len(elements) == 0:
			raise CannotFindElements("Cannot find elements with xpath: %s" % xpath)

		if len(elements) == 1:
			return elements[0]
		return elements
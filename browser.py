import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

class Browser:
	driver = None

	def __init__(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()

	def open_video(self, search):
		
		try:
			self.driver.get("https://www.youtube.com/results?search_query=" + str(search))

			# Agree for cookies disclaimer
			agree = self.driver.find_elements_by_xpath("//*[contains(text(), 'I Agree')]")[0]
			if agree.is_enabled:
				agree.click()
			else:
				print("Unable to click the \"I Agree\" button from disclaimer.")
				return -1

			fail = True
			# Play first video from search query
			videos = self.driver.find_elements_by_xpath('//*[@id="video-title"]')
			for video in videos:
				# Sometimes the first result is not clickable
				if video.is_enabled() and video.is_displayed():
					video.click()
					fail = False
					break

			if fail:
				print("Could not find any video to open.")
				return -1

		except WebDriverException:
			print("There is no internet connection.")
			return -1

		return 1

	def close(self):
		self.driver.close()

if __name__ == '__main__':
	video = "Mozart - Lacrimosa"
	
	browser = Browser()
	browser.open_video(video)
	time.sleep(2)
	browser.close()



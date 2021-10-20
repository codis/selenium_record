import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

class Browser:
	driver = None

	def __init__(self):
		self.driver = webdriver.Chrome()
		self.driver.maximize_window()

	def open_video(self, search):

		#wait = WebDriverWait(driver, 3)
		#presence = EC.presence_of_element_located
		#visible = EC.visibility_of_element_located

		self.driver.get("https://www.youtube.com/results?search_query=" + str(search))
		# Agree for cookies disclaimer
		self.driver.find_elements_by_xpath("//*[contains(text(), 'I Agree')]")[0].click()
		# Play first video from search query
		videos = self.driver.find_elements_by_xpath('//*[@id="video-title"]')
		for video in videos:
			# Sometimes the first result is not clickable
			if video.is_enabled() and video.is_displayed():
				video.click()
				break

	def close(self):
		self.driver.close()

if __name__ == '__main__':
	video = "Mozart - Lacrimosa"
	
	browser = Browser()
	browser.open_video(video)
	time.sleep(2)
	browser.close()



import time

import os

#import math
import numpy as np
from browser import Browser
from record import Record, highest_fps_possible
from scipy.io.wavfile import read

#options = webdriver.ChromeOptions()
#options.addrguments("--incognito");
#options.AddUserProfilePreference("profile.default_content_setting_values.cookies", 2)

VIDEO = "Rachmaninoff - Piano Concerto No.2, I. Moderato"
SCREEN_SIZE = (1920, 1080)


def dbs_average(file):
	samprate, wavdata = read(file)
	chunks = np.array_split(wavdata, 5)
	dbs = [20*np.log10( np.sqrt(np.mean(chunk**2)) ) for chunk in chunks]
	print(dbs)

def main():
	(fps, timing) = highest_fps_possible()
	# for (1920, 1080) its 2 fps
	print(fps, timing)

	browser = Browser()
	browser.open_video(VIDEO)
	#time.sleep(2)
	
	record = Record()
	record.test_screen(30, SCREEN_SIZE, fps, timing, "output.avi")

	browser.close()
	#record_screen()

main()
#dbs_average("out.wav")

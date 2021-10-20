# Code for Screen recording was adapted from:
# 	https://www.thepythoncode.com/article/make-screen-recorder-python
# Pyautogui docs:
#	https://pyautogui.readthedocs.io/_/downloads/en/latest/pdf/

import time
import cv2
import numpy as np
import pyautogui

SCREEN_SIZE = (1920, 1080)

class Screen():
	screen_size = ()
	fps = -1
	video_out = None
	timing = 0

	def __init__(self, screen_size, fps, timing):
		# display screen resolution, get it from your OS settings
		# pyautogui.size() says it gives the size of the primary screen only,
		# but in my case it gave of both monitors
		#SCREEN_SIZE = pyautogui.size()
		self.screen_size = screen_size
		self.timing = timing
		self.fps = fps

	def open(self, file):
		fourcc = cv2.VideoWriter_fourcc(*"XVID")
		self.video_out = cv2.VideoWriter(file, fourcc, self.fps, (self.screen_size))

	def record(self, record_time):
		t1 = time.time()
		t2 = time.time()
		# To fill the short delay between seconds
		delay = (1000 - int((1 / self.fps + self.timing) * 1000))
		while (t2 - t1) < record_time:
			#print(t2 - t1, delay)
			img = pyautogui.screenshot(region=(0, 0, self.screen_size[0], self.screen_size[1]))
			frame = np.array(img)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.video_out.write(frame)
			
			#Its in ms
			#cv2.waitKey(delay)
			t2 = time.time()

		self.video_out.release()

	def check_fps_timing(self):
		FRAMES = 10

		print("Start")
		t1 = time.time()
		for i in range(0, FRAMES):
			img = pyautogui.screenshot(region=(0, 0, self.screen_size[0], self.screen_size[1]))
			frame = np.array(img)
			frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			self.video_out.write(frame)
		t2 = time.time()
		print("Stop")

		took = t2 - t1
		print(took)

		self.video_out.release()
		return took / FRAMES

def highest_fps_possible():
	screen = Screen(SCREEN_SIZE, 30, 1, "output.avi")
	# How much time it took per frame to screenshot and write
	# Needed to optimes how many fps can be put in the recording without
	timing = screen.check_fps_timing()

	for i in range(1,60):
		if timing * i > 1:
			break

	return (i - 1, timing)

if __name__ == '__main__':
	#(fps, timing) = highest_fps_possible()
	# for (1920, 1080) its 2 fps
	#print(fps, timing)
	fps = 2
	timing = 0.5
	screen = Screen(SCREEN_SIZE, fps, timing)
	screen.open("output.avi")
	screen.record(10)
	
import numpy as np
from browser import Browser
from screen import Screen, highest_fps_possible
from audio import Audio

VIDEO = "Rachmaninoff - Piano Concerto No.2, I. Moderato"
SCREEN_SIZE = (1920, 1080)
DEFAULT_FRAMES = 512

def dbs_average(file):
	samprate, wavdata = read(file)
	chunks = np.array_split(wavdata, 5)
	dbs = [20*np.log10( np.sqrt(np.mean(chunk**2)) ) for chunk in chunks]
	print(dbs)

def main():
	#(fps, timing) = highest_fps_possible()
	# for (1920, 1080) its 2 fps
	#print(fps, timing)

	browser = Browser()
	browser.open_video(VIDEO)

	"""
	audio = Audio(DEFAULT_FRAMES)
	devs = audio.get_device()
	print(devs)
	mode = {"input": True, "output": False}
	err = audio.set_device(0, mode)
	err = audio.open("out.wav")
	audio.record(10)
	"""

	fps = 2
	timing = 0.5
	screen = Screen(SCREEN_SIZE, fps, timing)
	screen.open("output.avi")
	screen.record(10)

	browser.close()

main()
#dbs_average("out.wav")

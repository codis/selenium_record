from threading import Thread
from browser import Browser
from screen import Screen, highest_fps_possible
from audio import Audio
import numpy as np

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
	err = browser.open_video(VIDEO)
	if err < 0:
		print("Failed to open video. Exiting...")
		exit()
	record_time = 10

	audio = Audio(DEFAULT_FRAMES)
	devs = audio.get_device()

	mode = {"input": True, "output": False}
	err = audio.set_device(0, mode)
	if err < 0:
		print("Failed to setup audio device. Exiting...")
		exit()
	
	err = audio.open("out.wav")
	if err < 0:
		print("Failed to open audio stream. Exiting...")
		exit()

	print("Audio setup was succesfull")

	fps = 2
	timing = 0.5
	screen = Screen(SCREEN_SIZE, fps, timing)
	screen.open("output.avi")
	if err < 0:
		print("Failed to open screen interface. Exiting...")
		audio.close()
		exit()

	print("Screen setup was succesfull")

	threads = [
    	Thread(target = audio.record, args=(record_time,)),
    	Thread(target = screen.record, args=(record_time,))
	]

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	audio.close()
	screen.close()
	browser.close()

main()
#dbs_average("out.wav")

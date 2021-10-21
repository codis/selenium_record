from browser import Browser
from screen import Screen, highest_fps_possible
from audio import Audio
from scipy.io import wavfile
import urllib.request
import numpy as np
import threading
import signal
import time

VIDEO = "Rachmaninoff - Piano Concerto No.2, I. Moderato"
SCREEN_SIZE = (1920, 1080)
DEFAULT_FRAMES = 512
audio_file = "out.wav"
screen_file = "output.avi"

def dbs_average(file, record_time):
	samprate, wavdata = wavfile.read(file)
	wavdata = wavdata / (2.**15)
	chunks = np.array_split(wavdata, record_time)
	dbs = [20 *np.log10(np.sqrt(np.mean(chunk))) for chunk in chunks]

	new_dbs = []
	for db in dbs:
		if np.isnan(db):
			continue
		new_dbs.append(db)

	print("Average db level is %f" % np.mean(new_dbs))

def clean(audio, screen, browser):
	audio.close()
	screen.close()
	browser.close()

def check_net():
	while True:
		try:
			urllib.request.urlopen('http://google.com')
		except:
			print("There is no more internet connection. Exiting...")
			exit()
		time.sleep(5)

def main():
	#(fps, timing) = highest_fps_possible()
	# for (1920, 1080) its 2 fps
	#print(fps, timing)

	# If at any point we lose internet
	# there is no reason to continue
	daemon = threading.Thread(target=check_net)
	daemon.daemon = True
	daemon.start()
	print("Internet daemon started.")

	audio = Audio(DEFAULT_FRAMES)
	dev_list = audio.get_device()
	print("List of devices")
	print(dev_list)

	# Ideally we would select from the list of devs a device
	# since this is not the point, I will just use the default dev
	dev_id = 0
	mode = {"input": True, "output": False}
	err = audio.set_device(0, mode)
	if err < 0:
		print("Failed to setup audio device. Exiting...")
		exit()
	print("Audio Device %d was succesfully setup." % dev_id)
	
	err = audio.open(audio_file)
	if err < 0:
		print("Failed to open audio stream. Exiting...")
		exit()
	print("Audio stream is open.")

	print("Audio setup was succesfull.")

	fps = 2
	timing = 0.5
	screen = Screen(SCREEN_SIZE, fps, timing)
	screen.open(screen_file)
	if err < 0:
		print("Failed to open screen interface. Exiting...")
		audio.close()
		exit()
	print("Screen interface is open.")

	print("Screen setup was succesfull.")

	browser = Browser()
	err = browser.open_video(VIDEO)
	if err < 0:
		print("Failed to open video. Exiting...")
		clean(audio, screen, browser)
		exit()
	print("Video is now online.")

	record_time = 120
	threads = [
    	threading.Thread(target=audio.record, args=(record_time,)),
    	threading.Thread(target=screen.record, args=(record_time,))
	]

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	print("Audio recording was succesfull.")
	print("Screen recording was succesfull.")

	clean(audio, screen, browser)

	dbs_average(audio_file, record_time)	

main()


# Code for Screen recording was adapted from:
# 	https://www.thepythoncode.com/article/make-screen-recorder-python
# Pyautogui docs:
#	https://pyautogui.readthedocs.io/_/downloads/en/latest/pdf/
# Code for Audio recording was taken from:
#	https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo_python3.py

import time
import cv2
import numpy as np
import pyautogui

import pyaudio
import wave

SCREEN_SIZE = (1920, 1080)
DEFAULT_FRAMES = 512

class Record:
	# Screen
	screen_size = ()
	fps = -1
	video_out = None
	timing = 0

	# Audio
	audio = None
	default_dev_id = -1
	dev_info = None
	frames = -1
	channels = 0
	input_ch = False
	output_ch = False
	recorded_frames = []

	def __init__(self):
		pass
		
	def init_audio(self, frames):
		self.audio = pyaudio.PyAudio()
		try:
			self.default_dev_id = self.audio.get_default_input_device_info()
		except IOError:
			self.default_dev_id = -1

		self.frames = frames

	def init_screen(self, screen_size, fps, timing, file):
		# display screen resolution, get it from your OS settings
		# pyautogui.size() says it gives the size of the primary screen only,
		# but in my case it gave of both monitors
		#SCREEN_SIZE = pyautogui.size()
		self.screen_size = screen_size
		self.timing = timing
		self.fps = fps
		fourcc = cv2.VideoWriter_fourcc(*"XVID")
		self.video_out = cv2.VideoWriter(file, fourcc, self.fps, (self.screen_size))

	def get_audio_device(self):
		devs = []
		for i in range(0, self.audio.get_device_count()):
			info = self.audio.get_device_info_by_index(i)
			hostAPI = self.audio.get_host_api_info_by_index(info["hostApi"])["name"]
			print("Dev id: " + str(info["index"]), (info["name"], hostAPI))
			devs.append((info["index"], info["name"], hostAPI))

		return devs

	def set_audio_device(self, dev_id, mode):
		try:
			if dev_id < 0:
				self.dev_info = self.audio.get_device_info_by_index(self.default_dev_id)
			else:
				self.dev_info = self.audio.get_device_info_by_index(dev_id)
		except IOError:
			print("Selected device is not available.")
			return -1

		is_mode = False
		print(mode)
		if mode["input"]:
			is_input = self.dev_info["maxInputChannels"] > 0
			if is_input:
				is_mode = True
				self.input_ch = True
				self.channels = self.channels + self.dev_info["maxInputChannels"]
			else:
				print("Selected device has no input channels.")
		
		if mode["output"]:
			is_output = self.dev_info["maxOutputChannels"] > 0
			if is_output:
				is_mode = True
				self.output_ch = True
				self.channels = self.channels + self.dev_info["maxOutputChannels"]
			else:
				print("Selected device has no output channels.")

		if not is_mode:
			print("Please chose mode for selected device.")
			return -1

		return 1

	def record_audio(self, record_time):
		print(self.input_ch, self.output_ch)
		stream = self.audio.open(format = pyaudio.paInt16,
			channels = self.channels,
			rate = int(self.dev_info["defaultSampleRate"]),
			input = self.input_ch,
			output = self.output_ch,
			frames_per_buffer = self.frames,
			input_device_index = self.dev_info["index"])

		recorded_frames = []
		for i in range(0, int(int(self.dev_info["defaultSampleRate"]) / self.frames * record_time)):
			recorded_frames.append(stream.read(self.frames, exception_on_overflow = False))

		stream.stop_stream()
		stream.close()

		filename = "out.wav"
		waveFile = wave.open(filename, 'wb')
		waveFile.setnchannels(self.channels)
		waveFile.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
		waveFile.setframerate(int(self.dev_info["defaultSampleRate"]))
		waveFile.writeframes(b''.join(recorded_frames))
		waveFile.close()

	def record_screen(self, record_time):
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

	def test_audio(self, record_time, frames):
		self.init_audio(frames)
		devs = self.get_audio_device()
		#print(devs)
		mode = {"input": True, "output": False}
		err = self.set_audio_device(0, mode)
		self.record_audio(record_time)

	def test_screen(self, record_time, screen_size, fps, timing, file):
		self.init_screen(screen_size, fps, timing, file)
		self.record_screen(record_time)

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
	record = Record()
	record.init_screen(SCREEN_SIZE, 30, 1, "output.avi")
	# How much time it took per frame to screenshot and write
	# Needed to optimes how many fps can be put in the recording without
	timing = record.check_fps_timing()

	for i in range(1,60):
		if timing * i > 1:
			break

	return (i - 1, timing)

if __name__ == '__main__':
	#(fps, timing) = highest_fps_possible()
	# for (1920, 1080) its 2 fps
	#print(fps, timing)
	record = Record()

	#record.test_screen(10, SCREEN_SIZE, fps, timing, "output.avi")
	record.test_audio(10, DEFAULT_FRAMES)
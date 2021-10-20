# Code for Audio recording was taken from:
#	https://github.com/intxcc/pyaudio_portaudio/blob/master/example/echo_python3.py

import pyaudio
import wave

DEFAULT_FRAMES = 512

class Audio:
	audio = None
	dev_info = None
	frames = -1
	channels = 0
	input_ch = False
	output_ch = False
	stream = None
	wave_file = None
	recorded_frames = []

	def __init__(self, frames):
		self.audio = pyaudio.PyAudio()
		self.frames = frames

	def get_device(self):
		devs = []
		for i in range(0, self.audio.get_device_count()):
			info = self.audio.get_device_info_by_index(i)
			hostAPI = self.audio.get_host_api_info_by_index(info["hostApi"])["name"]
			print("Dev id: " + str(info["index"]), (info["name"], hostAPI))
			devs.append((info["index"], info["name"], hostAPI))

		return devs

	def set_device(self, dev_id, mode):
		try:
			if dev_id < 0:
				default_dev_id = self.audio.get_default_input_device_info()["index"]
				self.dev_info = self.audio.get_device_info_by_index(default_dev_id)
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
				return -1
		
		if mode["output"]:
			is_output = self.dev_info["maxOutputChannels"] > 0
			if is_output:
				is_mode = True
				self.output_ch = True
				self.channels = self.channels + self.dev_info["maxOutputChannels"]
			else:
				print("Selected device has no output channels.")
				return -1

		if not is_mode:
			print("Please chose mode for selected device.")
			return -1

		return 1

	def open(self, file):
		self.stream = self.audio.open(format = pyaudio.paInt16,
			channels = self.channels,
			rate = int(self.dev_info["defaultSampleRate"]),
			input = self.input_ch,
			output = self.output_ch,
			frames_per_buffer = self.frames,
			input_device_index = self.dev_info["index"])

		try:
			self.wave_file = wave.open(file, 'wb')
			self.wave_file.setnchannels(self.channels)
			self.wave_file.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
			self.wave_file.setframerate(int(self.dev_info["defaultSampleRate"]))
		except wave.Error:
			self.stream.stop_stream()
			self.stream.close()
			print("Failed to open wave file.")
			return -1

		return 1

	def close(self):
		self.stream.close()
		self.wave_file.close()

	def record(self, record_time):
		recorded_frames = []
		self.stream.start_stream()
		try:
			for i in range(0, int(int(self.dev_info["defaultSampleRate"]) / self.frames * record_time)):
				recorded_frames.append(self.stream.read(self.frames, exception_on_overflow = False))
			
		except IOError:
			print("Read operation was unsuccessful")
			self.stream.stop_stream()
			return -1

		self.stream.stop_stream()
		self.wave_file.writeframes(b''.join(recorded_frames))

		return 1

if __name__ == '__main__':
	audio = Audio(DEFAULT_FRAMES)
	devs = audio.get_device()
	print(devs)
	mode = {"input": True, "output": False}
	err = audio.set_device(-1, mode)
	err = audio.open("out.wav")
	audio.record(10)
	audio.close()

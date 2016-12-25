"""
    @file        AudioManager
    @description 
    @author      Res260 
    @created_at  20161221
    @updated_at  20161221
"""
import time
import queue as q
import wave

import pyaudio as pa

class AudioManager:
	"""
		Class that manage the audio for the app.
	"""

	FORMAT = pa.paInt16
	CHANNELS = 1
	RATE = 32000

	def __init__(self, context, logger):
		"""
			Creates a new instance of AudioManager.

			:param context: The ShadowCar object that created `self`
			:param logger:  The logger instance of the app.
		"""
		self._context = context
		self._logger = logger
		self._chunks_queue = q.Queue()
		self._timestamps_queue = q.Queue()
		self.CHUNK = int(self.RATE / self._context.FPS)
		if self.CHUNK != self.RATE / self._context.FPS:
			self._logger.error('Current sound sample rate value ({}) is not '
			                   'divisible by current FPS value ({})'
			                   'Change either value.'.format(self.RATE,
			                                                 self._context.FPS))
			exit(254)
		self._pyaudio = pa.PyAudio()
		self._stream = self._pyaudio.open(
				format=self.FORMAT,
				channels=self.CHANNELS,
				rate=self.RATE,
				input=True,
				frames_per_buffer=self.CHUNK
		)
		self._logger.info('Audio stream opened, ready for recording.')


	def start(self):
		"""
			Starts the audio recording.
		"""
		while not self._context.is_running:
			pass

		while self._context.is_running:
			if self._chunks_queue.qsize() > 100:
				self._save()
			initial_time = time.time()
			self._logger.debug('Audio loop')
			self._capture_audio_chunk()
			while (time.time() - initial_time) < 1 / self._context.FPS:
				pass

	def _save(self):

		audio_sample = []
		while self._chunks_queue.qsize() > 0:
			self._logger.info('{} chunks left'.format(self._chunks_queue.qsize()))
			audio_sample.append(self._chunks_queue.get())

		self._logger.info('Opening wave file...')
		wf = wave.open(self._context.get_output_file_name() + '.wav', 'wb')
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(self._pyaudio.get_sample_size(self.FORMAT))
		wf.setframerate(self.RATE)
		wf.writeframes(b''.join(audio_sample))
		wf.close()
		self._logger.info('Audio saved.')

	def _capture_audio_chunk(self):
		self._chunks_queue.put(self._stream.read(self.CHUNK))
		self._logger.info(self._chunks_queue.qsize())

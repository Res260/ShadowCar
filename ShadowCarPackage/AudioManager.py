"""
    @file        AudioManager
    @description 
    @author      Res260 
    @created_at  20161221
    @updated_at  20161225
"""
import time
import queue as q
import wave

import pyaudio as pa

import ShadowCarPackage


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


	def run(self):
		"""
			Starts the audio recording. When context.is_running is set to false,
			saves the audio.
		"""
		while not self._context.is_running:
			pass

		while self._context.is_running:
			initial_time = time.time()
			self._logger.debug('Audio loop')
			self._capture_audio_chunk()
			while (time.time() - initial_time) < 1 / self._context.FPS:
				pass

		self._save()

	def _save(self):
		"""
			Saves the audio to a wave file. Empties self._chunks_queue.
		"""

		self.output_file_name = self._context.get_output_file_name(ShadowCarPackage.AUDIO)

		audio_sample = []
		while self._chunks_queue.qsize() > 0:
			self._logger.debug('{} chunks left'.format(self._chunks_queue.qsize()))
			audio_sample.append(self._chunks_queue.get())

		self._logger.info('Opening wave file...')
		wf = wave.open(self._context.TEMP_FOLDER + self.output_file_name, 'wb')
		wf.setnchannels(self.CHANNELS)
		wf.setsampwidth(self._pyaudio.get_sample_size(self.FORMAT))
		wf.setframerate(self.RATE)
		wf.writeframes(b''.join(audio_sample))
		wf.close()
		self._logger.info('Saved {}.'.format(self.output_file_name))


	def _capture_audio_chunk(self):
		"""
			Captures an audio chunk of self.CHUNK samples and add it to
			self._chunks_queue.
		"""
		self._chunks_queue.put(self._stream.read(self.CHUNK))
		self._remove_chunk_if_needed()
		self._logger.debug('{} (aud)'.format(self._chunks_queue.qsize()))


	def _remove_chunk_if_needed(self):
		"""
			Removes an element from self._chunks_queue if it reached its
			max length.
		"""
		if self._chunks_queue.qsize() > self._context.FPS * self._context.RECORDING_TIME:
			self._chunks_queue.get()

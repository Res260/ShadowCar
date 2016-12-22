"""
    @file        AudioManager
    @description 
    @author      Res260 
    @created_at  20161221
    @updated_at  20161221
"""
import time
import pyaudio as pa

class AudioManager:
	"""
		Class that manage the audio for the app.
	"""

	def __init__(self, context, logger):
		"""
			Creates a new instance of AudioManager.

			:param context: The ShadowCar object that created `self`
			:param logger:  The logger instance of the app.
		"""
		self._context = context
		self._logger = logger
		self._pyaudio = pa.PyAudio()

	def start(self):
		while not self._context.is_running:
			pass

		while self._context.is_running:
			initial_time = time.time()
			self._logger.debug('Audio loop')
			self._capture_audio_chunk()
			while (time.time() - initial_time) < 1 / self._context.FPS:
				pass

	def _capture_audio_chunk(self):
		pass

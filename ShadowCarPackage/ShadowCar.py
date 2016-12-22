"""
	@file        main.py
	@description
	@author      Res260
	@created_at  20161219
	@updated_at  20161219
"""
import datetime
import logging
import time
from threading import Thread

from ShadowCarPackage.AudioManager import AudioManager
from ShadowCarPackage.VideoManager import VideoManager


class ShadowCar:
	"""
		Class that manages the app.
	"""

	FPS = 8
	RECORDING_TIME = 5  # In seconds

	def __init__(self):
		"""
			Creates a new instance of ShadowCarPackage.
		"""
		self._logger = None
		self._instanciate_logger()
		self._video_manager = VideoManager(self, self._logger)
		self._video_thread = None
		self._audio_manager = AudioManager(self, self._logger)
		self._audio_thread = None
		self.is_running = False


	def start(self):
		"""
			Starts the recording.

			:return: None
		"""
		self._video_thread = Thread(target=self._video_manager.start)
		self._audio_thread = Thread(target=self._audio_manager.start)
		self._video_thread.start()
		self._audio_thread.start()
		self.is_running = True

	def _instanciate_logger(self):
		"""
			Instantiate and configure the logger object to use in the app.

			:return: None
		"""
		self._logger = logging.getLogger('main')
		self._logger.setLevel(logging.DEBUG)
		self._logger.addHandler(logging.StreamHandler())


	@staticmethod
	def get_output_file_name():
		"""
			:return: A string formatted using
					 this format: save_%Y%m%d_%H-%M-%S.avi
		"""
		return 'save_{}.avi'.format(
				datetime.datetime.fromtimestamp(time.time())
					.strftime('%Y%m%d_%H-%M-%S'))


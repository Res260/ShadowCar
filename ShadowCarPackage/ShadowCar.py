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
import subprocess as sp
from threading import Thread

import ShadowCarPackage
from ShadowCarPackage.AudioManager import AudioManager
from ShadowCarPackage.VideoManager import VideoManager


class ShadowCar:
	"""
		Class that manages the app.
	"""

	FPS = 8
	RECORDING_TIME = 3  # In seconds

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
		self._input_thread = None
		self.is_running = False


	def start(self):
		"""
			Starts the recording.

			:return: None
		"""
		self._video_thread = Thread(target=self._video_manager.run)
		self._audio_thread = Thread(target=self._audio_manager.run)
		self._input_thread = Thread(target=self._run)
		self._video_thread.start()
		self._audio_thread.start()
		self.is_running = True
		self._input_thread.start()

	def _instanciate_logger(self):
		"""
			Instantiate and configure the logger object to use in the app.

			:return: None
		"""
		self._logger = logging.getLogger('main')
		self._logger.setLevel(logging.INFO)
		self._logger.addHandler(logging.StreamHandler())


	def _run(self):
		while self.is_running:
			if self._audio_manager._chunks_queue.qsize() > 23 and\
				self._video_manager._frames_queue.qsize() > 23:
				self.is_running = False
		self._video_thread.join()
		self._audio_thread.join()
		sp.Popen('ffmpeg -i save.avi -i save.wav -c:v copy -c:a aac -strict experimental final.avi')


	@staticmethod
	def get_output_file_name(file_type):
		"""
			:param file_type: either the constant VIDEO or AUDIO defined
			             in __init__.py
			:return: A string formatted using
					 this format: save_%Y%m%d_%H-%M-%S.(avi|wav)
					 *Depending on 'file_type'*
		"""
		file_extension = 'avi' if file_type == ShadowCarPackage.VIDEO else 'wav'
		return 'save.' + file_extension
		#return 'save_{}.{}'.format(
		#						datetime.datetime.fromtimestamp(time.time())
		#							.strftime('%Y%m%d_%H-%M-%S'),
		#						file_extension)


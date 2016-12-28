"""
	@file        main.py
	@description
	@author      Res260
	@created_at  20161219
	@updated_at  20161219
"""
import datetime
import glob
import logging
import os
import time
import subprocess as sp
from threading import Thread

import ShadowCarPackage
from ShadowCarPackage.AudioManager import AudioManager
from ShadowCarPackage.UnplugTrigger import UnplugTrigger
from ShadowCarPackage.VideoManager import VideoManager


class ShadowCar:
	"""
		Class that manages the app.
	"""

	FPS = 8
	RECORDING_TIME = 30  # In seconds
	TEMP_FOLDER = 'tmp/'
	SAVE_FOLDER = 'saves/'

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
		self._trigger_manager = None
		self.is_running = False


	def start(self):
		"""
			Starts the recording. Also creates the temp and save folders if
			necessary.
		"""
		self.create_app_folders()

		self._logger.info('Starting the recording.')

		self._video_thread = Thread(target=self._video_manager.run)
		self._audio_thread = Thread(target=self._audio_manager.run)
		self._input_thread = Thread(target=self._run)
		self._video_thread.start()
		self._audio_thread.start()
		self.is_running = True
		self._input_thread.start()


	def _run(self):
		"""
			Listens for trigger to save the input, then mixes the audio and the
			video using ffmpeg.
		"""
		self._trigger_manager = UnplugTrigger(self._audio_manager,
		                                      self._logger)
		self._trigger_manager.start_listening()
		while not self._trigger_manager.is_triggered():
			time.sleep(0.1)
		self.is_running = False
		self._logger.info('Waiting on saves to complete...')
		self._video_thread.join()
		self._audio_thread.join()
		self.mix_audio_and_video()


	def _instanciate_logger(self):
		"""
			Instantiate and configure the logger object to use in the app.
		"""
		self._logger = logging.getLogger('main')
		self._logger.setLevel(logging.DEBUG)
		self._logger.addHandler(logging.StreamHandler())


	def mix_audio_and_video(self):
		"""
			Mixes the saved audio and video files, then deletes the
			unmixed files.
		"""
		self._logger.info('Starting ffmpeg...')
		sp.run('ffmpeg -v 0 -i {0} -i {1} -c:v copy '
		         '-c:a aac -strict experimental {2}'
		         .format(self.TEMP_FOLDER + self._video_manager.output_file_name,
		                 self.TEMP_FOLDER + self._audio_manager.output_file_name,
		                 self.SAVE_FOLDER + self._video_manager.output_file_name))
		self._logger.info('Save done. Output file: {}'
		                  .format(self._video_manager.output_file_name))
		self._logger.info('Cleaning the temp folder...')
		for file in glob.glob(self.TEMP_FOLDER + '*'):
			os.remove(file)


	def create_app_folders(self):
		"""
			Creates the temp and saves folders if they don't exist.
		"""
		if not os.path.exists(self.TEMP_FOLDER):
			os.makedirs(self.TEMP_FOLDER)
		if not os.path.exists(self.SAVE_FOLDER):
			os.makedirs(self.SAVE_FOLDER)


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
		return 'save_{}.{}'.format(
								datetime.datetime.fromtimestamp(time.time())
									.strftime('%Y%m%d_%H-%M-%S'),
								file_extension)

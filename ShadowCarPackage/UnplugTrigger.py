"""
    @file        UnplugTrigger
    @author      Res260 
    @created_at  20161228
    @updated_at  20161228
"""
from threading import Thread
import cv2
import time

from ShadowCarPackage.TriggerManager import TriggerManager


class UnplugTrigger(TriggerManager):
	"""
		TriggerManager that triggers when the device's mic has been unplugged.
	"""

	def __init__(self, audio_manager, logger):
		super().__init__(logger)
		self._logger.info('Creating UnplugTrigger...')
		self._audio_manager = audio_manager
		self._is_triggered = False
		self.listen_thread = Thread(target=self._run)


	def start_listening(self):
		self.listen_thread.start()


	def is_triggered(self):
		return self._is_triggered


	def _run(self):
		"""
			Checks if the audio wire has been unplugged and sets
			self._is_triggered to True when it is.
		"""
		while not self._audio_manager.is_closed:
			time.sleep(0.1)
		self._is_triggered = True
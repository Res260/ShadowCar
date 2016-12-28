"""
    @file        TriggerManager
    @description 
    @author      Res260 
    @created_at  20161226
    @updated_at  20161226
"""

from abc import ABCMeta, abstractmethod

class TriggerManager(metaclass=ABCMeta):
	"""
		Abstract class for trigger managers.
	"""

	def __init__(self, logger):
		"""
			:param logger: The logger instance for the app.
		"""
		self._logger = logger


	@abstractmethod
	def start_listening(self):
		"""
			Starts listening to a trigger.
		"""
		pass

	@abstractmethod
	def is_triggered(self):
		"""
			:return: True if the trigger has been fired.
		"""
		pass

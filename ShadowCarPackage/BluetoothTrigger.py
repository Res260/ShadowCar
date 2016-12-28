"""
    @file        BluetoothTrigger
    @description NOT WORKING AT ALL
    @author      Res260 
    @created_at  20161226
    @updated_at  20161226
"""
from threading import Thread

import bluetooth as bt
import socket as s
import sys

import time

from ShadowCarPackage.TriggerManager import TriggerManager


class BluetoothTrigger(TriggerManager):
	"""
		Trigger that connects to a Bluetooth device and listens for a trigger.
		NOT WORKING AT ALL
	"""

	PHONE_ADDRESS = '24:da:9b:0a:ef:df'
	COMP_ADDR =     '00:1b:10:00:2a:ec' #ec:2a:00:10:1b:00'

	def __init__(self, logger):
		super().__init__(logger)
		self._logger.info('Creating BluetoothTrigger...')
		self._is_triggered = False
		self._socket = None
		self._client = None
		self.listen_thread = Thread(target=self._run)


	def start_listening(self):
		#nearby_devices = bt.discover_devices()
		self._socket = s.socket(s.AF_BLUETOOTH, s.SOCK_STREAM, s.BTPROTO_RFCOMM)
		#self._socket.connect((self.PHONE_ADDRESS, 3))
		# self._socket.listen(1)
		self._logger.debug('BT socket.')
		self.listen_thread.start()


	def is_triggered(self):
		return self._is_triggered


	def _run(self):
		try:
			self._socket.connect((self.PHONE_ADDRESS, 3))
			while 1:
				self._logger.warning('hihi')
				self._socket
				self._logger.warning('hihi2')
				time.sleep(1)
		except:
			self._logger.warning(sys.exc_info()[1])
			self._socket.close()

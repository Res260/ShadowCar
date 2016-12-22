"""
    @file        AudioManager
    @description 
    @author      Res260 
    @created_at  20161221
    @updated_at  20161221
"""
import pyaudio as pa

class AudioManager:
	def __init__(self, context, logger):
		self._context = context
		self._logger = logger
		self._pyaudio = pa.PyAudio()

	def start(self):
		pass
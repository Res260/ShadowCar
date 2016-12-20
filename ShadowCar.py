"""
	@file        main.py
	@description
	@author      Res260
	@created_at  20161219
	@updated_at  20161219
"""
import datetime
import cv2
import time
import logging
import queue as q

class ShadowCar:
	"""
		Class that manages the app.
	"""

	def __init__(self):
		"""
			Creates a new instance of ShadowCar.
		"""
		self._logger = None
		self._queue  = q.Queue()
		self._instanciate_logger()

	def start(self):
		cap = cv2.VideoCapture(0)

		if not cap.isOpened():
			self._logger.info('Capture device not found.')
		else:
			self._logger.info('Capture starting.')
			while True:
				initial_time = time.time()
				# Capture frame-by-frame
				ret, frame = cap.read()
				self._queue.put(frame)

				# Display the resulting frame
				text = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
				cv2.putText(frame, text, (50,50), 0, 1, (255, 255, 255), lineType=5)
				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					self._save()
				if self._queue.qsize() > 200:
					self._queue.get()
				print(self._queue.qsize())
				time.sleep(max(0.1 - (time.time() - initial_time), 0))


	def _instanciate_logger(self):
		"""
			Instantiate and configure the logger object to use in the app.
			:return: None
		"""
		self._logger = logging.getLogger('main')
		self._logger.setLevel(logging.DEBUG)
		self._logger.addHandler(logging.StreamHandler())


	def _save(self):
		"""
			Saves the recorded video as an .avi file.
			:param queue: The queue of video frames to use for the video.
			:return: None
		"""
		self._logger.info('Saving...')
		output_file_name = self._get_output_file_name()
		video_writer = cv2.VideoWriter(output_file_name,
			cv2.VideoWriter_fourcc(*'DIVX'),
			10.0,
			(640, 480)
		)
		self._write_frames(video_writer)
		video_writer.release()
		self._logger.info('Saved {}.'.format(output_file_name))


	def _write_frames(self, video_writer):
		"""
			Writes the frames in the queue using video_writer.
			:param video_writer: The cv2.VideoWriter instance.
			:return: None
		"""
		while self._queue.qsize() > 0:
			self._logger.info('{} frame(s) left.'.format(self._queue.qsize()))
			video_writer.write(self._queue.get())


	@staticmethod
	def _get_output_file_name():
		"""
			:return: A string formatted using
					 this format: save_%Y%m%d_%H-%M-%S.avi
		"""
		return 'save_{}.avi'.format(
				datetime.datetime.fromtimestamp(time.time())
					.strftime('%Y%m%d_%H-%M-%S'))


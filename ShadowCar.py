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
		self._instanciate_logger()
		self._queue  = q.Queue()
		self._video_capture = cv2.VideoCapture(0)
		if not self._video_capture.isOpened():
			self._logger.error('Capture device not found.')
			exit(255)
		else:
			self._logger.info('Capture device found: {}'.format(self._video_capture.get(cv2.CAP_PROP_FPS  )))
		self._camera_height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self._camera_width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)


	def start(self):

			while True:
				initial_time = time.time()
				# Capture frame-by-frame
				ret, frame = self._video_capture.read()
				self._queue.put(frame)

				# Display the resulting frame
				self._add_timestamp_to_frame(frame,
				                             datetime.datetime.fromtimestamp(
						                             time.time()).strftime(
					                                    '%Y-%m-%d %H:%M:%S'))
				cv2.imshow('frame', frame)
				if cv2.waitKey(1) & 0xFF == ord('q'):
					self._save()
				if self._queue.qsize() > 200:
					self._queue.get()
				print(self._queue.qsize())
				time.sleep(max(0.1 - (time.time() - initial_time), 0))

	def _add_timestamp_to_frame(self, frame, timestamp):
		"""
			Adds a small timestamp to the bottom-right of a frame.

			:param frame: The cv2 frame in question
			:param timestamp: the string to add.
			:return: None
		"""
		cv2.rectangle(frame,
		              (int(self._camera_width) - 175, int(self._camera_height) - 20),
		              (int(self._camera_width) - 10,
		               int(self._camera_height) - 10),
		              (0, 0, 0, 0.2),
		              thickness=-1 # Filled
		)
		cv2.putText(frame,
		            timestamp,
	                (   int(self._camera_width) - 175,
		                int(self._camera_height) - 10),
		            2,
		            0.45,
		            (255, 255, 255)
		)

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
			(self._camera_width, self._camera_height)
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


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
import pyaudio as pa

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
		self._frames_queue = q.Queue()
		self._FPS = 8
		self._RECORDING_TIME = 300 # In seconds
		self._video_capture = cv2.VideoCapture(0)
		if not self._video_capture.isOpened():
			self._logger.error('Capture device not found.')
			exit(255)
		else:
			self._logger.info('Capture device found: {}'.format(self._video_capture.get(cv2.CAP_PROP_FPS  )))
		self._camera_height = self._video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)
		self._camera_width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)


	def start(self):
		"""
			Starts the recording.

			:return: None
		"""

		while True:
			initial_time = time.time()
			self._capture_video_frame()
			time.sleep(max(
				(self._FPS / 100) - ((time.time() - initial_time) / 100),
				0))

	def _capture_video_frame(self):
		"""
			Captures a video frame and deals with it accordingly.

			:return: None
		"""

		# Capture frame-by-frame
		ret, frame = self._video_capture.read()
		self._frames_queue.put(frame)
		# Display the resulting frame
		self._add_timestamp_to_frame(frame,
		                             datetime.datetime.fromtimestamp(
				                             time.time()).strftime(
				                             '%Y-%m-%d %H:%M:%S'))
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			self._save()
		self._remove_frame_if_needed()
		print(self._frames_queue.qsize())  # To remove

	def _save(self):
		"""
			Saves the recorded video as an .avi file.

			:return: None
		"""
		self._logger.info('Saving...')
		output_file_name = self._get_output_file_name()
		video_writer = cv2.VideoWriter(output_file_name,
			cv2.VideoWriter_fourcc(*'DIVX'),
			self._FPS,
			(int(self._camera_width), int(self._camera_height))
		)
		self._write_frames(video_writer)
		video_writer.release()
		self._logger.info('Saved {}.'.format(output_file_name))


	def _remove_frame_if_needed(self):
		"""
			Removes an element from self._frames_queue if it reached
			it's max length.

			:return: None
		"""
		if self._frames_queue.qsize() > self._FPS * self._RECORDING_TIME:
			self._frames_queue.get()


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
		              (0, 0, 0),
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


	def _write_frames(self, video_writer):
		"""
			Writes the frames in the queue using video_writer.
			:param video_writer: The cv2.VideoWriter instance.
			:return: None
		"""
		while self._frames_queue.qsize() > 0:
			self._logger.info('{} frame(s) left.'.format(self._frames_queue.qsize()))
			video_writer.write(self._frames_queue.get())


	@staticmethod
	def _get_output_file_name():
		"""
			:return: A string formatted using
					 this format: save_%Y%m%d_%H-%M-%S.avi
		"""
		return 'save_{}.avi'.format(
				datetime.datetime.fromtimestamp(time.time())
					.strftime('%Y%m%d_%H-%M-%S'))


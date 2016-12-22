"""
    @file        VideoManager
    @description 
    @author      Res260 
    @created_at  20161221
    @updated_at  20161221
"""

import datetime
import time
import cv2
import queue as q


class VideoManager:
	"""
			Class that manage the video for the app.
	"""

	def __init__(self, context, logger):
		"""
			Creates a new instance of VideoManager.

			:param context: The ShadowCar object that created `self`
			:param logger:  The logger instance of the app.
		"""
		self._context = context
		self._logger = logger
		self._frames_queue = q.Queue()
		self._timestamps_queue = q.Queue()
		self._video_capture = cv2.VideoCapture(0)
		if not self._video_capture.isOpened():
			self._logger.error('Capture device not found.')
			exit(255)
		else:
			self._logger.info('Capture device found: {}'.format(self._video_capture.get(cv2.CAP_PROP_FPS)))
		self._camera_height = self._video_capture.get(
				cv2.CAP_PROP_FRAME_HEIGHT)
		self._camera_width = self._video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)


	def start(self):
		"""
			Starts the recording.

			:return: None
		"""
		while not self._context.is_running:
			pass

		while self._context.is_running:
			initial_time = time.time()
			self._logger.debug('Video loop')
			self._timestamps_queue.put(initial_time)
			self._capture_video_frame()
			while (time.time() - initial_time) < 1 / self._context.FPS:
				pass

	def _capture_video_frame(self):
		"""
			Captures a video frame and deals with it accordingly.

			:return: None
		"""

		# Capture frame-by-frame
		ret, frame = self._video_capture.read()
		self._frames_queue.put(frame)
		# Display the resulting frame
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
		output_file_name = self._context.get_output_file_name()
		video_writer = cv2.VideoWriter(output_file_name,
			cv2.VideoWriter_fourcc(*'DIVX'),
			self._context.FPS,
			(int(self._camera_width), int(self._camera_height))
		)
		self._write_frames(video_writer)
		video_writer.release()
		self._logger.info('Saved {}.'.format(output_file_name))


	def _remove_frame_if_needed(self):
		"""
			Removes an element from self._frames_queue and
			self._timestamps_queue if it reached its max length.

			:return: None
		"""
		if self._frames_queue.qsize() > self._context.FPS * self._context.RECORDING_TIME:
			self._frames_queue.get()
			self._timestamps_queue.get()


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


	def _write_frames(self, video_writer):
		"""
			Writes the frames in the queue using video_writer. Adds a
			timestamp to each frame as well.

			:param video_writer: The cv2.VideoWriter instance.
			:return: None
		"""
		while self._frames_queue.qsize() > 0:
			self._logger.info('{} frame(s) left.'.format(self._frames_queue.qsize()))
			frame = self._frames_queue.get()
			self._add_timestamp_to_frame(frame, datetime.datetime.fromtimestamp(
											    self._timestamps_queue.get()).strftime(
				                                '%Y-%m-%d %H:%M:%S'))
			video_writer.write(frame)

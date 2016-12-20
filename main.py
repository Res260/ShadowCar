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

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())

def save(queue):
	logger.info('saving...')
	fourcc = cv2.VideoWriter_fourcc(*'DIVX')
	saver = cv2.VideoWriter('save_{}.avi'.format(datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H-%M-%S')), fourcc, 10.0, (640,480))
	while queue.qsize() > 0:
		logger.info(queue.qsize())
		saver.write(queue.get())
	logger.info('saved1...')
	saver.release()
	logger.info('saved...')

cap = cv2.VideoCapture(0)

if not cap.isOpened():
	logger.info('Capture device not found.')
else:
	logger.info('Capture starting.')
	queue = q.Queue()
	while True:
		initial_time = time.time()
		# Capture frame-by-frame
		ret, frame = cap.read()
		queue.put(frame)

		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			save(queue)
		if queue.qsize() > 200:
			queue.get()
		print(queue.qsize())
		time.sleep(max(0.1 - (time.time() - initial_time), 0))

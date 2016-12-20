"""
	@file        main.py
	@description
	@author      Res260
	@created_at  20161219
	@updated_at  20161219
"""

import cv2
import time
import logging

logger = logging.getLogger('main')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
cap = cv2.VideoCapture(0)

if not cap.isOpened():
	logger.info('Capture device not found.')
else:
	logger.info('Capture starting.')
	while True:
		initial_time = time.time()
		# Capture frame-by-frame
		ret, frame = cap.read()

		# Display the resulting frame
		cv2.imshow('frame', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		time.sleep(max(0.1 - (time.time() - initial_time), 0))

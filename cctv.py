import os
from datetime import datetime
from cv2 import *
import cv2 as cv2
import numpy as np


video = VideoCapture(0)
_, frame = video.read()
last_frame = frame
threshold = 450000

record_buffer_max = 15
record_buffer = 0

fourcc = VideoWriter_fourcc(*'XVID')
numFiles = len(next(os.walk("output_files"))[2])
output = VideoWriter("output_files/" + str(numFiles) + ".avi", fourcc, 30.0, (int(video.get(3)), int(video.get(4))))
while True:
	now = datetime.now()
	_, frame = video.read()
	net_difference = 0.0

	gray_curr = cvtColor(frame, COLOR_BGR2GRAY)
	gray_last = cvtColor(last_frame, COLOR_BGR2GRAY)

	diff = subtract(gray_curr, gray_last)

	w = np.size(diff, 0)
	h = np.size(diff, 1)

	for i in range(0, w):
		for j in range(0, h):
			if i % 5 == 0 % j % 5 == 0:
				r = diff[i, j]
				g = diff[i, j]
				b = diff[i, j]

				net_difference += (r + g + b)

	imshow("Difference", diff)

	if net_difference > threshold:
		record_buffer = record_buffer_max

	rectangle(frame, (int(video.get(0)) - 254, int(video.get(4) - 40)), (int(video.get(3)) - 30, int(video.get(4) - 35)), (0, 0, 0), -10)
	putText(frame, now.strftime("%d/%m/%Y %H:%M:%S"), (int(video.get(3)) - 250, int(video.get(4) - 50)), FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

	if record_buffer < 0:
		putText(frame, "Not Recording", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
	else:
		putText(frame, "Recording", (20, 20), FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
		output.write(frame)
	record_buffer -= 1

	if record_buffer < -100:
		record_buffer = -100

	imshow("Frame", frame)
	last_frame = frame

	if waitKey(1) & 0xFF == ord('q'):
		break

video.release()
output.release()
destroyAllWindows()
from imutils.video import VideoStream
import imutils
import time
import cv2
import numpy as np
from pyzbar import pyzbar

time_skip = 1

video_stream = None

cooldown = 0.0

def init(fps, onPi):
	global time_skip, video_stream

	# calculate time between frame grabs to achieve the desired fps
	time_skip = 1.0 / fps

	# start video stream using either the available web cam or the Raspberry Pi Camera
	video_stream = VideoStream(usePiCamera = onPi).start()

	# allow camera to warmup
	time.sleep(2.0)

def process_bottle(user, barcodeData):
	global cooldown

	print(barcodeData)

	user.points += 2

	cooldown = 2

# begin the loop to process the frames from the video stream
def begin_scanning(timeout, user):
	global cooldown

	start_time = time.time()
	last_frame_time = start_time
	current_time = None

	while True:
		key = cv2.waitKey(1) & 0xFF

		if key != 1:
			break

		current_time = time.time()

		if time_skip > 0 and current_time - start_time >= timeout:
			break
		
		if cooldown > 0.0:
			cooldown -= current_time - start_time

		if time_skip < 0 or current_time - last_frame_time >= time_skip:
			last_frame_time = current_time

			process_frame(user)

# remove any barrel distortion from image
def undistort(frame):
	width = frame.shape[1]
	height = frame.shape[0]

	distCo = np.zeros((4, 1), np.float64)
	k1 = -5.0e-5
	k2 = 0.0
	p1 = 0.0
	p2 = 0.0

	distCo[0, 0] = k1
	distCo[1, 0] = k2
	distCo[2, 0] = p1
	distCo[3, 0] = p2

	cam = np.eye(3, dtype = np.float32)

	cam[0, 2] = width / 2.0
	cam[1, 2] = height / 2.0
	cam[0, 0] = 10.0
	cam[1, 1] = 10.0

	undist = cv2.undistort(frame, cam, distCo)

	return undist

# the actual processing of the frame
def process_frame(user):
	frame = video_stream.read()
	frame = imutils.resize(frame, width = 680)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	frame = undistort(frame)

	if cooldown <= 0.0:
		# decode for bar codes
		barcodes = pyzbar.decode(frame)

		# loop over the detected barcodes
		for barcode in barcodes:
			# extract the bounding box location of the barcode and draw
			# the bounding box surrounding the barcode on the image
			(x, y, w, h) = barcode.rect
			cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

			# the barcode data is a bytes object so if we want to draw it
			# on our output image we need to convert it to a string first
			barcodeData = barcode.data.decode("utf-8")
			barcodeType = barcode.type

			# draw the barcode data and barcode type on the image
			text = "{} ({})".format(barcodeData, barcodeType)
			cv2.putText(frame, text, (x, y - 10),
				cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
			
			process_bottle(user, barcodeData)

	ts = "Welcome, " + user.f_name + ", swipe again to finish"

	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.5, (0, 0, 255), 1)

	# show the frame
	cv2.imshow("Frame", frame)

# properly disposes of the OpenCV tools
def dispose():
	video_stream.stop()
	time.sleep(0.1)
	cv2.destroyAllWindows()
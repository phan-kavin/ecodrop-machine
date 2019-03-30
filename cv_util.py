from imutils.video import VideoStream
import imutils
import time
import cv2
from pyzbar import pyzbar

time_skip = 1

video_stream = None

def init(fps, onPi):
	global time_skip, video_stream

	# calculate time between frame grabs to achieve the desired fps
	time_skip = 1.0 / fps

	# start video stream using either the available web cam or the Raspberry Pi Camera
	video_stream = VideoStream(usePiCamera = onPi).start()

	# allow camera to warmup
	time.sleep(2.0)

# begin the loop to process the frames from the video stream
def begin_scanning(timeout, iso):
	start_time = time.time()
	last_frame_time = start_time
	current_time = None

	while True:
		key = cv2.waitKey(1) & 0xFF

		if key == ord('q'):
			break

		current_time = time.time()

		if current_time - start_time >= timeout:
			break

		if current_time - last_frame_time >= time_skip:
			last_frame_time = current_time

			process_frame(iso)

# the actual processing of the frame
def process_frame(iso):
	# grab the frame from the threaded video stream and resize it
	# to have a maximum width of 800 pixels
	frame = video_stream.read()
	frame = imutils.resize(frame, width=512)
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# decode for bar codes
	barcodes = pyzbar.decode(frame)

	print(len(barcodes))

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

	ts = "iso: " + iso

	cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
		0.75, (0, 0, 255), 1)

	# show the frame
	cv2.imshow("Frame", frame)

# properly disposes of the OpenCV tools
def dispose():
	video_stream.stop()
	time.sleep(0.1)
	cv2.destroyAllWindows()
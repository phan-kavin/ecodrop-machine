import os

import fb_util
import card_util
import cv_util

def on_pi():
	_, nodename, _, _, _ = os.uname()

	if nodename == "raspberrypi":
		return True
	else:
		return False

# initialize everything else
fb_util.init()
print("Firebase done initializing")

card_util.init()
print("Card swiper done initializing")

cv_util.init(fps = 30, onPi = on_pi())
print("OpenCV done initializing")

# begin program
while True:
	# need to authenticate users first
	# probably update display right here

	print("reading card now")
	iso = card_util.read_card()

	cv_util.begin_scanning(timeout = 99999999, iso = iso)

	break


cv_util.dispose()
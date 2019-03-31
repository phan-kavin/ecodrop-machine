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

cv_util.init(fps = -1, onPi = on_pi())
print("OpenCV done initializing")

# begin program
while True:
	# need to authenticate users first
	# probably update display right here

	print("reading card now")
	iso = card_util.read_card()

	user = fb_util.get_user(iso)

	cv_util.begin_scanning(timeout = 30, user = user)

	fb_util.update_user(iso, user)

cv_util.dispose()
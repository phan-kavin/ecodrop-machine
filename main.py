import fb_util
import card_util
import cv_util

import time

# initialize everything else
fb_util.init()
print("Firebase done initializing")

card_util.init()
print("Card swiper done initializing")

cv_util.init(fps = 10, onPi = False)
print("OpenCV done initializing")

# begin program
while True:
	# need to authenticate users first
	# probably update display right here

	print("reading card now")
	iso = card_util.read_card()

	cv_util.begin_scanning(timeout = 10000, iso = iso)

	break


cv_util.dispose()
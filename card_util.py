from pynput.keyboard import Key, Listener
from pynput.keyboard._xorg import KeyCode

from queue import Queue

# the keyboard listener
listener = None

# the key event queue
key_queue = None

# will only listen for cards when set to True
enabled = False

# called when the enter key is hit
# joins the digits within iso_buffer to a string
# returns a string containing an iso
# blocks thread until an iso is read
def read_card():
	# enable the key listener and reset state
	enable()

	# holds numbers entered by the card swiper
	iso_buffer = []

	while True:
		item = key_queue.get()

		if item == None:
			# item is null? pass
			pass
		elif item == "enter":
			# iso is done reading, break while loop
			key_queue.task_done()
			break
		else:
			# received a digit, appending to iso_buffer
			iso_buffer.append(item)
			key_queue.task_done()

	# join is a method of str,
	# so it can only be used on strings!
	iso = "".join(iso_buffer)
	iso = iso[6:]
	iso_buffer.clear()
	# print("read iso: {}".format(iso)

	# disable key listener and reset state again (just to be safe)
	disable()

	return iso

# listener method for keyboard events
# used to grab keys entered by the card swiper
def on_press(key):
	if enabled:
		if key == Key.enter:
			# pass the keycode to the queue so read_card knows when to stop appending digits
			key_queue.put("enter")
		else:
			# when KeyCode is formatted it returns 'x' where x is the actual key
			keyToChar = "{}".format(key)[1]

			# only append if a digit
			if keyToChar.isdigit():
				key_queue.put(keyToChar)
			else:
				print("unknown key caught! key: {}".format(key))
	else:
		return True

# start keyboard listener
# won't be enabled unless enable() is called!
def init():
	global listener

	listener = Listener(on_press=on_press)

	listener.start()

# must be called in order to start reading a card
def enable():
	global enabled, key_queue

	enabled = True
	key_queue = Queue()

# call to reset state and disable the card reader
# note: does not actually disable the physical card reader
def disable():
	global enabled, key_queue
	
	enabled = False
	key_queue = None
import board
import neopixel
from time import sleep

DEBUG = True

if DEBUG:
	from time import time

# our strip has 60 LEDs
NUM_PIXELS = 60

# delay of 125ms between pulses
FLASH_DELAY = 125 / 1000

# long delay for error signaling. 5 seconds.
LONG_DELAY = 4

GREEN = (0, 255, 0)
RED = (255, 0, 0)
OFF = (0, 0, 0)

# the dataline is on GPIO 18
pixels = neopixel.NeoPixel(board.D18, NUM_PIXELS)

# pulse a given color for the set flash delay
def __pulse(color):
	pixels.fill(color)
	sleep(FLASH_DELAY)
	pixels.fill(OFF)
	sleep(FLASH_DELAY)

def setGreen():
	pixels.fill(GREEN)

# pulse red twice before going solid red
def errorFlash():
	__pulse(RED)
	__pulse(RED)

	if DEBUG:
		start = time()

	pixels.fill(RED)
	sleep(LONG_DELAY)

	if DEBUG:
		end = time()
		print(end - start)

	setGreen()

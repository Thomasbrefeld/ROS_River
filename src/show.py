#!/usr/bin/python3

import sys
import board
import neopixel
from PIL import Image, ImageDraw, ImageFont, ImageOps
import time

displayPin = board.D18
displayWidth = 32
displayHeight = 8
numLEDs = displayWidth * displayHeight
displayBrightness = .3
textColor = (10, 10, 10)

ORDER = neopixel.GRB
pixels = neopixel.NeoPixel(displayPin, numLEDs, auto_write=False)
roation = 0

font = ImageFont.truetype("/home/ubuntu/catkin_ws/src/ros_river/src/5x7.ttf", 16)

def getIndex(x, y):
    if x % 2 != 0:
        return (x * 8) + y
    else:
        return (x * 8) + (7 - y)

def scrollText(text, offSet):
	textWidth, textHeight = font.getsize(text)

	image = Image.new('P', (textWidth + displayWidth - 11, displayHeight), 0)
	draw = ImageDraw.Draw(image)

	draw.text((0, -1), text, font=font, fill=255)
#	image = ImageOps.mirror(image)
	image = ImageOps.flip(image)

	for x in range(displayWidth - 11):
		for y in range(displayHeight):
			if (image.getpixel((x + offSet, y)) == 255):
				pixels[getIndex(x, y)] = textColor
			else:
				pixels[getIndex(x, y)] = (0,0,0)

def status(num):
	textWidth, textHeight = font.getsize(num)

	image = Image.new('P', (textWidth, displayHeight), 0)
	draw = ImageDraw.Draw(image)
	draw.text((0, -1), num, font=font, fill=255)
	image = ImageOps.flip(image)

	loc = -1 * (textWidth - displayWidth)
	for x in range(textWidth):
		for y in range(displayHeight):
#			print(getIndex(x + loc, y))
			if (image.getpixel((x, y)) == 255):
				pixels[getIndex(x + loc, y)] = textColor
			else:
				pixels[getIndex(x + loc, y)] = (0,0,0)


def display(text, postion, statusNum):
	scrollText(text, postion)
	status(str(statusNum))
	pixels.show()

if __name__ == "__main__":
#	try:
	print('show called')
	if (len(sys.argv) == 1):
		pixels.fill(0)
		pixels.show()
	if (len(sys.argv) == 4):
		display(sys.argv[1], int(sys.argv[2]), sys.argv[3])
#	except Exception as e:
#		print('bad args', e)

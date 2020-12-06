#!/usr/bin/env python3

try:
	import sys
	import board
	import neopixel
	from PIL import Image, ImageDraw, ImageFont, ImageOps

	font = ImageFont.truetype("/home/ubuntu/catkin_ws/src/ros_river/src/5x7.ttf", 16)
	displayOrder = neopixel.GRB
	displayPin = board.D18

	class Show:
		def __init__(self, width, height, brightness = .1, color = (255, 255, 255)):
			self.width = width
			self.height = height
			self.numPixels = self.width * self.height

			self.color = color

			self.pixels = neopixel.NeoPixel(displayPin, self.numPixels, brightness=float(brightness), auto_write=False)

		def clear(self):
			self.pixels.fill(0)
			self.pixels.show()

		def show(self, text, count, status):
			count = count
			status = str(status)

			textWidth, textHeight = font.getsize(text)
			statusWidth, statusHeight = font.getsize(status)

			offset = count % (textWidth - self.width + statusWidth + 20)
			if (textWidth < self.width):
				offset = 0
			elif (offset < 10):
				offset = 0
			elif (offset > (textWidth - self.width + statusWidth + 10)):
				offset = (textWidth - self.width + statusWidth)
			else:
				offset -= 10

			textImage = Image.new('P', (textWidth + self.width - statusWidth - 1, self.height), 0)
			textdraw = ImageDraw.Draw(textImage)

			textdraw.text((0, -1), text, font=font, fill=255)
			textImage = ImageOps.flip(textImage)

			for x in range (self.width - statusWidth - 1):
				for y in range (self.height):
					if (textImage.getpixel((x + offset, y)) is 255):
						self.pixels[self.getIndex(x, y)] = self.color
					else:
						self.pixels[self.getIndex(x, y)] = (0,0,0)

			statusImage = Image.new('P', (statusWidth, self.height), 0)
			statusDraw = ImageDraw.Draw(statusImage)

			statusDraw.text((0, -1), status, font=font, fill=255)
			statusImage = ImageOps.flip(statusImage)

			loc = self.width - statusWidth
			for x in range (statusWidth):
				for y in range (self.height):
					if (statusImage.getpixel((x,y)) == 255):
						self.pixels[self.getIndex(x + loc, y)] = self.color
					else:
						self.pixels[self.getIndex(x + loc, y)] = (0,0,0)
			if (count % 2 < 1):
				self.pixels[248] = (0, 100, 0)
			else:
				self.pixels[248] = (0, 0, 0)

			self.pixels.show()

		def getIndex(self, x, y):
			if x % 2 != 0:
				return (x * 8) + y
			else:
				return (x * 8) + (7 - y)

	#width, height, brightness, text, counter, status

	if __name__ == "__main__":
		sys.argv[1] = int(sys.argv[1])
		sys.argv[2] = int(sys.argv[2])
		if (len(sys.argv) == 7):
			sys.argv[3] = float(sys.argv[3])
			sys.argv[4] = str(sys.argv[4])
			sys.argv[5] = int(sys.argv[5])
			sys.argv[6] = int(sys.argv[6])
		if (len(sys.argv) == 3):
			Show(sys.argv[1], sys.argv[2]).clear()
		if (len(sys.argv) == 7):
			Show(sys.argv[1], sys.argv[2], sys.argv[3]).show(sys.argv[4], sys.argv[5], sys.argv[6])
except KeyboardInterrupt:
	print(" keyboard Interrupt in show1.py: Exiting")
	import sys
	sys.exit(1)
except Exception as e:
	print(" show1.py failed:", e, ": Exiting")
	import sys
	sys.exit(2)

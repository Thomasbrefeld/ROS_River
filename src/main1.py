#!/usr/bin/env python

import rospy
import subprocess
import sys
import time
from std_msgs.msg import String
from std_msgs.msg import Int8
from PIL import Image, ImageDraw, ImageFont, ImageOps

__metaclass__ = type

class ROSHandler:
	text = "Wait"
	status = 1
	counter = 0

	def __init__(self):
		self.textSub = rospy.Subscriber("display_text", String, self.textCB)
		self.statusSub = rospy.Subscriber("display_status", Int8, self.statusCB)

	def textCB(self, msg):
		self.counter = 0
		self.text = str(msg.data)

	def statusCB(self, msg):
		self.counter = 0
		self.status = int(msg.data)

class DisplayHander(ROSHandler):
	exitInterrupt = False
	timeToExit = 0

	def __init__(self, width, height, brightness, rate = 8):
		super(DisplayHander, self).__init__()

		self.rate = rate

		self.displayWidth = int(width)
		self.displayHeight = int(height)
		self.brightness = float(brightness)

	def displayThread(self):
		rate = rospy.Rate(self.rate)
		while True:
			try:
				self.processStatus = subprocess.check_call(["sudo", "-H", "python3", 
						"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
						str(self.displayWidth), str(self.displayHeight),
						str(self.brightness), str(self.text),str(self.counter),
						str(self.status)])
				self.counter += 1
				rate.sleep()
			except KeyboardInterrupt:
				print(" Keyboard Interrupt in main1.py!")
				sys.exit(1)
			except subprocess.CalledProcessError:
				print(" Subprocess Error in main1.py!")
				sys.exit(self.processStatus)


if __name__ == '__main__':
    rospy.init_node('display_node')
    display = DisplayHander(32, 8, .01)
    display.displayThread()

#!/usr/bin/env python

import rospy
import subprocess
import sys
import time
from std_msgs.msg import String
from std_msgs.msg import Int8
from std_msgs.msg import Bool
from std_msgs.msg import Header
from rosgraph_msgs.msg import Log
from sensor_msgs.msg import Joy
from PIL import Image, ImageDraw, ImageFont, ImageOps

__metaclass__ = type

class ROSHandler:
	auto = True
	logOut = None #level, msg, time
	enabled = False
	last = 0
	joy = False

	text = "Wait"
	status = 1
	counter = 0

	def __init__(self):
		self.textSub = rospy.Subscriber("display/text", String, self.textCB)
		self.statusSub = rospy.Subscriber("display/status", Int8, self.statusCB)

		self.autoSub = rospy.Subscriber("display/auto", Bool, self.autoCB)
		self.rosoutSub = rospy.Subscriber("rosout", Log, self.logCB)
		self.dbwEnabledSub = rospy.Subscriber("/vehicle/dbw_enabled", Bool, self.enabledCB)
		self.joySub = rospy.Subscriber("joy", Joy, self.joyCB)

	def autoCB(self, msg):
		self.auto = bool(msg.data)

	def logCB(self, msg):
		if msg.name is "/joy_node":
			self.joy = True
			self.logOut = (msg.level, msg.msg, msg.header.stamp.to_sec())
		elif self.logOut is None or msg.level >= self.logOut[0] or rospy.Time.now().to_sec() - 11 > self.logOut[2]:
			if self.logOut is None or self.logOut[1] is msg.msg:
				self.counter = 0
			self.logOut = (msg.level, msg.msg, msg.header.stamp.to_sec())

	def enabledCB(self, msg):
		self.enabled = bool(msg.data)

	def joyCB(self, msg):
		self.joy = False

	def textCB(self, msg):
		if not self.auto:
			self.counter = 0
			self.text = str(msg.data)
		else:
			print ("Mode is set to Auto, unable to change text")

	def statusCB(self, msg):
		if not self.auto:
			self.status = int(msg.data)
		else:
			print ("Mode is set to Auto, unable to change status")

class DisplayHander(ROSHandler):
	exitInterrupt = False
	timeToExit = 0

	def __init__(self, width, height, brightness):
		super(DisplayHander, self).__init__()

		self.displayWidth = int(width)
		self.displayHeight = int(height)
		self.brightness = float(brightness)

	def displayRun(self):
		if self.auto:
			self.displayThreadAuto()
			#print((self.logOut), rospy.Time.now().to_sec() - self.logOut[2], self.counter, self.enabled)
		else:
			self.displayThreadManual()
		self.counter += 3

	def displayThreadManual(self):
		self.processStatus = subprocess.check_call(["sudo", "-H", "python3", 
			"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
			str(self.displayWidth), str(self.displayHeight),
			str(self.brightness), str(self.text),str(self.counter),
			str(self.status)])

	def displayThreadAuto(self):
		if self.logOut is None:
			print("starting")
			return
		#print(rospy.Time.now().to_sec() - self.logOut[2])
		#if last message is less then 15 seconds old and the level is greater then 4
		if rospy.Time.now().to_sec() - self.logOut[2] < 11 and self.logOut[0] >= 4 or self.joy:
			if not self.last is 0:
				self.last = 0
				self.counter = 0
			self.processStatus = subprocess.check_call(["sudo", "-H", "python3",
				"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
				str(self.displayWidth), str(self.displayHeight),
				str(self.brightness), str(self.logOut[1]),str(self.counter),
				str(self.logOut[0])])
		elif self.enabled:
			if not self.last is 1:
				self.last = 1
				self.counter = 0
			self.processStatus = subprocess.check_call(["sudo", "-H", "python3",
				"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
				str(self.displayWidth), str(self.displayHeight),
				str(self.brightness), str("Joy Stick"),str(self.counter),
				str(0)])
		else:
			if not self.last is 2:
				self.last = 2
				self.counter = 0
			self.processStatus = subprocess.check_call(["sudo", "-H", "python3",
				"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
				str(self.displayWidth), str(self.displayHeight),
				str(self.brightness), str("Manual"),str(self.counter),
				str(0)])

if __name__ == '__main__':
	try:
		rospy.init_node('display_node')
		display = DisplayHander(32, 8, .01)
#		rate = rospy.Rate(32)
		while not rospy.is_shutdown():
			display.displayRun()
#			rate.sleep()
	except KeyboardInterrupt:
		print("Keyboard Interrupt  Exit")
	except subprocess.CalledProcessError:
		print("Subproces Exit")
		sys.exit(self.processStatus)
	except Exception as e:
		print("Uncought Error:", e)
	finally:
		print("Main1 Exit")
		sys.exit(1)

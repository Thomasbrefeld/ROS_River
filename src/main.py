#!/usr/bin/env python
import rospy
import subprocess
from std_msgs.msg import String
from std_msgs.msg import Int8

from PIL import Image, ImageDraw, ImageFont, ImageOps
displayWidth = 32
displayHeight = 8
numLEDs = displayWidth * displayHeight
font = ImageFont.truetype("/home/ubuntu/catkin_ws/src/ros_river/src/5x7.ttf", 16)
textWidth, textHeight = font.getsize("Waiting")

text = {
	"msg" : "Waiting",
	"postion" : 0,
	"size" : textWidth
}
status = str(0)

def stringCB(msg):
	global text
	textWidth, textHeight = font.getsize(msg.data)
	text["msg"] = msg.data
	text["postion"] = 0
	text["size"] = textWidth

def statusCB(msg):
	global status
	status = str(msg.data)

if __name__ == '__main__':
	rospy.init_node('display_node')
	#rospy.loginfo('display node has started')
	rospy.Subscriber("display_text", String, stringCB)
	rospy.Subscriber("display_status", Int8, statusCB)

	rate = rospy.Rate(4)
	while not rospy.is_shutdown():
		try:
			subprocess.Popen(["sudo", "-H", "python3", "/home/ubuntu/catkin_ws/src/ros_river/src/show.py", text["msg"], str(text["postion"]), status]).wait()
		except KeyboardInterrupt:
			break
		except:
			text["postion"] = 0
		text["postion"] += 1
		if (text["postion"] > text["size"] - displayWidth + 11):
			text["postion"] = 0
		rate.sleep()
	#rospy.loginfo('display node has exited')

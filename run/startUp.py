import os
import sys
import time
import socket
import fcntl
import struct
import psutil
import rosgraph
import signal
import subprocess

def isROS():
	try:
		rosgraph.Master('/rostopic').getPid()
		return True
	except:
		return False


mainProcess = None
rosProcess = None
coutner = 0

try:
	while True:
		if isROS():
			if not rosProcess is None:
				rosProcess.kill()
				rosProcess = None
			if mainProcess is None:
				print('ROS River running')
				mainProcess = subprocess.Popen('exec ' + 'rosrun ros_river main1.py', stdout = subprocess.PIPE, shell = True)
		else:
			if not mainProcess is None:
				mainProcess.kill()
				mainProcess = None
			if rosProcess is None:
				print('Waiting for master')
				counter = 0
			else:
				rosProcess.wait()
			rosProcess = subprocess.Popen("sudo " + "-H " + "python3 " +
						"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py " + " " +
						str(32) + " " + str(8) + " "  + str(.01) + " 'ROS Connection Error' " + str(counter) + " " + str(2), stdout = subprocess.PIPE, shell = True)
			counter += 3
		time.sleep(.1)

except Exception as e:
	print('Error:', e)
except KeyboardInterrupt:
	print("keyboard Interrupt")
finally:
	if not mainProcess is None:
		mainProcess.kill()
	try:
		subprocess.check_call(["sudo", "-H", "python3",
				"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
				str(32), str(8), str(.01), "Done", str(0), str(0)])
		time.sleep(3)
	except:
		pass
	subprocess.check_call(["sudo", "-H", "python3",
				"/home/ubuntu/catkin_ws/src/ROS_River/src/show1.py",
				str(32), str(8)])

#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from Tkinter import *

class ScanMonitor:
	def __init__(self, scan_topic):
		self.scan_topic_name = scan_topic

	def scanCallback(self,msg):
		#ranges contains 360 float measurements 
		print("Range array has " + str(len(msg.ranges)) + " elements.")
		print("Angle increement is " + str(msg.angle_increment))

	def start(self):
		root = Tk()
		rospy.Subscriber(self.scan_topic_name,LaserScan,self.scanCallback)
		root.mainloop() #similar to spin, but this method is more compatible with ui

def main():
	rospy.init_node('scan_monitor')
	scan_monitor = ScanMonitor("/robot0/laser_1")
	scan_monitor.start()

if __name__ == '__main__':
	main()
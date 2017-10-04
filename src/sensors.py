#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from rosmaze.msg import MinimumDistances
import sys

class Sensors:
	def __init__(self, scan_topic):
		self.scan_topic_name = scan_topic

	def scanCallback(self,msg):
		#minimum values from front20 left30 right30 rays
		

		#if turtlebot, then have the opposite values since it increments angles in the opposite direction
		if(self.scan_topic_name == "/robot0/laser_0"):
			min_right_val = min(msg.ranges[75:105])
			min_left_val = min(msg.ranges[255:285])
			min_front_val = min(msg.ranges[165:195])
		else:
			min_left_val = min(msg.ranges[75:105])
			min_right_val = min(msg.ranges[255:285])
			min_front_val = min(min(msg.ranges[350:359]),min(list(msg.ranges[0:10])))

		#print values to check in console
		print("Min Front: " + str(min_front_val))
		print("Min Left: " + str(min_left_val))
		print("Min Right: " + str(min_right_val))

		#create a new message an publish
		msg = MinimumDistances()
		msg.min_front = min_front_val
		msg.min_left = min_left_val
		msg.min_right = min_right_val

		self.pub.publish(msg)

	def start(self):
		self.pub = rospy.Publisher('minimumDistances', MinimumDistances, queue_size=10)
		rospy.Subscriber(self.scan_topic_name,LaserScan,self.scanCallback)
		rospy.spin()

def main():
	robotid = str(sys.argv[1])
	rospy.init_node('sensors')
	
	#if turtlebot, get sensor data from scan topic
	if(robotid=="tb"):
		sensor_data = Sensors("scan")
		sensor_data.start()
	else:
		sensor_data = Sensors("/robot0/laser_0")
		sensor_data.start()
	
	

if __name__ == '__main__':
	main()



#!/usr/bin/env python
import rospy
from time import sleep
from geometry_msgs.msg import Twist

#make new twist command to have the bot go forward 1 unit
twist = Twist()
twist.linear.x = 1
twist.angular.z = 5

#make publisher
pub = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)

#initialize node
rospy.init_node('motor_controller')

while(True):
	pub.publish(twist)
	print("publishing")
	sleep(1)
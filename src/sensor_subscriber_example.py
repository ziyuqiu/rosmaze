#!/usr/bin/env python
import rospy
from rosmaze.msg import MinimumDistances

def callback(msg):
	print 'min_front:', msg.min_front
	print 'min_left:', msg.min_left
	print 'min_right:', msg.min_left
	print

rospy.init_node('message_subscriber')
sub = rospy.Subscriber('minimumDistances', MinimumDistances, callback)
rospy.spin()


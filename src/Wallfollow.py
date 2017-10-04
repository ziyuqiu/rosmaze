#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from time import sleep
import sys

class Wallfollow:
	def __init__(self, scan_topic, pub_topic):
		self.scan_topic_name = scan_topic
		self.pub_topic_name = pub_topic

	def scanCallback(self,msg):
		min_right_val = min(msg.ranges[70:110])
		min_front_val = min(msg.ranges[160:200])
		min_left_val = min(msg.ranges[250:290])
		t=Twist()
		t.linear.x = 0.2
		t.linear.y = 0
		t.linear.z = 0
		t.angular.x = 0
		t.angular.y = 0
		t.angular.z = 0
		self.pub.publish(t)

		if(min_right_val > self.wall_dist_away):
			#turn right and go back to the wall
			print("op1")
			t.linear.x = 0.2
			t.linear.y = 0
			t.linear.z = 0
			t.angular.x = 0
			t.angular.y = 0
			t.angular.z = -0.8
			self.pub.publish(t)
		elif(min_right_val < self.wall_dist_near):
			#turn left and go away from the wall slightly
			print("op2")
			t.linear.x = 0.2
			t.linear.y = 0
			t.linear.z = 0
			t.angular.x = 0
			t.angular.y = 0
			t.angular.z = 0.8
			self.pub.publish(t)
		elif(min_right_val < self.wall_dist_near/2):
			#turn left and go away from the wall slightly
			print("op2.5")
			t.linear.x = 0
			t.linear.y = 0
			t.linear.z = 0
			t.angular.x = 0
			t.angular.y = 0
			t.angular.z = 0.6
			self.pub.publish(t)

		if(min_front_val < self.wall_dist_near):
			print("op3")
			t.linear.x = 0
			t.linear.y = 0
			t.linear.z = 0
			t.angular.x = 0
			t.angular.y = 0
			t.angular.z = 0.7
			self.pub.publish(t)
		elif(min_left_val < self.opp_wall_dist_near):
			print("op4")
			t.linear.x = 0
			t.linear.y = 0
			t.linear.z = 0
			t.angular.x = 0
			t.angular.y = 0
			t.angular.z = 0.7
			self.pub.publish(t)	

	def start(self):
		self.wall_dist_away = .3
		self.wall_dist_near = .1
		self.opp_wall_dist_near = .2
		self.pub = rospy.Publisher(self.pub_topic_name, Twist, queue_size=10)
		rospy.Subscriber(self.scan_topic_name,LaserScan,self.scanCallback)
		rospy.spin()

def main():
	robotid = str(sys.argv[1])
	rospy.init_node('wall_follow')
	
	#if turtlebot, get sensor data from scan topic
	if(robotid=="tb"):
		wall_follow = Wallfollow("scan","cmd_vel")
		wall_follow.start()
	else:
		wall_follow = Wallfollow("/robot0/laser_0","/robot0/cmd_vel")
		wall_follow.start()
	
	

if __name__ == '__main__':
	main()
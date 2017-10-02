#!/usr/bin/env python
import rospy
from rosmaze.msg import MinimumDistances
from std_msgs.msg import Int32

class Mainloop:
	side = 0.32 #one side of width is 32 cm
	miss = side/5 #allowed error range
	range = 0.6

	def __init__(self,sensor_topic):
		self.sensor_topic = sensor_topic

	def sensor_callback(msg):
		front = msg.min_front
		left = msg.min_left
		right = msg.min_right
		if (left>=range or right >=range or front<= side):
			evaluateIntersection(front,left,right)
		else:
			self.pub.publish(0)
	
	def evaluateIntersection(front,left,right):	
		if (right >= range):
			if (front >= range and left >= range):
				self.pub.publish(4) #out	
			else:
				self.pub.publish(2) #rightturn
		elif (front >= range):
			self.pub.publish(0) #straight
		elif (left >= range):
			self.pub.publish(1) #leftturn
		else:
			self.pub.publish(3) #uturn

	def start():
		self.sub = rospy.Subscriber (self.sensor_topic, MinimumDistances, sensor_callback)	
		#0: go straight
		#1: leftturn
		#2: rightturn
		#3: uturn
		#4: out
		self.pub = rospy.Publisher('instruction', Int32)
		rospy.spin()
			
def main():
	rospy.init_node('instruction_publisher')
	main_loop = Mainloop("minimumDistances")
	main_loop.start()

if __name__ == '__main__':
	main()




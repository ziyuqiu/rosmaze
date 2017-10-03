#!/usr/bin/env python
import rospy
from rosmaze.msg import MinimumDistances
from std_msgs.msg import Int32

class Mainloop:

	def __init__(self,sensor_topic):
		self.sensor_topic = sensor_topic

	def sensor_callback(self, msg):
		front = msg.min_front
		left = msg.min_left
		right = msg.min_right
		if (left>=self.range or right >=self.range or front<= self.side):
			self.evaluateIntersection(front,left,right)
		else:
			self.pub.publish(0)
	
	def evaluateIntersection(self,front,left,right):	
		if (right >= self.range):
			if (front >= self.range and left >= self.range):
				self.pub.publish(4) #out	
			else:
				self.pub.publish(2) #rightturn
		elif (front >= self.range):
			self.pub.publish(0) #straight
		elif (left >= self.range):
			self.pub.publish(1) #leftturn
		else:
			self.pub.publish(3) #uturn

	def start(self):
		self.sub = rospy.Subscriber (self.sensor_topic, MinimumDistances, self.sensor_callback)	
		#0: go straight
		#1: leftturn
		#2: rightturn
		#3: uturn
		#4: out
		self.pub = rospy.Publisher('instruction', Int32, queue_size = 10)
		self.side = 0.32 #one side of width is 32 cm
		self.miss = self.side/5 #allowed error range
		self.range = 0.6

		rospy.spin()
			
def main():
	rospy.init_node('instruction_publisher')
	main_loop = Mainloop("minimumDistances")
	main_loop.start()

if __name__ == '__main__':
	main()




import rospy
from rosmaze.msg import MinimumDistances
from std_msgs.msg import Int32

class Mainloop:
	side = 0.32 #one side of width is 32 cm
	miss = side/5 #allowed error range
	range = 0.6
	straight = TRUE

	def __init__(self,sensor_topic):
		self.sensor_topic = sensor_topic

	def sensor_callback(msg):
		self.front = msg.min_front
		self.left = msg.min_left
		self.right = msg.min_right
	
	def evaluateIntersection(front,left,right):	
		if (right >= range):
			if (front >= range && left >= range):
				self.pub.publish(4) #out
				rospy.sleep()
			else:
				self.pub.publish(2) #rightturn
			else if (front >= range):
				self.pub.publish(0) #straight
			else if (left >= range):
				self.pub.publish(1) #leftturn
			else:
				self.pub.publish(3) #uturn

	def start():
		self.sub = rospy.Subscriber ('minimumDistances', MinimumDistances, sensor_callback)	
		#0: go straight
		#1: leftturn
		#2: rightturn
		#3: uturn
		#4: out
		self.pub = rospy.Publisher('instruction', Int32)
		rospy.spin()
		while not rospy.is_shutdown():
			self.pub.publish(0)
			if (self.left>=range || self.right >=range || self.front<= side):
				evaluateIntersection()
def main():
	rospy.init_node('instruction_publisher')
	main_loop = Mainloop("minimumDistances")
	main_loop.start()

if __name__ == '__main__':
	main()




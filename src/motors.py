#!/usr/bin/env python
import rospy
from time import sleep
from geometry_msgs.msg import Twist
from rosmaze.msg import MinimumDistances
from math import pi
from std_msgs.msg import Int32


class Motors:
	#expected width of the path
	EXPECTED_WIDTH = 15

	#line following p gain
	Kp_LINE_FOLLOW = 0.1

	#max error before we say the wall went away
	MAX_WALL_ERROR = 15

	def __init__(self):
		self.twist = Twist()
		#make publisher
		self.pub = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)
		#make subscriber
		self.sub = rospy.Subscriber('minimumDistances',MinimumDistances, self.callBack)

		#subscribe to commands
		self.conmand_sub = rospy.Subscriber('instruction', Int32, self.command_call_back)

		#initialize node
		rospy.init_node('motor_controller')

		self.lineFollowContinue = False

		#decide if we ignore commands so we can finish turns
		self.busy = False

		rospy.spin()




	def command_call_back(self, x):
		n = x.data
		print("running command callback, command is " + str(x))
		self.lineFollowContinue = (0 == x)
		if(self.busy):
			print("go away, I'm busy")
			return
		print("i'm getting to the psuedo-switch statement")
		if(1 == n):
			print("running case 1")
			self.turnLeft()
		elif(2==n):
			self.turnRight()
		elif(3==n):
			self.turnLeft()
			self.turnLeft()
		elif(4==n):
			self.turnLeft()
			self.turnRight()





	def turnLeft(self):
		self.busy = True
		self.goForward()
		self.twist.linear.x = 0
		self.twist.angular.z = pi / 2
		self.pub.publish(self.twist)
		sleep(1)
		self.twist.linear.x = 0
		self.twist.angular.z = 0
		self.pub.publish(self.twist)
		self.goForward()
		self.busy = False


	def turnRight(self):
		self.busy = True
		self.goForward()
		self.twist.linear.x = 0
		self.twist.angular.z = -1*pi / 2
		self.pub.publish(self.twist)
		sleep(1)
		self.twist.linear.x = 0
		self.twist.angular.z = 0
		self.pub.publish(self.twist)
		self.goForward()
		self.busy = False

	def goForward(self):
		self.twist.linear.x = 0.2
		self.twist.angular.z = 0
		self.pub.publish(self.twist)
		self.twist.linear.x = 0
		self.twist.angular.z = 0
		sleep(1.8)
		self.pub.publish(self.twist)

	def lineFollow(self):
		twist.linear.x = 0.2
		while(self.lineFollowContinue):
			left_error = self.min_left - EXPECTED_WIDTH
			right_error = EXPECTED_WIDTH - self.min_right
			#ignore measurements if errors are too large, it means there's not a wall to track
			ignore_left = (abs(left_error) > MAX_WALL_ERROR)
			ignore_right = (abs(right_error) > MAX_WALL_ERROR)
			if(ignore_left and ignore_right):
				twist.angular.z = 0
			elif(ignore_left):
				twist.angular.z = Kp_LINE_FOLLOW * right_error
			elif(ignore_right):
				twist.angular.z = Kp_LINE_FOLLOW * left_error
			else:
				twist.angular.z = Kp_LINE_FOLLOW * (left_error + right_error) / 2
			self.pub.publish(twist)


	def callBack(self,msg):
		self.min_front = msg.min_front
		self.min_left = msg.min_left
		self.min_right = msg.min_right


def main():
	m = Motors()



if __name__ == '__main__':
	main()



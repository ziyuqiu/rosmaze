#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from math import pi
from time import sleep


class PField:
	def __init__(self):
		self.sub = rospy.Subscriber("/robot0/laser_0",LaserScan,self.callback)
		rospy.init_node('potential_field')
		self.ranges = [0]*360

	def maxima_angle(self,input):
		i = 3 * len(input) / 4
		min_diff = 0.004
		#find the rightmost minima
		#print(input[i-(len(input)/20):i+(len(input)/20)])
		while(input[i] < input[i+1] + min_diff):
			i = i - 1
		#then find the rightmost maxima
		#find the element that is less than the one before it
		while(input[i] + min_diff > input[i+1]):
			i = i - 1
		return i;

	#moving average function
	def filter(self,input):
		return input
		
		output = [0] * len(input)
		smoothing_range = 10;
		i = smoothing_range
		while(i+smoothing_range < len(input)):
			#average
			output[i] = sum(input[i - smoothing_range:i + smoothing_range])/len(input[i - smoothing_range:i + smoothing_range])
			i = i + 1
		return output
		

	def callback(self,msg):
		self.ranges = msg.ranges



def main():
	p = PField()
	while(True):
		sleep(2)
		print(p.maxima_angle(p.filter(p.ranges)))

	


if __name__ == '__main__':
	main()
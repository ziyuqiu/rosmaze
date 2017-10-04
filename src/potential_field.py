#!/usr/bin/env python
import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from math import pi
from time import sleep


class PField:
	def __init__(self):
		self.sub = rospy.Subscriber("/robot0/laser_0",LaserScan,self.callback)
		#make publisher
		self.pub = rospy.Publisher("/robot0/cmd_vel", Twist, queue_size=10)
		rospy.init_node('potential_field')

	def command_vehicle(self):
		angle = self.pick_direction(
			self.find_peaks(
				self.ranges))
		Kp = 0.01
		angular_vel = -Kp*(angle-180)
		t = Twist()
		t.linear.x = 0.2
		t.linear.y = 0
		t.linear.z = 0
		t.angular.x = 0
		t.angular.y = 0
		t.angular.z = angular_vel
		self.pub.publish(t)

	def pick_direction(self, peaks):
		return peaks[len(peaks)-1]


	def find_peaks(self,input):
		i = 3 * len(input) / 4
		peaks = []
		while(i>len(input)/4):
			i = self.maxima_angle(input, i)
			peaks.append(i)
		return peaks




	def maxima_angle(self,input,i):
		#i = 3 * len(input) / 4
		min_diff = 0.004
		#find the rightmost minima
		#print(input[i-(len(input)/20):i+(len(input)/20)])
		while(input[i] < input[i+1] + min_diff):
			i = i - 1
		#then find the rightmost maxima
		#find the element that is less than the one before it
		while(input[i] + min_diff > input[i+1]):
			i = i - 1
		print("angle is " + str(i))
		print("range is " + str(input[i]))
		#return angle
		return i;

	#moving average function
	def filter(self,input):
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
	sleep(2)
	while(True):
		p.command_vehicle()
		sleep(.01)

	


if __name__ == '__main__':
	main()
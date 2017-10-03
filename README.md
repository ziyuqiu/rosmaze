# rosmaze

#To connect with turtlebot:

Terminal of laptop:
`ifconfig`
  -Copy inet addr
`gedit -/.bashrc`
  -Add “`export ROS_MASTER_RUI = HTTP://<IP Address>:11311`”
   -Add “`export ROS_HOSTNAME = <IP Address>`”
`source -/.bashrc`


Terminal of turtlebot:
`ifconfig`
  - get turtlebot’s IP Address
`gedit -/.bashrc`
  -Replace “`export ROS_MASTER_RUI = HTTP:// *<IP Address>*:11311`” with your laptop’s IP address
   -Replace “`export ROS_HOSTNAME = *<IP Address>*`” with turtlebot’s IP Address
`source  -/.bashrc`
`roslaunch turtlebot3_bringup turtlebot3_robot.launch`

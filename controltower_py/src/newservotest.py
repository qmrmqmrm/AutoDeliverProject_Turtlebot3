#!/usr/bin/env python
import rospy
from aruco_pkg.msg import ArucoTriggerMsg
from aruco_pkg.msg import ArucoMsg
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionResult


rospy.init_node("control", anonymous=True)
servo_pub = rospy.Publisher('/servo', UInt16, queue_size = 10)
serv = UInt16()
rate = rospy.Rate(0.3)
rate.sleep()


for i in range(10):
    serv.data = 50
    servo_pub.publish(serv)
    


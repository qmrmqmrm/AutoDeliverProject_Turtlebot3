#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist
from std_msgs.msg import UInt16

rospy.init_node("control", anonymous=True)

cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
servo_pub = rospy.Publisher('/servo', UInt16, queue_size=10)
serv = UInt16()
cmd = Twist()
rate = rospy.Rate(0.3)
rate.sleep()

while True:
    serv.data = 155
    servo_pub.publish(serv)
    cmd.angular.z = 0.995
    cmd_pub.publish(cmd)
    rate.sleep()
    cmd.angular.z = 0.0
    cmd.linear.x = -0.1
    cmd_pub.publish(cmd)
    rate.sleep()
    cmd.linear.x = 0.0
    serv.data = 140
    servo_pub.publish(serv)
    cmd_pub.publish(cmd)
    rate.sleep()
    #cmd.angular.z = -0.99
    cmd.linear.x = 0.1
    cmd_pub.publish(cmd)
    rate.sleep()
    #cmd.angular.z = 0
    cmd.linear.x = 0.0
    cmd_pub.publish(cmd)
    rate.sleep()


#!/usr/bin/env python
import time
import rospy
from controltower_py.msg import data

rospy.init_node("servo123", anonymous=True)

pub = rospy.Publisher('servo_flag', data, queue_size=10)

trigger = data()

while True:
    trigger.servo =0
    rospy.sleep(5)
    pub.publish(trigger)
    print("down")
    trigger.servo =1
    rospy.sleep(5)
    pub.publish(trigger)
    print("up")
            

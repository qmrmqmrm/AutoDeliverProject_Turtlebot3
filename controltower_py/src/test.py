#!/usr/bin/env python
import time
import rospy
from std_msgs.msg import UInt16
from controltower_py.msg import data

rospy.init_node("servo", anonymous=True)

class ServoClass:
    def __init__(self):
        self.servo_act = 0
    def ServoCallback(self,data):
        self.servo_act = data.servo

    def start_action(self):
        rospy.Subscriber('servo_flag', data, classname.ServoCallback)

        pub = rospy.Publisher('/servo', UInt16, queue_size=10)

        sv = UInt16()

        while True:
            if self.servo_act == 0:
                sv.data = 160

            elif self.servo_act == 1:
                sv.data = 140
            pub.publish(sv)
            

classname = ServoClass()
classname.start_action()

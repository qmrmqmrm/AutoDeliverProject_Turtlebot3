#!/usr/bin/env python
import rospy
from aruco_pkg.msg import ArucoMsg
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist

class ControlTower:
    def __init__(self):
        self.pub = rospy.Publisher('/move_base_simple/goal',PoseStamped,queue_size=10)
        rospy.Subscriber("aruco_msg",ArucoMsg,self.MsgCallback)
        self.vel = PoseStamped()
        self.detected_marker = 0
        self.mode = 1
        rate = rospy.Rate(0.3)
        rate.sleep()

    def MsgCallback(self,data):
        self.detected_marker = data.marker_id
        self.Pub_goal()

    def Pub_goal(self):
        if self.mode == 1:
            if self.detected_marker == 1:
                self.vel.pose.position.x = -0.2
                self.vel.pose.position.y = 0.2
                self.vel.pose.position.z = 0
                self.vel.pose.orientation.z = -0.685
                self.vel.pose.orientation.w = 0.728
                self.vel.header.frame_id = "map"
                self.pub.publish(self.vel)
                print("published")
                self.mode = 0
                self.detected_marker = 0

rospy.init_node("control_0923")
Cnide = ControlTower()
rospy.spin()

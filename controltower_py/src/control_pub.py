#!/usr/bin/env python
import time
import rospy
from geometry_msgs.msg import Twist
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt16
from aruco_pkg.msg import ArucoMsg


class ControlTower:
    def __init__(self):
        self.vel_msg = Twist()
        self.servo_msg = UInt16()
        self.goal_msg = PoseStamped()
        self.cmd_vel_pub = rospy.Publisher("cmd_vel",Twist,queue_size=1)
        self.goal_pub = rospy.Publisher("move_base_simple/goal",PoseStamped,queue_size=1)
        self.servo_pub = rospy.Publisher("/servo",UInt16,queue_size=1)

    def MsgPublish(self):
	self.vel_msg.linear.x = -self.vel_msg.linear.x
	self.vel_msg.angular.z = -self.vel_msg.angular.z

	self.goal_msg.pose.position.x = -0.1;
        self.goal_msg.pose.position.y = -1.8;
        self.goal_msg.pose.position.z = 0;
        self.goal_msg.pose.orientation.w = 3.24;
        self.goal_msg.header.stamp = ros::Time::now();
        self.goal_msg.header.frame_id = "map";
        self.goal_pub.publish(goal_msg);

	self.servo_msg.data = 90

        self.cmd_vel_pub.publish(self.vel_msg)
        self.goal_pub.publish(self.goal_msg)
        self.servo_pub.publish(self.servo_msg)

def main():
    while True:
        time.sleep(5)
	print("publish")
	Cmode.MsgPublish()

rospy.init_node("control2")
Cmode = ControlTower()
main()

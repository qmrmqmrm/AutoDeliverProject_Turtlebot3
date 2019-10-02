#!/usr/bin/env python

import rospy
from geometry_msgs.msg import PoseStamped

rospy.init_node('sending_goal_pose', anonymous=True)


pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
vel = PoseStamped()
while True:
    vel.pose.position.x = -2.0
    vel.pose.position.y = 0.0
    vel.pose.position.z = 0
    vel.pose.orientation.z=1
    vel.pose.orientation.w =1
#    vel.header.stamp = rospy.Time.now()
    vel.header.frame_id = "map"
    pub.publish(vel)

if vel.pose.position.x == -1.0:
    print("sent")
else:
    print("error")

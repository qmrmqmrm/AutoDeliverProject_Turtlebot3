#!/usr/bin/env python
import rospy
from aruco_pkg.msg import ArucoTriggerMsg
from aruco_pkg.msg import ArucoMsg
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist
from move_base_msgs.msg import MoveBaseActionResult


class Control:
    def __init__(self):
        rospy.init_node("control", anonymous=True)
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size = 10)
        self.trigger_aruco = rospy.Publisher('arucoTrigger_msg', ArucoTriggerMsg, queue_size = 1)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size = 10)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 10)
        self.aruco_sub = None
        self.marker_id = 0
        self.goal_status = 0
        self.vel = PoseStamped()
        self.ArucoTrigger = ArucoTriggerMsg()
        self.serv = UInt16()
        self.cmd = Twist()
        self.mode = "waiting_position"


    def main(self):
        while True:
            self.starting_trigger()
            self.return_to_base()
            self.detect_marker()
            self.goal_reached()
            if self.mode == "exit_program":
                print("Exit Program")
                break
            else:
                pass

        # after returning, detect marker

        # turn around for 180 degrees

        # go backward for box, pick up box, go straight

        # start navigation and repeat

    def starting_trigger(self):
        if self.mode == "waiting_position" or self.mode == "detect_marker":
            rospy.Subscriber("/starting_trigger",ArucoTriggerMsg, self.StartingCallback)
        else:
            pass


    def GoalPoseCallback(self, data):
        self.goal_status = data.status.status


    def StartingCallback(self,data):
        if data.trigger == 1:
            self.mode = "return_to_base"
        elif data.trigger == -1:
            self.mode = "exit_program"
        else :
            pass

    def MarkerIdCallback(self, data):
        self.marker_id = data.marker_id

    def return_to_base(self):
        # set mode
        if self.mode == "return_to_base":
            self.vel.pose.position.x = -0.4
            self.vel.pose.position.y = 0.4
            self.vel.pose.position.z = 0
            self.vel.pose.orientation.z = -0.70444
            self.vel.pose.orientation.w = 0.7098
            self.vel.header.frame_id = "map"
            self.goal_pub.publish(self.vel)
            self.mode = "waiting_position"
        else:
            rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.GoalPoseCallback)
            if self.goal_status == 3 or self.goal_status == 4: # if goal reached
                self.mode = "detect_marker"
            else:
                pass


    def detect_marker(self):
        if self.mode == "detect_marker":
            self.ArucoTrigger.trigger = 1
            self.trigger_aruco.publish(self.ArucoTrigger)
            self.mode = "marker_waiting_position"
        else:
            pass
        if self.mode == "marker_waiting_position":
            rospy.Subscriber('aruco_msg', ArucoMsg, self.MarkerIdCallback)
            if self.marker_id != 0:
                self.mode = "navigation"
                self.ArucoTrigger.trigger = 0
                self.trigger_aruco.publish(self.ArucoTrigger)
                self.PickUp()
                self.Navigation()
            else:
                pass
        else:
            pass


    def goal_reached(self):
        if self.mode == "navigation":
            rospy.Subscriber('/move_base_msgs/result', MoveBaseActionResult, self.GoalPoseCallback)
            print(self.goal_status)
            if self.goal_status == 3 or self.goal_status == 4:
                self.PickDown()
                self.mode = "return_to_base"
                self.goal_status = 0
            else:
                pass
        else:
            pass
            
            

    def Delay(self, data):
        self.rate = rospy.Rate(data)
        self.rate.sleep()
        
    def PickUp(self):
        self.Delay(20)
        self.cmd.angular.z = 0.995
        self.cmd_pub.publish(self.cmd)
        self.Delay(0.3)
        self.cmd.angular.z = 0.0
        self.cmd.linear.x = -0.1
        self.cmd_pub.publish(self.cmd)
        self.Delay(0.3)
        self.cmd.linear.x = 0.0
        self.serv.data = 120
        self.servo_pub.publish(self.serv)
        self.cmd_pub.publish(self.cmd)
        self.Delay(2.3)
        self.serv.data = 80
        self.servo_pub.publish(self.serv)
        self.cmd.linear.x = 0.1
        self.cmd_pub.publish(self.cmd)
        self.Delay(0.3)
        self.cmd.linear.x = 0.0
        self.cmd_pub.publish(self.cmd)
        self.Delay(20)

    def PickDown(self):
        self.Delay(20)
        self.serv.data = 50
        self.servo_pub.publish(self.serv)
        self.Delay(2.8)
        self.serv.data = 80
        self.servo_pub.publish(self.serv)
        self.cmd.linear.x = 0.1
        self.cmd_pub.publish(self.cmd)
        self.Delay(0.3)
        self.cmd.linear.x = 0.0
        self.cmd_pub.publish(self.cmd)
        self.Delay(20)

    def Navigation(self):
        if self.marker_id == 1:
            self.vel.pose.position.x = -2.175
            self.vel.pose.position.y = 0.87
            self.vel.pose.position.z = 0
            self.vel.pose.orientation.z = -0.02
            self.vel.pose.orientation.w = 1.0
            self.vel.header.frame_id = "map"
        else:
            pass
        self.goal_pub.publish(self.vel)
        self.marker_id = 0
        self.goal_status = 0

Turtle = Control()

if __name__ == "__main__":
    Turtle.main()

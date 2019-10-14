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
        self.goal_pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
        self.trigger_aruco = rospy.Publisher('arucoTrigger_msg', ArucoTriggerMsg, queue_size=1)
        self.servo_pub = rospy.Publisher('/servo', UInt16, queue_size=10)
        self.cmd_pub = rospy.Publisher("/cmd_vel", Twist, queue_size=10)
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
            # 1. 프로그램 시작 트리거 subscribe
            self.starting_trigger()
            rospy.Subscriber("/move_base/result", MoveBaseActionResult, self.GoalPoseCallback)
            # 2. 만약 모드가 return_to_base 라면 본진으로 귀환("home" 메시지 퍼블리쉬)
            if self.mode == "return_to_base":
                self.return_to_base()
                self.mode = "marker_waiting_position"
            # 3. 만약 골 스테이터스가 3이나 4가 된다면 aruco trigger 발동(1)
            elif (self.goal_status == 3 or self.goal_status == 4) and self.mode == "marker_waiting_position":
                self.mode = "start_detect_marker"
                self.trigger_detect_marker()
                self.mode = "detect_marker"
            # 4. 마커 id subscibe
            elif self.mode == "detect_marker":
                self.detect_marker()
                if self.marker_id != 0:
                    self.mode = "pickup_box"
                else:
                    pass
            # 5. 박스 들어올리기
            elif self.mode == "pickup_box":
                self.PickUp()
                self.goal_status = 0
                self.mode = "navigation"
            # 6. 마커 id에 맞는 목적지로 네비게이션("dest1" 메시지 퍼블리쉬)
            elif self.mode == "navigation":
                self.Navigation()
                self.mode = "pickdown_box"
            # 7. 만약 골 스테이터스가 3이나 4가 된다면 박스 내려놓기
            elif (self.goal_status == 3 or self.goal_status == 4) and self.mode == "pickdown_box":
                self.PickDown()
                self.goal_status = 0
                self.mode = "return_to_base"
            # 8. 2번으로 회귀

    def starting_trigger(self):
        if self.mode == "waiting_position" or self.mode == "detect_marker":
            rospy.Subscriber("/starting_trigger", ArucoTriggerMsg, self.StartingCallback)
        else:
            pass

    def GoalPoseCallback(self, data):
        self.goal_status = data.status.status

    def StartingCallback(self, data):
        if data.trigger == 1:
            self.mode = "return_to_base"
        elif data.trigger == -1:
            self.mode = "exit_program"
        else:
            pass

    def MarkerIdCallback(self, data):
        self.marker_id = data.marker_id

    def return_to_base(self):
        self.vel.pose.position.x = -0.4
        self.vel.pose.position.y = 0.4
        self.vel.pose.position.z = 0
        self.vel.pose.orientation.z = -0.70444
        self.vel.pose.orientation.w = 0.7098
        self.vel.header.frame_id = "map"
        self.goal_pub.publish(self.vel)


    def trigger_detect_marker(self):
        if self.mode == "start_detect_marker":
            self.ArucoTrigger.trigger = 1
            self.trigger_aruco.publish(self.ArucoTrigger)
        else:
            pass

    def detect_marker(self):
        rospy.Subscriber('aruco_msg', ArucoMsg, self.MarkerIdCallback)
        self.ArucoTrigger.trigger = 0
        self.trigger_aruco.publish(self.ArucoTrigger)

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


Turtle = Control()

if __name__ == "__main__":
    Turtle.main()

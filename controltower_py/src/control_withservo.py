#!/usr/bin/env python
import time
import rospy
from aruco_pkg.msg import ArucoMsg
from geometry_msgs.msg import PoseStamped
from std_msgs.msg import UInt16
from geometry_msgs.msg import Twist

print("Robot Program Test")

class ControlTower:
    def __init__(self):
        self.cnt = False
        self.markercount = 0
        self.markercount2 = 0
        self.booltype = False
        if self.cnt == False:
            self.mode = "return_to_base"
            self.detected_marker = None
            self.servo_act = None
            self.servo_act_base = None
            self.servo_count = 0

        # self.marker_id = None
        # if mode == "mode":
        #     self.mode == "return_to_base"
        # else:
        #     print("mode error")


    def MsgCallback(self, data):
        self.detected_marker = data.marker_id
    def ReturnBase(self):
        print(self.mode)
        if self.mode == "return_to_base":
            pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
            vel = PoseStamped()
            pub_servo = rospy.Publisher('/servo', UInt16, queue_size=10)
            serv = UInt16()
            for i in range(500):
                serv.data = 160
                pub_servo.publish(serv)

            while True:
                # print("hi")
            # while vel.pose.position.x != 1.0 and vel.pose.position.y != 0.0 and vel.pose.orientation.z != 0 and vel.pose.orientation.w != 1:
            #     print('hi')
                vel.pose.position.x = -0.175
                vel.pose.position.y = 0.05
                vel.pose.position.z = 0
                vel.pose.orientation.z = -0.685
                vel.pose.orientation.w = 0.728
                vel.header.frame_id = "map"
                pub.publish(vel) 
            	rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MsgCallback)
            	if self.detected_marker == 0:
                self.mode = "detect_marker"
                    self.markercount = self.markercount+1
                    print(self.markercount)
                if self.markercount == 4000:
                    serv.data = 140
                    pub_servo.publish(serv)
                elif self.markercount == 6000:
                    break
               


            # if vel.pose.position.x == 1.0 and vel.pose.position.y == 0.0 and vel.pose.position.z == 0 and vel.pose.orientation.z == 0 and vel.pose.orientation.w == 1:
            self.markercount = 0
            self.mode = "detect_marker"
            print(self.mode)
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True

    def MarkerDetect(self):
        rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MsgCallback)

        if self.mode == "detect_marker":
            if self.detected_marker == 0:
                self.mode = "marker_detected"
                print("marker_detected")
            else:
                print("wrong marker")
                self.cnt = True

            # time.sleep(1)

            if self.mode == "marker_detected":
                pub_servo = rospy.Publisher('/servo', UInt16, queue_size=10)
                serv = UInt16()
                pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
                vel = PoseStamped()

                while True:
                    vel.pose.position.x = -2.125
                    vel.pose.position.y = 0.9
                    vel.pose.position.z = 0
                    vel.pose.orientation.z = -0.02
                    vel.pose.orientation.w = 1.0
                    vel.header.frame_id = "map"
                    pub.publish(vel)
                    rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MsgCallback)
                    self.markercount2 = self.markercount2+1
                    
                    if self.markercount2 == 12000:
                        serv.data = 160
                        pub_servo.publish(serv)
                    elif self.markercount2 == 13000:
                        break

                self.markercount2 = 0
                self.mode = "return_to_base"
                self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True
    def TurnRight(self):
        if self.mode == "turn_right":
            print("robot turned right!")
            self.mode = "move_backward"
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True
    def MoveBackward(self):
        if self.mode == "move_backward":
            print("robot moved backward!")
            self.mode = "pick_up"
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True
    def MoveForward(self):
        if self.mode == "move_forward":
            print("robot moved forward!")
            self.mode = "nav_to_des"
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True
    def PickUp(self):
        if self.mode == "pick_up":
            print("picked up box")
            self.mode = "move_forward"
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True
    def NavToDestination(self):
        if self.mode == "nav_to_des":
            print("started navigation!")
            time.sleep(1)
            if self.mode == "arrived_des":
                print("navigation finished!")
                self.mode = "return_to_base"
                self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True

starting_mode = "return_to_base"

def main():
    count = 0
    while True:
        time.sleep(1)
        Cmode.ReturnBase()
        time.sleep(1)
        Cmode.MarkerDetect()
        time.sleep(1)
        Cmode.TurnRight()
        time.sleep(1)
        Cmode.MoveBackward()
        time.sleep(1)
        Cmode.PickUp()
        time.sleep(1)
        Cmode.MoveForward()
        time.sleep(1)
        Cmode.NavToDestination()
        time.sleep(1)
        count +=1
        if count == 10:
            break

# main()
rospy.init_node("control", anonymous=True)
Cmode = ControlTower()
# Cmode.mode = "detect_marker"


Cmode.ReturnBase()
# Cmode.ReturnBase()
Cmode.MarkerDetect()
Cmode.ReturnBase()
Cmode.MarkerDetect()

# main()

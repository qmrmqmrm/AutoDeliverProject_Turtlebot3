#!/usr/bin/env python
import time
import rospy
from aruco_pkg.msg import ArucoMsg
from geometry_msgs.msg import PoseStamped

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
        # self.marker_id = None
        # if mode == "mode":
        #     self.mode == "return_to_base"
        # else:
        #     print("mode error")
    def PoseFeedback(self, data):
        self.CoordinateX = data.pose.position.x
        self.CoordinateY = data.pose.position.y
        self.OrientationZ = data.pose.orientation.z
        self.OrientationW = data.pose.orientation.w

    def MarkerMsgCallback(self, data):
        #rospy.loginfo('marker id : {}'.format(data.marker_id))
        #print("marker id: ",data.marker_id)
        self.detected_marker = data.marker_id

    def ReturnBase(self):
        print(self.mode)

        if self.mode == "return_to_base":
            pub = rospy.Publisher('/move_base_simple/goal', PoseStamped, queue_size=10)
            vel = PoseStamped()
            while True:
                # print("hi")
            # while vel.pose.position.x != 1.0 and vel.pose.position.y != 0.0 and vel.pose.orientation.z != 0 and vel.pose.orientation.w != 1:
            #     print('hi')
                vel.pose.position.x = -0.125
                vel.pose.position.y = -0.27
                vel.pose.orientation.z = -0.71
                vel.pose.orientation.w = 0.705
                vel.header.frame_id = "map"
                pub.publish(vel)

                # if
                rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MarkerMsgCallback)
                rospy.Subscriber("move_base/feedback", PoseStamped(), Cmode.PoseFeedback)
                if self.detected_marker == 0:
                #     self.markercount = self.markercount+1
                #     print(self.markercount)
                # if self.markercount == 3000:
                #     break

                    if ((self.CoordinateX >= -0.175 and self.CoordinateX <= -0.075) and (self.CoordinateY >= -0.32 and self.CoordinateY <= -0.22) and (self.OrientationZ >= -0.88 and self.OrientationZ <= -0.54) and (self.OrientationW >= 0.535 and self.OrientationW <= 0.875)):
                        break
                    else:
                        print("nonoman")
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
        rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MarkerMsgCallback)
        if self.mode == "detect_marker":
            if self.detected_marker == 0:
                self.mode = "marker_detected"
                print("marker_detected")
            else:
                print("wrong marker")
                self.cnt = True

            time.sleep(1)

            if self.mode == "marker_detected":
                pub = rospy.Publisher('/move_base_simple/goal', PoseStamped(), queue_size=10)
                vel = PoseStamped()
                while True:
                # while vel.pose.position.x != -2.0 and vel.pose.position.y != 0.0 and vel.pose.orientation.z != 1 and vel.pose.orientation.w != 1:
                    vel.pose.position.x = -2.125
                    vel.pose.position.y = 0.9
                    vel.pose.orientation.z = 1
                    vel.pose.orientation.w = 0.02
                    vel.header.frame_id = "map"
                    pub.publish(vel)
                    rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MarkerMsgCallback)
                    if self.detected_marker == 1:
                    #     self.markercount = self.markercount+1
                    #     print(self.markercount)
                    # if self.markercount == 3000:
                    #     break

                        if ((self.CoordinateX >= -2.175 and self.CoordinateX <= -2.075) and (self.CoordinateY >= 0.85 and self.CoordinateY <= 0.95) and (self.OrientationZ >= 0.83 and self.OrientationZ <= 1.34) and (self.OrientationW >= -0.15 and self.OrientationW <= 0.19)):
                            break
                # if vel.pose.position.x == -2.0 and  vel.pose.position.y == 0.0 and vel.pose.position.z == 0 and vel.pose.orientation.z==1 and vel.pose.orientation.w == 1:
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

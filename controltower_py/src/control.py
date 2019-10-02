#!/usr/bin/env python
import time
import rospy
from aruco_pkg.msg import ArucoMsg
print("Robot Program Test")

class ControlTower:
    def __init__(self):
        self.cnt = False
        if self.cnt == False:
            self.mode = "return_to_base"
            self.detected_marker = None
        # self.marker_id = None
        # if mode == "mode":
        #     self.mode == "return_to_base"
        # else:
        #     print("mode error")

    def MsgCallback(self, data):
        #rospy.loginfo('marker id : {}'.format(data.marker_id))
        #print("marker id: ",data.marker_id)
        self.detected_marker = data.marker_id
    def ReturnBase(self):
        if self.mode == "return_to_base":
            print("returned to base!")
            self.mode = "detect_marker"
            self.cnt = True
        else:
            print("Reseting mode")
            self.mode = "return_to_base"
            self.cnt = True

    def MarkerDetect(self):
        rospy.Subscriber("aruco_msg", ArucoMsg, Cmode.MsgCallback)
        if self.mode == "detect_marker":
            if self.detected_marker == 1:
                print("Marker id = {}".format(self.detected_marker))
                self.mode = "marker_detected"
            else:
                print("wrong marker")
                self.cnt = True

            time.sleep(1)

            if self.mode == "marker_detected":
                print("marker detect finished!")
                self.mode = "turn_right"
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
rospy.init_node("control")
Cmode = ControlTower()
# Cmode.mode = "detect_marker"

# while True:
#     Cmode.MarkerDetect()
main()

#include "ros/ros.h"
#include "aruco_pkg/ArucoMsg.h"


void msgCallback(const aruco_pkg::ArucoMsg::ConstPtr& msg)
{
	ROS_INFO("recieve msg = %d", msg->marker_id);

}

int main(int argc, char **argv)
{
	ros::init(argc, argv, "aruco_topic_subscriber");
	ros::NodeHandle nh;
	
	ros::Subscriber aruco_sub = nh.subscribe("aruco_msg", 10, msgCallback);
	
	ros::spin();
	return 0;
}

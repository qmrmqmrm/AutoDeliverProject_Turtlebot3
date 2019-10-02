#include "ros/ros.h"
#include "aruco_pkg/ArucoMsg.h"

int main(int argc, char **argv)
{
	ros::init(argc, argv, "aruco_topic_publisher"); 
	ros::NodeHandle aruco_nh;
	ros::Publisher aruco_pub = aruco_nh.advertise<aruco_pkg::ArucoMsg>("aruco_msg",10);
	
	ros::Rate loop_rate(10);
	
	aruco_pkg::ArucoMsg msg;
	msg.marker_id = 0;
	
	while(ros::ok())
	{

		ROS_INFO("send msg = %d", msg.marker_id);
		msg.marker_id++;
		aruco_pub.publish(msg);
		
		loop_rate.sleep();

	}
	
	return 0;
}

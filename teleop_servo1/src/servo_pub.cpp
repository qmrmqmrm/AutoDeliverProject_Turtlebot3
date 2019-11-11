#include <iostream>
#include "ros/ros.h"
#include <stdio.h>
#include "std_msgs/UInt16.h"
#include <termios.h>  
#include <unistd.h>  

int servo_angle, ch=0;

void signalCallback(const std_msgs::UInt16::ConstPtr& sigVal) 
{
   servo_angle=(int)2000/180*(sigVal->data);
   ROS_INFO("servo_angle = %f", servo_angle);
   ch=1;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "servo_pub");
  ros::NodeHandle nh1;
  ros::NodeHandle nh2;
  ros::Publisher servo_pub = nh1.advertise<std_msgs::UInt16>("servo",10);
  ros::Subscriber ros_sub = nh2.subscribe("signal", 10, signalCallback);
  ros::Rate loop_rate(10);
  std_msgs::UInt16 msg;

  while(ros::ok())
  {
    ros::spinOnce();
    
    if(ch==1)
    {
	    msg.data = servo_angle;
	    servo_pub.publish(msg);
	    printf("send servo_angular = %d\n", msg.data);
	    ch=0;
    }
   
   }
}

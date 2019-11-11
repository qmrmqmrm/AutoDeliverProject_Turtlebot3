#include <iostream>
#include "ros/ros.h"
#include <stdio.h>
#include "geometry_msgs/Twist.h"
#include "std_msgs/UInt16.h"

int servo_angle, ch=0;

void signalCallback(const std_msgs::UInt16::ConstPtr& sigVal) 
{
   signal=sigVal->data);
   ROS_INFO("servo_angle = %f", signal);
   ch=1;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "twist_pub");
  ros::NodeHandle nh1;
  ros::NodeHandle nh2;
  ros::Publisher moter_pub = nh1.advertise<geometry_msgs::Twist>("/cmd_vel",10);
  ros::Subscriber ros_sub = nh2.subscribe("signal", 10, signalCallback);
  ros::Rate loop_rate(10);
  geometry_msgs::Twist msg;

  while(ros::ok())
  {
    ros::spinOnce();
    
    if(ch==1)
    {
	switch(signal)
	      {			
		case 97:		// a
		  msg2.angular.z = -1;
		  break;
		case 115:		// s
		  msg2.angular.z = 0;
		  break;
		case 100:		// d
		  msg2.angular.z = 1;
		  break;
		case 113:		// q
		  msg2.linear.x = -0.1;
		  break;
		case 119:		// w
		  msg2.linear.x = 0;
		  break;
		case 101:		// e
		  servo_angle.data = 80;
		  break;
		case 122:		// z
		  servo_angle.data = 80;
		  break;
		case 120:		// x
		  servo_angle.data = 50;
		  break;
		case 99:		// c
		  servo_angle.data = 120;
		  break;
	       }

	    msg.data = servo_angle;
	    servo_pub.publish(msg);
	    printf("send servo_angular = %d\n", msg.data);
	    ch=0;
    }
   
   }
}


  
    
    printf("send linear = %f\n", msg2.linear.x);
    printf("send angular = %f\n", msg2.angular.z);
    printf("send servo_angular = %d\n", servo_angle.data);

    servo_pub.publish(servo_angle);
    moter_pub.publish(msg2);
    
    
    }
}

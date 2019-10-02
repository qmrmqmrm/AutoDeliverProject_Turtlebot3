#include "ros/ros.h"
#include <stdio.h>
#include "geometry_msgs/Twist.h"
#include "std_msgs/UInt16.h"
#include "teleop_servo1/mode_msg.h"
#include <termios.h>  
#include <unistd.h>  

int getch(void)  
{  
  int ch = '\n';  
  struct termios buf;  
  struct termios save;  
  
   tcgetattr(0, &save);  
   buf = save;  
   buf.c_lflag &= ~(ICANON|ECHO);  
   buf.c_cc[VMIN] = 1;  
   buf.c_cc[VTIME] = 0;  
   tcsetattr(0, TCSAFLUSH, &buf);  
   ch = getchar();  
   tcsetattr(0, TCSAFLUSH, &save);  
   return ch;  


}  

int main(int argc, char **argv)
{
  ros::init(argc, argv, "servo_pub");
  ros::NodeHandle nh1;
  ros::NodeHandle nh2;
  ros::NodeHandle nh3;
  ros::Publisher servo_pub = nh1.advertise<std_msgs::UInt16>("/servo",10);
  ros::Publisher trigger_pub = nh3.advertise<teleop_servo1::mode_msg>("/trigger_step",10);
  ros::Publisher moter_pub = nh2.advertise<geometry_msgs::Twist>("/cmd_vel",10);
  ros::Rate loop_rate(10);
  std_msgs::UInt16 servo_angle;
  geometry_msgs::Twist msg2;
  teleop_servo1::mode_msg msg;
  
  int ch;

  while(ros::ok())
  {
    ros::spinOnce();
    
    for(; !(ch=='\n');){  
  
        ch = getch();  
        printf("%d \n", ch);
        break;  
    }
    switch(ch)
      {			
        case 97:		// a
          msg.trigger = -1;
          break;
        case 115:		// s
	  msg.trigger = 0;
          break;
        case 100:		// d
	  msg.trigger = 1;
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
	  servo_angle.data = -1;
	  break;
	case 120:		// x
	  servo_angle.data = 50;
	  break;
	case 99:		// c
	  servo_angle.data = 100;
	  break;
       }
    //printf("send linear = %f\n", msg2.linear.x);
    //printf("send angular = %f\n", msg2.angular.z);
    //printf("send servo_angular = %d\n", servo_angle.data);
    printf("send trigger = %d\n", msg.trigger);

    //servo_pub.publish(servo_angle);
    //moter_pub.publish(msg2);
    trigger_pub.publish(msg);
    
    }
}

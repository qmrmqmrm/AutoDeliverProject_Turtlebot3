#include "ros/ros.h"
#include <stdio.h>
#include "std_msgs/UInt16.h"
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
  ros::init(argc, argv, "signal_pub");
  ros::NodeHandle nh1;
  ros::Publisher signal_pub = nh1.advertise<std_msgs::UInt16>("signal",10);
  ros::Rate loop_rate(10);
  std_msgs::UInt16 msg;
  
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
	case 122:		// z
	  msg.data = 45;
	  break;
	case 120:		// x
	  msg.data = 75;
	  break;
	case 99:		// c
	  msg.data = 100;
	  break;
       }

    signal_pub.publish(msg);
    printf("send servo_angular = %d\n", msg.data);
    }
}

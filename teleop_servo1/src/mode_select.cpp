#include "ros/ros.h"
#include <stdio.h>
#include "teleop_servo1/mode_msg.h"
#include <termios.h>
#include <unistd.h>

int mode = 0, cnt = 0;

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
  ros::init(argc, argv, "mode_select");
  ros::NodeHandle nh;
  ros::Publisher mode_pub = nh.advertise<teleop_servo1::mode_msg>("/starting_trigger",10);
  ros::Rate loop_rate(10);
  teleop_servo1::mode_msg msg;
  
  int ch;

  while(ros::ok())
  {
    for(; !(ch=='\n');){
      ch = getch();
      printf("%d \n",ch);
      break;
    }
    
    switch(ch)
      {			
        case 113:		// q
          msg.trigger = 0;
          break;
        case 119:		// w
          msg.trigger = 1;
          break;
	case 122:		// z
	  msg.trigger = -1;
	  break;
       }
    printf("send trigger = %d\n", msg.trigger);
    mode_pub.publish(msg);
    
    ros::spinOnce();
    }
}

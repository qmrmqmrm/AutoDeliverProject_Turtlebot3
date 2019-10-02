#include <opencv2/opencv.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv_bridge/cv_bridge.h>
#include <iostream>
#include <ros/ros.h>
#include <opencv2/core.hpp>

using namespace std;


#define ROS_NODE_NAME "camera_subscriber"
#define ROS_CAMERA_TOPIC_NAME "camera_topic"

int main(int argc, char** argv)
{
    ros::init(argc, argv, "opencv_test");
    cv::Mat frame;
    cv::VideoCapture cap(0);
    while(true){
        cap>>frame;
        cv::imshow("camera1", frame);
        if(cv::waitKey(10)==27)
            break;
    }
    cv::destroyAllWindows();

    return 0;
}


#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <iostream>
#include <opencv2/core/hal/hal.hpp>
#include <opencv2/core.hpp>
#include <opencv2/predefined_dictionaries.hpp>
#include <opencv2/aruco/dictionary.hpp>
#include "ros/ros.h"

using namespace cv;
using namespace std;


int main(int argc, char *argv[])
{
    ros::init(argc, argv, "camera_test"); 
	ros::NodeHandle cam_test;
	ros::NodeHandle cam_test2;
    cv::VideoCapture inputVideo;
    inputVideo.open(0);
    while (inputVideo.grab()) {
        cv::Mat image, imageCopy;
        inputVideo.retrieve(image);
        image.copyTo(imageCopy);
        cv::imshow("out", imageCopy);
        if(cv::waitKey(10) == 27)
            break;
    }
    cv::destroyAllWindows();
    return 0;
}


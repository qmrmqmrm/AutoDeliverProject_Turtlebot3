#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
#include <opencv2/videoio.hpp>
#include <iostream>
#include <opencv2/core/hal/hal.hpp>
#include <opencv2/core.hpp>
#include <opencv2/predefined_dictionaries.hpp>
#include <opencv2/aruco/dictionary.hpp>
#include <opencv2/aruco.hpp>


using namespace cv;
using namespace std;


int main(int argc, char *argv[])
{

    cv::VideoCapture inputVideo;
    inputVideo.open(0);
    cv::Ptr<cv::aruco::Dictionary> dictionary = cv::aruco::getPredefinedDictionary(cv::aruco::DICT_6X6_250);
    while (inputVideo.grab()) {
        cv::Mat image, imageCopy;
        inputVideo.retrieve(image);
        image.copyTo(imageCopy);
        std::vector<int> ids;
        std::vector<std::vector<cv::Point2f> > corners;
        cv::aruco::detectMarkers(image, dictionary, corners, ids);
        // if at least one marker detected
        if (ids.size() > 0)
            cv::aruco::drawDetectedMarkers(imageCopy, corners, ids);
        cv::imshow("out", imageCopy);
        if(cv::waitKey(10) == 27)
            break;
    }
    cv::destroyAllWindows();
    return 0;
}


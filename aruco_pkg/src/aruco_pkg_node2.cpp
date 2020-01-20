//#include <opencv2/highgui.hpp>
#include <opencv2/opencv.hpp>
//#include <opencv2/videoio.hpp>
#include <iostream>
#include <opencv2/core/hal/hal.hpp>
//#include <opencv2/core.hpp>
#include <opencv2/predefined_dictionaries.hpp>
#include <opencv2/aruco/dictionary.hpp>
#include "ros/ros.h"
#include "aruco_pkg/ArucoMsg.h"
#include "aruco_pkg/ArucoTriggerMsg.h"




using namespace cv;
using namespace std;

int starting = 0;

Mat dictionary = Mat(250, (6 * 6 + 7) / 8, CV_8UC4, (uchar*)DICT_6X6_1000_BYTES);

bool identify(const Mat &onlyBits, int &idx, int &rotation ) {
    int markerSize = 6;

    //비트 매트릭스를 바이트 리스트로 변환합니다.
    Mat candidateBytes = aruco::Dictionary::getByteListFromBits(onlyBits);

    idx = -1; // by default, not found

    //dictionary에서 가장 근접한 바이트 리스트를 찾습니다.
    int MinDistance = markerSize * markerSize + 1;
    rotation = -1;
    for (int m = 0; m < dictionary.rows; m++) {

        //각 마커 ID
        for (unsigned int r = 0; r < 4; r++) {
            int currentHamming = hal::normHamming(
                dictionary.ptr(m) + r*candidateBytes.cols,
                candidateBytes.ptr(),
                candidateBytes.cols );

            //이전에 계산된 해밍 거리보다 작다면
            if (currentHamming < MinDistance) {
                //현재 해밍 거리와 발견된 회전각도를 기록합니다.
                MinDistance = currentHamming;
                rotation = r;
                idx = m;
            }
        }
    }

    //idx가 디폴트값 -1이 아니면 발견된 것
    return idx != -1;
}


Mat getByteListFromBits(const Mat &bits) {
    // integer ceil
    int nbytes = (bits.cols * bits.rows + 8 - 1) / 8;

    Mat candidateByteList(1, nbytes, CV_8UC1, Scalar::all(0));
    unsigned char currentBit = 0;
    int currentByte = 0;

    uchar* rot0 = candidateByteList.ptr();

    for (int row = 0; row < bits.rows; row++) {
        for (int col = 0; col < bits.cols; col++) {
            // circular shift
            rot0[currentByte] <<= 1;

            // set bit
            rot0[currentByte] |= bits.at<uchar>(row, col);

            currentBit++;
            if (currentBit == 8) {
                // next byte
                currentBit = 0;
                currentByte++;
            }
        }
    }
    return candidateByteList;
}

void TriggerCallback(const aruco_pkg::ArucoTriggerMsg::ConstPtr& msg) {
    starting = msg->trigger;
}

int main(int argc, char *argv[])
{

	ros::init(argc, argv, "aruco_side_topic_publisher"); 
	ros::NodeHandle aruco_nh;
	ros::NodeHandle aruco_nh2;
	ros::Publisher aruco_pub = aruco_nh.advertise<aruco_pkg::ArucoMsg>("aruco_msg",10);
	ros::Subscriber aruco_sub = aruco_nh2.subscribe("arucoTrigger_msg", 1, TriggerCallback);
	ros::Rate loop_rate(10);
	aruco_pkg::ArucoMsg msg;
	
    cv::Mat input_image;
    cv::VideoCapture cap2(2);


    while(true) {
	ros::spinOnce();
        cap2>>input_image;
        
        Mat input_gray_image;
        cvtColor(input_image, input_gray_image, COLOR_BGR2GRAY);

        //Adaptive Thresholding을 적용하여 이진화 한다.
        Mat binary_image;
        adaptiveThreshold(input_gray_image, binary_image,
        255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, 91, 7);
        //threshold(input_gray_image, binary_image, 125, 255, THRESH_BINARY_INV | THRESH_OTSU);
        //imshow("binaried", binary_image);

        vector<vector<Point> > contours;
        findContours(binary_image, contours, RETR_LIST, CHAIN_APPROX_SIMPLE);

        for (size_t i = 0; i<contours.size(); i++) {
            Scalar c(0,255,0);
//            drawContours(input_image, contours, i, c, 2);
//            cv::imshow("cameratest",input_image);
        }

        vector<vector<Point2f> > marker;
        vector<Point2f> approx;

        for (size_t i = 0; i < contours.size(); i++)
        {
            approxPolyDP(Mat(contours[i]), approx, arcLength(Mat(contours[i]), true)*0.05, true);

            if (
                approx.size() == 4 && //사각형은 4개의 vertex를 가진다.
                fabs(contourArea(Mat(approx))) > 1000  && //면적이 일정크기 이상이어야 한다.
                fabs(contourArea(Mat(approx))) < 50000 && //면적이 일정크기 이하여야 한다.
                isContourConvex(Mat(approx)) //convex인지 검사한다.
                )
            {

                drawContours(input_image, contours, i, Scalar(0, 0, 255), 1, LINE_AA);

                vector<cv::Point2f> points;
                for (int j = 0; j<4; j++)
                    points.push_back(cv::Point2f(approx[j].x, approx[j].y));

                    //반시계 방향으로 정렬
                cv::Point v1 = points[1] - points[0];
                cv::Point v2 = points[2] - points[0];

                double o = (v1.x * v2.y) - (v1.y * v2.x);
                if (o < 0.0)
                    swap(points[1], points[3]);

                marker.push_back(points);

            }
        }

        cv::imshow("newcontoured2",input_image);

        vector<vector<Point2f> > detectedMarkers;
        vector<Mat> detectedMarkersImage;
        vector<Point2f> square_points;

        int marker_image_side_length = 80; //마커 6x6크기일때 검은색 테두리 영역 포함한 크기는 8x8
                                    //이후 단계에서 이미지를 격자로 분할할 시 셀하나의 픽셀너비를 10으로 한다면
                                    //마커 이미지의 한변 길이는 80
        square_points.push_back(cv::Point2f(0, 0));
        square_points.push_back(cv::Point2f(marker_image_side_length - 1, 0));
        square_points.push_back(cv::Point2f(marker_image_side_length - 1, marker_image_side_length - 1));
        square_points.push_back(cv::Point2f(0, marker_image_side_length - 1));

        Mat marker_image;
        for (int i = 0; i < marker.size(); i++)
        {
            vector<Point2f> m = marker[i];

            //Mat input_gray_image2 = input_gray_image.clone();
            //Mat markerSubImage = input_gray_image2(cv::boundingRect(m));


            //마커를 사각형형태로 바꿀 perspective transformation matrix를 구한다.
            Mat PerspectiveTransformMatrix = getPerspectiveTransform(m, square_points);

            //perspective transformation을 적용한다.
            warpPerspective(input_gray_image, marker_image, PerspectiveTransformMatrix, Size(marker_image_side_length, marker_image_side_length));

            //otsu 방법으로 이진화를 적용한다.
            threshold(marker_image, marker_image, 125, 255, THRESH_BINARY | THRESH_OTSU);



            //마커의 크기는 6, 검은색 태두리를 포함한 크기는 8
            //마커 이미지 테두리만 검사하여 전부 검은색인지 확인한다.
            int cellSize = marker_image.rows / 8;
            int white_cell_count = 0;
            for (int y = 0; y<8; y++)
            {
                int inc = 7; // 첫번째 열과 마지막 열만 검사하기 위한 값

                if (y == 0 || y == 7) inc = 1; //첫번째 줄과 마지막줄은 모든 열을 검사한다.


                for (int x = 0; x<8; x += inc)
                {
                    int cellX = x * cellSize;
                    int cellY = y * cellSize;
                    cv::Mat cell = marker_image(Rect(cellX, cellY, cellSize, cellSize));

                    int total_cell_count = countNonZero(cell);

                    if (total_cell_count > (cellSize*cellSize) / 2)
                        white_cell_count++; //태두리에 흰색영역이 있다면, 셀내의 픽셀이 절반이상 흰색이면 흰색영역으로 본다
                }
            }

            //검은색 태두리로 둘러쌓여 있는 것만 저장한다.
            if (white_cell_count == 0) {
                detectedMarkers.push_back(m);
                Mat img = marker_image.clone();
                detectedMarkersImage.push_back(img);
            }

            imshow("detected",marker_image);
        }


        vector<Mat> bitMatrixs;
        for (size_t i = 0; i < detectedMarkers.size(); i++)
        {
            Mat marker_image = detectedMarkersImage[i];

            //내부 6x6에 있는 정보를 비트로 저장하기 위한 변수
            Mat bitMatrix = Mat::zeros(6, 6, CV_8UC1);

            int cellSize = marker_image.rows / 8;
            for (int y = 0; y < 6; y++)
            {
                for (int x = 0; x < 6; x++)
                {
                    int cellX = (x + 1)*cellSize;
                    int cellY = (y + 1)*cellSize;
                    Mat cell = marker_image(cv::Rect(cellX, cellY, cellSize, cellSize));

                    int total_cell_count = countNonZero(cell);


                    if (total_cell_count > (cellSize*cellSize) / 2)
                        bitMatrix.at<uchar>(y, x) = 1;
                }
            }

            bitMatrixs.push_back(bitMatrix);
            //std::cout << bitMatrix<<std::endl;

        }

        vector<int> markerID;
        vector<vector<Point2f> > final_detectedMarkers;
        for (int i = 0; i < detectedMarkers.size(); i++)
        {
            Mat bitMatrix = bitMatrixs[i];
            vector<Point2f> m = detectedMarkers[i];


            int rotation;
            int marker_id;
            if (!identify(bitMatrix, marker_id, rotation ))
                cout << "발견안됨" << endl;
            else {

                if (rotation != 0) {
                    //회전을 고려하여 코너를 정렬합니다.
                    //마커의 회전과 상관없이 마커 코너는 항상 같은 순서로 저장됩니다.
                    std::rotate(m.begin(), m.begin() + 4 - rotation, m.end());
                }

                int sumx = 0, sumy = 0;
                for (int j = 0; j < 4; j++) {
                    putText(input_image, to_string(j + 1), Point(m[j].x, m[j].y), 16, 1, Scalar(255, 0, 0), 1, 1);
                    sumx += m[j].x;
                    sumy += m[j].y;
                }
                putText(input_image, "id="+to_string(marker_id), Point( sumx/4 , sumy/4 ), 16, 1, Scalar(255, 0, 0), 1, 1);

                cornerSubPix(input_gray_image, m, Size(5, 5), Size(-1, -1), TermCriteria(cv::TermCriteria::MAX_ITER | cv::TermCriteria::EPS, 30, 0.01));

                markerID.push_back(marker_id);
                final_detectedMarkers.push_back(m);
                imshow("cornerdetect2",input_image);
            }
			msg.marker_id = marker_id;
//if(starting!=0){
//std::cout<< starting <<std::endl;}

			if((starting == 1 && (msg.marker_id >=2) && (msg.marker_id <=5))) {
			    aruco_pub.publish(msg);
			    ROS_INFO("send msg = %d", msg.marker_id);

			}
			
			
			
        }

        if(cv::waitKey(10) == 27)
            break;
    }

    cv::waitKey();
    if(cv::waitKey(10) == 27)
        destroyAllWindows();
    return 0;
}


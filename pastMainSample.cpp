#include "ardrone/ardrone.h"
#include "opencv2/highgui/highgui.hpp"
#include "opencv2/imgproc/imgproc.hpp"
#include <unistd.h>
#include <iostream>
#include <fstream>
using namespace cv;
using namespace std;

ofstream fp("debug.out");
// AR.Drone class
ARDrone ardrone;
class pixel{
public:
int x, y;
};

int vel = 10;
int neg_vel = -3;

void move_up()
{

	//Go Up
	ardrone.move3D(0,0,vel, 0);
	usleep(500000); //1s
	ardrone.move3D(0,0,0.0,0);
	/* usleep(500000); //1s */

	//Come Down
	ardrone.move3D(0,0,neg_vel,0);
	usleep(500000); //1s
	ardrone.move3D(0,0,0.0,0);
	/* usleep(500000); //1s */

	
}

void move_down()
{

	//Come Down
	ardrone.move3D(0,0,neg_vel,0);
	usleep(500000); //1s
	ardrone.move3D(0,0,0.0,0);
	/* usleep(500000); //1s */

	//Go Up
	ardrone.move3D(0,0,vel,0);
	usleep(500000); //1s
	ardrone.move3D(0,0,0.0,0);
	/* usleep(500000); //1s */
}

	
// --------------------------------------------------------------------------
// main(Number of arguments, Argument values)
// Description  : This is the entry point of the program.
// Return value : SUCCESS:0  ERROR:-1
// --------------------------------------------------------------------------
int main(int argc, char *argv[])
{

	bool moved_down=false, moved_up=false,moved_left,moved_right;

	// Initialize
	if (!ardrone.open()) {
		std::cout << "Failed to initialize." << std::endl;
		return -1;
	}
	
	ardrone.takeoff();
	// Battery
	std::cout << "Battery = " << ardrone.getBatteryPercentage() << "[%]" << std::endl;

	// Key input
	int key = cv::waitKey(33);

	// Get an image
	cv::Mat imgTmp = ardrone.getImage();
	int rows, cols;
	int darea_threshold = 80000;
	int pix_ary_len = 06;
	list<pixel> pix_array;
	pixel temp;
	list<pixel>::iterator it;
	int count = 0;

	namedWindow("Control", WINDOW_AUTOSIZE); //create a window called "Control"

	/* Green */
	/* int iLowH = 38; */
	/* int iHighH = 75; */

	/* int iLowS = 150; */
	/* int iHighS = 255; */

	/* int iLowV = 60; */
	/* int iHighV = 255; */

	/* PINK */
	int iLowH = 153;
	int iHighH = 179;

	int iLowS = 148;
	int iHighS = 237;

	int iLowV = 109;
	int iHighV = 255;

	//Create trackbars in "Control" window
	createTrackbar("LowH", "Control", &iLowH, 179); //Hue (0 - 179)
	createTrackbar("HighH", "Control", &iHighH, 179);

	createTrackbar("LowS", "Control", &iLowS, 255); //Saturation (0 - 255)
	createTrackbar("HighS", "Control", &iHighS, 255);

	createTrackbar("LowV", "Control", &iLowV, 255);//Value (0 - 255)
	createTrackbar("HighV", "Control", &iHighV, 255);

	int iLastX = -1;
	int iLastY = -1;

	//Capture a temporary image from the camera

	//Create a black image with the size as the camera output
	Mat imgLines = Mat::zeros(imgTmp.size(), CV_8UC3);;
	Mat imgHSV;
	Mat imgThresholded;
	Mat imgOriginal;

	while (true)
	{

		imgOriginal= ardrone.getImage(); // read a new frame from video

		rows = imgOriginal.rows;
		cols = imgOriginal.cols;


		cvtColor(imgOriginal, imgHSV, COLOR_BGR2HSV); //Convert the captured frame from BGR to HSV


		inRange(imgHSV, Scalar(iLowH, iLowS, iLowV), Scalar(iHighH, iHighS, iHighV), imgThresholded); //Threshold the image

		//morphological opening (removes small objects from the foreground)
		erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		//morphological closing (removes small holes from the foreground)
		dilate(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));
		erode(imgThresholded, imgThresholded, getStructuringElement(MORPH_ELLIPSE, Size(5, 5)));

		//Calculate the moments of the thresholded image
		Moments oMoments = moments(imgThresholded);

		double dM01 = oMoments.m01;
		double dM10 = oMoments.m10;
		double dArea = oMoments.m00;

		// if the area <= 10000, I consider that the there are no object in the image and it's because of the noise, the area is not zero 
		if (dArea > 10000)
		{
			static int print_count = 0;
			//cout << dArea << endl;
			//calculate the position of the ball
			//
			int posX = dM10 / dArea;
			int posY = dM01 / dArea;

	//		cout << posX << "," << posY << endl;
			fp<< posX << "," << posY << endl;
			//The last five co-ordinates of the object are stored in this array

			temp.x = posX;
			temp.y = posY;

			if (pix_array.size() <= pix_ary_len){
				pix_array.push_back(temp);
			}

			else{
				pix_array.pop_front();
				pix_array.push_back(temp);
			}
			//This following if condition will check if the object has come close enough to the drone for the drone to dodge.
			//The base condition chosen for this case is, area of the object should be greater the 1 block. 1 block is equal to 
			//1/9th of the total image area.
			int up_count = 0, down_count = 0, left_count = 0, right_count = 0;
			if (dArea > darea_threshold){
				//Now decide what commands have to be sent to the drone, i.e. to dodge up, down, left , right
				it = pix_array.begin();
				temp.x = (*it).x;
				temp.y = (*it).y;
				it++;
				for (; it != pix_array.end(); it++){
					if ((*it).y < temp.y) up_count++;
					else if  ((*it).y > temp.y) down_count++;
					if ((*it).x < temp.x) left_count++;
					else if ((*it).x > temp.x) right_count++;
					temp.x = (*it).x;
					temp.y = (*it).y;
				}
					fp<< "Up: "<<up_count << endl;
					fp<< "Down : "<<down_count << endl;
					fp<< left_count << endl;
					fp<< right_count << endl;

				if (up_count >=pix_ary_len/2-1) {
						
					//Send D to the drone
					if(!moved_down)
					{
						move_down();
						cout << "Move Down" << endl;
						moved_down = true;
						moved_up = false;
					}
				}
				else if(down_count >= pix_ary_len/2-1){
					//Send U to the drone
					if(!moved_up)
					{
						cout << "Move Up" << endl;
						move_up();
						moved_up= true;
						moved_down= false;
					}
				}

				if (left_count > right_count) {
					//Send R to the drone
					//cout << "Move Right" << endl;
				}
				else{
					//Send L to the drone
					//cout << "Move Left" << endl;
				}
			}
			if (iLastX >= 0 && iLastY >= 0 && posX >= 0 && posY >= 0)
			{
				//Draw a red line from the previous point to the current point
				line(imgLines, Point(posX, posY), Point(iLastX, iLastY), Scalar(0, 0, 255), 2);
			}

			iLastX = posX;
			iLastY = posY;
		}
		//Mat detected_edges;

		imshow("Thresholded Image", imgThresholded); //show the thresholded image

		imgOriginal = imgOriginal + imgLines;
		imshow("Original", imgOriginal); //show the original image

		if (waitKey(5) == 27) //wait for 'esc' key press for 30ms. If 'esc' key is pressed, break loop
		{
			cout << "esc key is pressed by user" << endl;
			break;
		}
	}


	ardrone.landing();
	// See you
	ardrone.close();
	return 0;
}

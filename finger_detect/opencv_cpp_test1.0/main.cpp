#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

int main()
{
	cv::VideoCapture cap(1);
	const char *windowName = "Fingertip detection";
	int minH = 0, maxH = 30, minS = 30, maxS = 90, minV = 0, maxV = 190;
	cv::namedWindow(windowName);
	// cv::createTrackbar("MinH", windowName, &minH, 180);
	// cv::createTrackbar("MaxH", windowName, &maxH, 180);
	// cv::createTrackbar("MinS", windowName, &minS, 255);
	// cv::createTrackbar("MaxS", windowName, &maxS, 255);
	// cv::createTrackbar("MinV", windowName, &minV, 255);
	// cv::createTrackbar("MaxV", windowName, &maxV, 255);
	while (1)
	{
		cv::Mat frame;
		cap >> frame;
		cv::Mat hsv;
		cv::cvtColor(frame, hsv, CV_BGR2HSV);
		cv::inRange(hsv, cv::Scalar(minH, minS, minV), cv::Scalar(maxH, maxS, maxV), hsv);
		// cv::imshow(windowName, hsv);

		int blurSize = 3;
		int elementSize = 3;
		cv::medianBlur(hsv, hsv, blurSize);
		cv::Mat element = cv::getStructuringElement(cv::MORPH_ELLIPSE, cv::Size(2 * elementSize + 1, 2 * elementSize + 1), cv::Point(elementSize, elementSize));
		cv::dilate(hsv, hsv, element);
		// cv::imshow(windowName, hsv);

		// Contour detection
		std::vector<std::vector<cv::Point>> contours;
		std::vector<cv::Vec4i> hierarchy;
		cv::findContours(hsv, contours, hierarchy, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_SIMPLE, cv::Point(0, 0));
		// find the largest contour
		size_t largestContour = 0;
		for (size_t i = 1; i < contours.size(); i++)
		{
			if (cv::contourArea(contours[i]) > cv::contourArea(contours[largestContour]))
				largestContour = i;
		}
		cv::drawContours(frame, contours, largestContour, cv::Scalar(0, 0, 255), 1);

		if (!contours.empty())
		{
			std::vector<std::vector<cv::Point>> hull(1);
			cv::convexHull(cv::Mat(contours[largestContour]), hull[0], false);
			cv::drawContours(frame, hull, 0, cv::Scalar(0, 255, 0), 3);
		}
		cv::imshow(windowName, frame);

		if (cv::waitKey(30) >= 0)
			break;
	}
	return 0;
}

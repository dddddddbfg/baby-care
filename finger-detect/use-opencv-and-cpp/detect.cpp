#include <iostream>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>

float innerAngle(float px1, float py1, float px2, float py2, float cx1, float cy1)
{

	float dist1 = std::sqrt((px1 - cx1) * (px1 - cx1) + (py1 - cy1) * (py1 - cy1));
	float dist2 = std::sqrt((px2 - cx1) * (px2 - cx1) + (py2 - cy1) * (py2 - cy1));

	float Ax, Ay;
	float Bx, By;
	float Cx, Cy;

	//find closest point to C
	//printf("dist = %lf %lf\n", dist1, dist2);

	Cx = cx1;
	Cy = cy1;
	if (dist1 < dist2)
	{
		Bx = px1;
		By = py1;
		Ax = px2;
		Ay = py2;
	}
	else
	{
		Bx = px2;
		By = py2;
		Ax = px1;
		Ay = py1;
	}

	float Q1 = Cx - Ax;
	float Q2 = Cy - Ay;
	float P1 = Bx - Ax;
	float P2 = By - Ay;

	float A = std::acos((P1 * Q1 + P2 * Q2) / (std::sqrt(P1 * P1 + P2 * P2) * std::sqrt(Q1 * Q1 + Q2 * Q2)));

	A = A * 180 / CV_PI;

	return A;
}

int main()
{
	cv::VideoCapture cap(1);
	const char *windowName = "Fingertip detection";
	// int minH = 0, maxH = 20, minS = 30, maxS = 150, minV = 60, maxV = 255;
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
		//		 cv::imshow(windowName, hsv);

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
		// cv::imshow(windowName, frame);

		if (!contours.empty())
		{
			std::vector<std::vector<cv::Point>> hull(1);
			cv::convexHull(cv::Mat(contours[largestContour]), hull[0], false);
			cv::drawContours(frame, hull, 0, cv::Scalar(0, 255, 0), 3);
			if (hull[0].size() > 2)
			{
				std::vector<int> hullIndexes;
				cv::convexHull(cv::Mat(contours[largestContour]), hullIndexes, true);
				std::vector<cv::Vec4i> convexityDefects;
				cv::convexityDefects(cv::Mat(contours[largestContour]), hullIndexes, convexityDefects);
				cv::Rect boundingBox = cv::boundingRect(hull[0]);
				cv::rectangle(frame, boundingBox, cv::Scalar(255, 0, 0));
				cv::Point center = cv::Point(boundingBox.x + boundingBox.width / 2, boundingBox.y + boundingBox.height / 2);
				std::vector<cv::Point> validPoints;
				for (size_t i = 0; i < convexityDefects.size(); i++)
				{
					cv::Point p1 = contours[largestContour][convexityDefects[i][0]];
					cv::Point p2 = contours[largestContour][convexityDefects[i][1]];
					cv::Point p3 = contours[largestContour][convexityDefects[i][2]];
					double angle = std::atan2(center.y - p1.y, center.x - p1.x) * 180 / CV_PI;
					double inAngle = innerAngle(p1.x, p1.y, p2.x, p2.y, p3.x, p3.y);
					double length = std::sqrt(std::pow(p1.x - p3.x, 2) + std::pow(p1.y - p3.y, 2));
					if (angle > -30 && angle < 160 && std::abs(inAngle) > 20 && std::abs(inAngle) < 120 && length > 0.1 * boundingBox.height)
					{
						validPoints.push_back(p1);
					}
				}
				for (size_t i = 0; i < validPoints.size(); i++)
				{
					cv::circle(frame, validPoints[i], 9, cv::Scalar(0, 255, 0), 2);
				}
			}
		}
		cv::imshow(windowName, frame);

		if (cv::waitKey(30) >= 0)
			break;
	}
	return 0;
}

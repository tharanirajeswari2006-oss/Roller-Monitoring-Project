# Roller Monitoring Project

## Description
This project implements a vision-based roller monitoring system using Python and OpenCV. A camera tracks the movement of a paint mark on the roller from the top region to the bottom region within a fixed time interval to determine whether the roller is rotating. If the paint mark does not reach the bottom region within the specified time, the system identifies that the roller has stopped.

## Objective
To monitor roller rotation without physical sensors using camera-based image processing.

## Methodology
- Capture live video using a camera
- Detect paint mark using HSV color thresholding
- Divide the frame into top and bottom regions
- Track paint movement from top to bottom
- Trigger alarm and email alert if rotation stops

## Technologies Used
- Python
- OpenCV
- NumPy

## Application
- Industrial roller monitoring
- Manufacturing process automation

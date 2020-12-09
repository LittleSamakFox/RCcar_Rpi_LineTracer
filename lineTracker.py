import numpy as np
import cv2
import serial
import time
ser = serial.Serial('/dev/serial/by-id/usb-Arduino_Srl_Arduino_Uno_754393137373514170C0-if00',9600)
if ser is None:
    print("disconnected with arduino")

#camera setting
camera_pixel_x = 160
camera_pixel_y = 120
video_capture = cv2.VideoCapture(-1)
video_capture.set(3, camera_pixel_x)
video_capture.set(4, camera_pixel_y)

#line coordinate factor
gap = 1/10
right_g = 1/2 + gap
left_g = 1/2 - gap

#stop time factor
stop_count = 0

while(True):
	# Capture the frames
	ret, frame = video_capture.read()

	# Crop the image
	crop_img = frame[int(camera_pixel_y/2):camera_pixel_y, 0:camera_pixel_x]
	
	# Image Transformation for Recognition of black line
	# convert to grayscale, gaussian blur, and threshold
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(5,5),0)
	ret,thresh = cv2.threshold(blur,35,255,cv2.THRESH_BINARY_INV)

	# Erode to eliminate noise, Dilate to restore eroded parts of image
	mask = cv2.erode(thresh, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)
	
	#contours insert
	contours,hierarchy = cv2.findContours(mask.copy(), 1, cv2.CHAIN_APPROX_NONE)
	
	#line detection
	if len(contours) > 0:
		c = max(contours, key=cv2.contourArea)
		M = cv2.moments(c)
		cx = int(M['m10']/M['m00'])
		cy = int(M['m01']/M['m00'])
		
		cv2.line(crop_img,(cx,0),(cx,720),(255,0,0),1)
		cv2.line(crop_img,(0,cy),(1280,cy),(255,0,0),1)
		cv2.drawContours(crop_img, contours, -1, (0,255,0), 1)
		print(cx, cy)
		#Line recognition coordinates identify left, straight and right turns
		if cx >= camera_pixel_x*(right_g):
			print("R")
			cmd = ("R").encode('ascii')
		if cx < camera_pixel_x*(right_g) and cx > camera_pixel_x*(left_g):
			print("S")
			cmd = ("S").encode('ascii')
		if cx <= camera_pixel_x*(left_g):
			print("L")
			cmd = ("L").encode('ascii')
		ser.write(cmd)
	else:
		print("I don't see the line")
		stop_count +=1
		if stop_count > 20:
			cmd = ("D").encode('ascii')
			ser.write(cmd)
			stop_count = 0
		
	#Display the resulting frame
	cv2.imshow('frame',crop_img)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

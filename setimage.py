import cv2
# initialize the list of reference points and boolean indicating
# whether cropping is being performed or not
cropping = False



def get_coordinates(file_directory):
	refPt = []
	def click(event, x, y, flags, param):
		# grab references to the global variables
		global cropping
		# if the left mouse button was clicked, record the starting
		# (x, y) coordinates and indicate that cropping is being
		# performed
		i = 0
		if event == cv2.EVENT_LBUTTONDOWN:
			cropping = True
		# check to see if the left mouse button was released
		elif event == cv2.EVENT_LBUTTONUP:
			# record the ending (x, y) coordinates and indicate that
			# the cropping operation is finished
			refPt.append((x, y))
			#print(refPt)
			cropping = False

			# draw a rectangle around the region of interest
			radius = 5
			color = (0, 255, 0)
			thickness = 2
			for point in refPt:
				cv2.circle(image, tuple(point), radius, color, thickness)
				cv2.imshow("image", image)



	# Resize Image functions

	# load the image, clone it, and setup the mouse callback function
	src = cv2.imread(file_directory)

	#percent by which the image is resized
	scale_percent = 60

	#calculate the percent of original dimensions
	width = int(src.shape[1] * scale_percent / 100)
	height = int(src.shape[0] * scale_percent / 100)

	# dsize
	dsize = (width, height)

	# resize image
	image = cv2.resize(src, dsize)

	# Mouse callback functions

	clone = image.copy()
	cv2.namedWindow("image")
	cv2.setMouseCallback("image", click)



	# keep looping until the 'q' key is pressed
	while True:
		# display the image and wait for a keypress
		cv2.imshow("image", image)
		key = cv2.waitKey(1) & 0xFF
		# if the 'r' key is pressed, reset the cropping region
		if key == ord("r"):
			image = clone.copy()
			refPt.pop()
			radius = 5
			color = (0, 255, 0)
			thickness = 2
			for point in refPt:
				cv2.circle(image, tuple(point), radius, color, thickness)
				cv2.imshow("image", image)
			#print(refPt)
		# if the 'n' key is pressed, break from the loop and go to next image
		elif key == ord("n"):
			break
			

	# close all open windows
	cv2.destroyAllWindows()

	return refPt
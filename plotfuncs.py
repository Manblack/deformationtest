# import the necessary packages
import cv2
import os
import math
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy.interpolate import make_interp_spline, BSpline
from datetime import datetime



def count_frames(path):
	# grab a pointer to the video file and initialize the total
	# number of frames read
	video = cv2.VideoCapture(path)

	total = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

	video.release()
	# return the total number of frames in the video
	return total



def save_frames(path, total, samples):
	interval = total//(samples - 1)

	#Opening video and saving frames into Frame Analysis folder
	cap = cv2.VideoCapture(path)

	i=0
	while i < total:
		cap.set(1, i)
		ret, frame = cap.read()
		cv2.imwrite(str(i)+'.jpg',frame)
		i = i + interval - 2

	cap.release()
	cv2.destroyAllWindows()



def list_frames(total, samples):
	interval = total//(samples - 1)
	num_frames = []
	i = 0
	while i < total:
		num_frames.append(i)
		i = i + interval - 2

	for j in range (0, len(num_frames)):
		num_frames[j] = num_frames[j]/25
		round(num_frames[j])

	return num_frames



def get_files():
	files = []
	# r=root, d=directories, f = files
	for r, d, f in os.walk(os.getcwd()):
		for file in f:
			if '.jpg' in file:
				files.append(os.path.join(r, file))

	files.sort(key=os.path.getmtime)
	return files



def delete_files(path):
	os.unlink(path)



def calcdist(x1, x2, y1, y2):
	dist = math.sqrt ((x2 - x1)**2 + (y2-y1)**2)
	return dist



def curve(time, distances, xLabel):
#Function based on Manas Sharma lesson at https://www.bragitoff.com
	xData = time
	yData = distances
	samples_number = len(xData)

	#Plot experimental data points
	plt.plot(xData, yData, 'bo', label='Experimental Data')

	x_new = np.linspace (min(xData), max(xData), 300)
		# min and max of T can be substitude by numbers or be used as a percentage

	if samples_number >= 4:
		spl = make_interp_spline (xData, yData, k=3)
		power_smooth = spl (x_new)

	# calculate polynomial of 7 degree
	if samples_number <= 5:
		polinomial = np.polyfit(xData, yData, 3)
		degree = "3rd"
	if samples_number >5:
		polinomial = np.polyfit(xData, yData, 7)
		degree = "7th"
	
	poli_function = np.poly1d(polinomial)

	# calculate new y's for polonomial fit
	y_new = poli_function(x_new)

	plt.plot(x_new, y_new, 'c', label = "Polinomial Fit "+ "(" + str(degree) + "degree)")

	if samples_number >= 4:
		plt.plot(x_new, power_smooth, 'r', label = 'BSpline Fit')

	plt.title(xLabel)
	plt.xlabel("Time [s]")
	plt.ylabel('Distance [pixels]')
	plt.legend()
	plt.show()



def date():

	# datetime object containing current date and time
	now = datetime.now()

	# dd/mm/YY H:M:S
	dt_string = now.strftime("%d/%m/%Y_%H-%M-%S")
	new_date = dt_string.replace('/', '-')
	return(new_date)
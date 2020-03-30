import os
import setimage
import numpy as np
import cv2 as cv
import math
import matplotlib.pyplot as plt
import numpy as np
import time
from scipy.optimize import curve_fit
from datetime import datetime
from scipy.interpolate import make_interp_spline, BSpline
from plotfuncs import list_frames
from plotfuncs import count_frames
from plotfuncs import save_frames
from plotfuncs import get_files
from plotfuncs import delete_files
from plotfuncs import calcdist
from plotfuncs import date
from plotfuncs import curve
from setimage import get_coordinates



# Inputing video and Saving frames
print("\n")
print('AUXETIC DEFORMATION TEST - DISTANCE PLOT', '\n')
print('WARNINGS')
print("1: Remember to always select the couple of points in sequence")
print("2: If you will plot the distances using this program, analyse 4 frames minimum")
print(2*"\n")
videopath = input("Please, enter the video path:")
#print('Analysing video at', videopath)
print('this video has', count_frames(videopath), 'frames')
print("\n")
points = int(input('How many points would you like to analyse? (type an even number): '))
framesample = int(input('How many frames would you like to extract data? (needs to be > 1): '))



#Calculate number of Frames in the video
frames = count_frames(videopath)



#Make a list with the frames used, to identificate them later
listframes = list_frames(frames, framesample)



#Creating directory called Frame Analysis to store and manipulate frames
original_dir = os.getcwd()
new_dir = 'Frame Analysis'
if not os.path.exists(new_dir):
    os.mkdir(new_dir)
    print("Directory " , new_dir,  " Created ")
os.chdir(original_dir+"/Frame Analysis")


#Save frames inside Frame Analysis folder
save_frames(videopath, frames, framesample)



#Function that gives you all the files on a folder
ordered_files = get_files()



#For every file, collect 8 coordinates and save it on first_coordinates list

first_coordinates = []

for files in ordered_files:
	coord = get_coordinates(files)
	first_coordinates.append(coord)


#Deleting the Frames of the Frame Analysis Folder
for files in ordered_files:
	delete_files(files)


#Get all the distances and save on a list
all_distances = []
for i in range (0, len(first_coordinates)):
    for j in range (0, len(first_coordinates[0]),2) :
        x1 = first_coordinates [i][j][0]
        y1 = first_coordinates [i][j][1]
        x2 = first_coordinates [i][j+1][0]
        y2 = first_coordinates [i][j+1][1]

        DIST = calcdist (x1, x2, y1, y2)

        all_distances.append(DIST)


#Make a new list organized
#Create lists that will be used to plot the graphs
#Each sublist represent the distance of the same couple of points during the frames

couples_number = int(points/2)
dist_list = [[] for i in range(couples_number)]


for i in range(0, couples_number):
    position = i
    k = 0
    while k < framesample:
        dist_list[i].append(all_distances[position])
        position += couples_number
        k += 1



#Display Choices Menu
print(2*"\n")
print("Distances calculated succesfully")
print("\n")
print("What do you need now?")
print("Press [1] to save the data in CSV")
print("Press [2] to plot distances")
print("Press [3] to save data and plot distances")
choice = int(input("Type now: "))



#Saving in CSV:
if choice == 1 or choice == 3:
    
    #Create or new directory "CSV Data" if it doesn't exists
    os.chdir(original_dir)
    data_dir = "CSV Data"
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)  

    os.chdir(original_dir+"/CSV Data")
    date_now = date()
    os.mkdir(date_now)
    os.chdir(original_dir+"/CSV Data"+"/"+str(date_now))

    #Save data in CSV
    for l in range(0, len(dist_list)):
        txtname = "Distance" + str(l+1) + ".txt"
        with open(txtname, "w") as output:
            output.write(str(dist_list[l]))

    with open("Time.txt", "w") as output:
        output.write(str(listframes))
    print(2*"\n")    
    print("CSV files saved succesfully at:")
    
    print(os.getcwd())
    time.sleep(3)
    print("\n") 



#Plot BSpline and Polinomial curves using Scipy and Matplotlib
if choice == 2 or choice == 3:
    print("Wait 5 sec. for the plots to appear. Close one to see the next plot.")
    print("\n") 
    time.sleep(6)
    for h in range(0, len(dist_list)):
        title = "Distance" + str(h+1)
        curve(listframes, dist_list[h], title)

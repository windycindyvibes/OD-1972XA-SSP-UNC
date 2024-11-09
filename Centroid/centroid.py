import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
def findCentroid(fits_file, target_x, target_y, radius=3, sky_radius=5):
# YOUR CODE HERE
    data = fits.getdata(fits_file)
    star_values = data[target_y - radius:target_y + radius + 1, target_x - radius:target_x + radius + 1].astype('f')
    print(star_values) #debug
    total_radius = radius+sky_radius
    sky_values = data[target_y - total_radius:target_y + total_radius + 1, target_x - total_radius:target_x + total_radius + 1]
    print(sky_values) #debug
    sky_total = 0
    counter = 0
    for i in range(0, len(sky_values)):
        for j in range(0, len(sky_values[0])):
            if not (i >= sky_radius and i <= (sky_radius+2*radius) and j >= sky_radius and j <= (sky_radius+2*radius)):
                sky_total += sky_values[i][j]
                print("x " + str(i) + " y " + str(j) + " value " + str(sky_values[i][j])) #debug
                counter += 1
    print("count " + str(counter))
    sky_average = sky_total/((2*total_radius+1)**2 - (2*radius+1)**2)
    print(sky_total) #debug
    print(sky_average) #debug

    print(star_values)

    for i in range(len(star_values)):
        for j in range(len(star_values[0])):
            star_values[i][j] = star_values[i][j] - sky_average
    
    print(star_values)
    
    x_total_weighted = 0
    y_total_weighted = 0
    star_total = 0

    for i in range(len(star_values)):
        for j in range(len(star_values[0])):
            x_total_weighted += (star_values[i][j]*(target_x-radius+j))
            y_total_weighted += (star_values[i][j]*(target_y-radius+i))
            star_total += star_values[i][j]
            print("x " + str(target_x-radius+i) + " y " + str(target_y-radius+j) + " value " + str(star_values[i][j])) #debug
    
    x_centroid = x_total_weighted/(star_total)
    y_centroid = y_total_weighted/(star_total)

    return x_centroid, y_centroid 

centroid_x, centroid_y= findCentroid("D:/SSP/Centroid/sampleimage.fits", 351,
154, 3, 5)

# centroid_x, centroid_y, uncert_x, uncert_y = findCentroid("sampleimage.fits", 459,
# 397, 2)

if abs(centroid_x - 350.7806) < 0.1 and abs(centroid_y - 153.5709) < 0.1:
    print("centroid calculation CORRECT")
else:
    print(
        "centroid calculation INCORRECT, expected (350.7806, 153.5709), got ({}, {})".format(
        centroid_x, centroid_y))
    


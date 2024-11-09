import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits

def findCentroid(fits_file, target_x, target_y, radius=3, sky_radius=5):
    data = fits.getdata(fits_file)
    star_values = data[target_y - radius:target_y + radius + 1, target_x - radius:target_x + radius + 1].astype('f')
    total_radius = radius+sky_radius
    sky_values = data[target_y - total_radius:target_y + total_radius + 1, target_x - total_radius:target_x + total_radius + 1]
    sky_total = 0
    counter = 0
    for i in range(0, len(sky_values)):
        for j in range(0, len(sky_values[0])):
            if not (i >= sky_radius and i <= (sky_radius+2*radius) and j >= sky_radius and j <= (sky_radius+2*radius)):
                sky_total += sky_values[i][j]
                counter += 1
    sky_average = sky_total/((2*total_radius+1)**2 - (2*radius+1)**2)

    for i in range(len(star_values)):
        for j in range(len(star_values[0])):
            star_values[i][j] = star_values[i][j] - sky_average
    
    x_total_weighted = 0
    y_total_weighted = 0
    star_total = 0

    for i in range(len(star_values)):
        for j in range(len(star_values[0])):
            x_total_weighted += (star_values[i][j]*(target_x-radius+j))
            y_total_weighted += (star_values[i][j]*(target_y-radius+i))
            star_total += star_values[i][j]
    
    x_centroid = x_total_weighted/(star_total)
    y_centroid = y_total_weighted/(star_total)

    return x_centroid, y_centroid 
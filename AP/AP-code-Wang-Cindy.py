#!usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import math

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

def ap_phot(image, x, y, ap_rad, sky_inrad, sky_outrad, pad=10, find_centroid=True,
 dark_current=10., read_noise=11.):
    """
    Measure instrumental magnitude of a star in a fits image.
    image = fits image filename
    x = Approx. x position of object [pix]
    y = Approx. y position of object [pix]
    ap_rad = Aperture radius in pixels
    sky_inrad = Sky annulus inner radius in pixels
    sky_outrad = Sky annulus outer radius in pixels 
    pad = number of pixels to pad around this sky annulus for centroiding purposes. This should
    be larger than the possible difference between x,y and the actual centroid.
    """

    # Write here your code
    data = fits.getdata(image)
    x, y = findCentroid(image, x, y, ap_rad, pad)
    x_centroid = round(x)
    y_centroid = round(y)
    print('centroid', data[y_centroid][x_centroid])

    aperture_data = data[y_centroid-ap_rad:y_centroid+ap_rad+1, x_centroid-ap_rad:x_centroid+ap_rad+1]
    aperture = np.copy(aperture_data)
    sky_data = data[y_centroid-sky_outrad:y_centroid+sky_outrad+1, x_centroid-sky_outrad:x_centroid+sky_outrad+1]
    sky = np.copy(sky_data)

    excluded_pixels = 0
    included_values = np.array([])

    for i in range(len(sky)):
        for j in range(len(sky[0])):
            distance = np.sqrt((x_centroid-(j+x_centroid-sky_outrad))**2+(y_centroid-(i+y_centroid-sky_outrad))**2) #NOTEEE
            #distance = np.linalg.norm(np.array([i-sky_outrad, j-sky_outrad]))
            if (distance <= sky_inrad or distance >= sky_outrad):
                sky[i][j] = 0
                excluded_pixels += 1
            else:
                included_values = np.append(included_values, sky[i][j])

    n_annulus = (2*sky_outrad+1)**2-excluded_pixels
    background = np.median(included_values)

    excluded_num_aperture = 0
    for i in range(len(aperture)):
        for j in range(len(aperture[0])):
            distance = np.sqrt((x_centroid - (j+x_centroid-ap_rad))**2 + (y_centroid - (i+y_centroid-ap_rad))**2)
            #distance = np.linalg.norm(np.array([i-ap_rad, j-ap_rad]))
            if (distance > ap_rad):
                aperture[i][j] = 0
                excluded_num_aperture += 1    
    
    n_aperture = (2*ap_rad+1)**2 - excluded_num_aperture
    print(aperture)
    print('aperture', n_aperture)
    print("annulus", n_annulus)
    print('ap signal', aperture.sum())
    print('background', background)
    #background = 1244.5
    print('check', aperture.sum(), n_aperture, background)
    signal = aperture.sum() - n_aperture * background

    m_inst = -2.5*math.log10(signal)
    SNR = signal/np.sqrt(signal+n_aperture*(1+n_aperture/n_annulus)*(background+dark_current+read_noise**2))
    sig_m_inst = 1.0875/SNR

    # Do not modify these print statements
    print("Centroid at: ({}, {})".format(round(x,2),round(y,2)))
    print("Signal:", int(signal), "+/-", int(signal/SNR), "ADU")
    print("SNR:", round(SNR,1))
    print("m_inst:", round(m_inst,2), "+/-", round(sig_m_inst,2), "mag")

    return

ap_phot("D:/SSP/AP/aptest.fit",490,293,5,8,13)

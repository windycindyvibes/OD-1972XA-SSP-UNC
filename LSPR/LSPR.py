import numpy as np
import math 
from astropy.io import fits

def get_percent_error(expected, calculated):
    percent_error = abs((calculated - expected) / expected) * 100
    return percent_error

def get_plate_constants(x, y, ra, dec):
    n = len(x)
    sum_x = np.sum(x)
    sum_y = np.sum(y)
    sum_ra = np.sum(ra)
    sum_dec = np.sum(dec)
    mat1 = [[n, sum_x, sum_y], [sum_x, np.dot(x,x), np.dot(x,y)], [sum_y, np.dot(x,y), np.dot(y,y)]]
    mat2 = [[sum_ra], [np.dot(x, ra)], [np.dot(y, ra)]]
    mat3 = [[sum_dec], [np.dot(x, dec)], [np.dot(y, dec)]]

    mat1 = np.linalg.inv(mat1)
    print(mat1)
    pc_ra = np.dot(mat1, mat2)
    pc_dec = np.dot(mat1, mat3)

    return pc_ra, pc_dec

def get_uncertainty_pc(pc_ra, pc_dec, x, y, ra, dec, n):
    sigma_ra_arr = [((ra[i]-pc_ra[0]-pc_ra[1]*x[i]-pc_ra[2]*y[i])**2) for i in range(n)]
    sigma_dec_arr = [((dec[i]-pc_dec[0]-pc_dec[1]*x[i]-pc_dec[2]*y[i])**2)for i in range(n)]

    sigma_ra = np.sqrt(np.sum(sigma_ra_arr)/(n-3))
    sigma_dec = np.sqrt(np.sum(sigma_dec_arr)/(n-3))

    return sigma_ra, sigma_dec

def hours_to_degrees(time):
    hours, minutes, seconds = map(float, time.split(':'))
    degrees = hours + minutes / 60.0 + seconds / 60.0 / 60.0
    return degrees*15

def arc_to_degrees(time):
    deg, arcmin, arcsec = map(float, time.split(':'))
    neg = False
    if deg < 0:
        deg *= -1
        neg = True
    degrees = float(deg) + arcmin/60.0 + arcsec/3600.0
    if neg:
        return -1*degrees
    return degrees

def degree_to_hours(deg):
    deg /= 15
    hours = math.floor(deg)
    deg = (deg-hours)*60
    min = math.floor(deg)
    deg = (deg-min)*60
    sec = float(deg)
    return str(hours) + ':' + str(min) + ':' + str(sec)

def degree_dec_to_degree(deg_old):
    deg = abs(deg_old)
    one = math.floor(deg)
    deg = (deg-one)*60
    two = math.floor(deg)
    deg = (deg-two)*60
    three = float(deg)
    if deg_old < 0:
        return '-' + str(one) + ':' + str(two) + ':' + str(three)
    else:
        return str(one) + ':' + str(two) + ':' + str(three)

def get_lspr_coeff(x, y, ra, dec):
    c1, c2 = get_plate_constants(x, y, ra, dec)
    sigma_ra, sigma_dec = get_uncertainty_pc(c1, c2, x, y, ra, dec, len(x))

def get_astrometry(r, pc_ra, pc_dec):
    ra = pc_ra[0] + pc_ra[1]*r[0] + pc_ra[2]*r[1]
    dec = pc_dec[0] + pc_dec[1]*r[0] + pc_dec[2]*r[1]
    return ra, dec

def read_test_input(filename):
    x = []
    y = []
    ra = []
    dec = []
    with open(filename, 'r') as file:
        for line in file:
            values = line.strip().split()
            x.append(float(values[0]))
            y.append(float(values[1]))
            ra.append(hours_to_degrees(values[2]))
            dec.append(arc_to_degrees(values[3]))
    return x, y, ra, dec

def findCentroid(fits_file, target_x, target_y, radius=3, sky_radius=5):
# YOUR CODE HERE
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

x, y, ra, dec = read_test_input("D:/SSP/LSPR/LSPRtestinput1.txt")
pc_ra, pc_dec = get_plate_constants(x, y, ra, dec)
pc_ra = pc_ra[:, 0]
pc_dec = pc_dec[:, 0]
print('b1: ' + str(float(pc_ra[0])) + '\nb2: ' + str(float(pc_dec[0])))
print('a11: ' + str(float(pc_ra[1])) + '\na12: ' + str(float(pc_ra[2])))
print('a21: ' + str(float(pc_dec[1])) + '\na22: ' + str(float(pc_dec[2])))
sigma_ra, sigma_dec = get_uncertainty_pc(pc_ra, pc_dec, x, y, ra, dec, len(x))
print('RA uncertainty ' + str(sigma_ra*3600))
print('DEC uncertainty ' + str(sigma_dec*3600))
r = [484.35,382.62]
ra, dec = get_astrometry(r, pc_ra, pc_dec)
print('RA: ' + str(degree_to_hours(ra)))
print('DEC: ' + str(degree_dec_to_degree(dec)))

with open('D:/SSP/LSPR/06_24_light_01_reference_stars.txt', 'r') as file:
        ra = []
        dec = []
        target_x = []
        target_y = []
        for line in file:
            print(line)
            values = line.strip().split()
            print(values)
            ra.append(float(values[0]))
            dec.append(float(values[1]))
            target_x.append(np.round(float(values[2])))
            target_y.append(np.round(float(values[3])))

path = "D:/SSP/LSPR/06_24_light_01_new2.fits"

centroid_x = []
centroid_y = []

for i in range(len(target_x)):
    print(target_x[i])
    print(target_y[i])
    c_x, c_y = findCentroid(path, int(target_x[i]), int(target_y[i]), 3, 5)
    centroid_x.append(c_x)
    centroid_y.append(c_y)

pc_ra, pc_dec = get_plate_constants(centroid_x, centroid_y, ra, dec)

image_x = 1318.0526
image_y = 1691.6152

constant = 530.0/3056.0
image_x *= constant
image_y *= constant

r_image = [image_x, image_y]
ra_image, dec_image = get_astrometry(r_image, pc_ra, pc_dec)

sigma_ra, sigma_dec = get_uncertainty_pc(pc_ra, pc_dec, centroid_x, centroid_y, ra, dec, len(centroid_x))

print(pc_ra)
print(pc_dec)

ra_real = '13:55:37.03'
dec_real = '-06:34:20.6'

print('calculated: ' + str(ra_image[0]))
print('real: ' + str(hours_to_degrees(ra_real)))
print(degree_to_hours(ra_image[0]))
print('RA error: ' + str(get_percent_error(hours_to_degrees(ra_real), ra_image[0])))
print(dec_image[0])
print(arc_to_degrees(dec_real))
print(degree_dec_to_degree(dec_image[0]))
print('DEC error: ' + str(get_percent_error(arc_to_degrees(dec_real), dec_image[0])))
print(sigma_ra*3600)
print(sigma_dec*3600)










    
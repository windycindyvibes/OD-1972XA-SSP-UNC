from .OD3 import *
from .OD2 import *
from .NewtonRaphson import *
import numpy as np
import math

k = 0.01720209894
mu = 1.000000
r_earth_sun = [-6.574011189521245E-01, 7.092445973782825E-01, 3.074588267894852E-01]
gauss_conversion = 365.2568983/2/math.pi

def get_mean_anomaly_time(time, curr_time, semimajor_axis):
    return 1/np.sqrt(semimajor_axis**3)*(get_jd(time)/gauss_conversion - get_jd(curr_time)/gauss_conversion)

def get_mean_anomaly_time_jd_time(time, curr_time, semimajor_axis):
    return 1/np.sqrt(semimajor_axis**3)*(time/gauss_conversion - curr_time/gauss_conversion)

def get_ra_dec(position, velocity, time, curr_time, tolerance):
    e = get_eccentricity(position, velocity)
    a = get_semimajor_axis(position, velocity)
    M = get_mean_anomaly_time(time, curr_time, a) + get_mean_anomaly(position, velocity)
    E = newton_method(M, e, tolerance)

    r = [[0.0], [0.0], [0.0]]
    r[0][0] = a*np.cos(E)-a*e
    r[1][0] = a*np.sqrt(1-e**2)*np.sin(E)

    o = get_longitude(position, velocity)
    i = get_inclination(position, velocity)
    w = get_argument(position, velocity)
    epi = 23.439281*math.pi/180

    mat1 = [[np.cos(o), -np.sin(o), 0], [np.sin(o), np.cos(o), 0], [0, 0, 1]]
    mat2 = [[1, 0, 0], [0, np.cos(i), -np.sin(i)], [0, np.sin(i), np.cos(i)]]
    mat3 = [[np.cos(w), -np.sin(w), 0], [np.sin(w), np.cos(w), 0], [0, 0, 1]]
    mat4 = [[1, 0, 0], [0, np.cos(epi), -np.sin(epi)], [0, np.sin(epi), np.cos(epi)]]
    r1 = np.dot(mat4, np.dot(mat1, np.dot(mat2, np.dot(mat3, r))))
    
    r_2 = [r1[0][0], r1[1][0], r1[2][0]]

    range = np.add(r_2, r_earth_sun)
    range = range/np.linalg.norm(range)

    dec = np.arcsin(range[2])
    ra = np.arccos(range[0]/np.cos(dec))
    ra = select_angle(np.arcsin(range[1]/np.cos(dec)), ra, range[0]/np.cos(dec))

    return ra, dec
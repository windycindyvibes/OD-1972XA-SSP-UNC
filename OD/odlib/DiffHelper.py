from .OD3 import *
from .OD2 import *
from .NewtonRaphson import *
import numpy as np
import math

def get_ra_dec_from_OD(position, velocity, sun, a, e, o, i, w, M, tolerance):
    E = newton_method(M, e, tolerance)

    r = [[0.0], [0.0], [0.0]]
    r[0][0] = a*np.cos(E)-a*e
    r[1][0] = a*np.sqrt(1-e**2)*np.sin(E)

    o = get_longitude(position, velocity)
    i = get_inclination(position, velocity)
    w = get_argument(position, velocity)
    epi = math.radians(23.439281)

    mat1 = [[np.cos(o), -np.sin(o), 0], [np.sin(o), np.cos(o), 0], [0, 0, 1]]
    mat2 = [[1, 0, 0], [0, np.cos(i), -np.sin(i)], [0, np.sin(i), np.cos(i)]]
    mat3 = [[np.cos(w), -np.sin(w), 0], [np.sin(w), np.cos(w), 0], [0, 0, 1]]
    mat4 = [[1, 0, 0], [0, np.cos(epi), -np.sin(epi)], [0, np.sin(epi), np.cos(epi)]]
    r1 = np.dot(mat4, np.dot(mat1, np.dot(mat2, np.dot(mat3, r))))
    
    r_2 = [r1[0][0], r1[1][0], r1[2][0]]

    range = np.add(r_2, sun)
    range = range/np.linalg.norm(range)

    dec = np.arcsin(range[2])
    ra = np.arccos(range[0]/np.cos(dec))
    ra = select_angle(np.arcsin(range[1]/np.cos(dec)), ra, range[0]/np.cos(dec))

    return ra, dec
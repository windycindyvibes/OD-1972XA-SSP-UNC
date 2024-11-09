import odlib
import numpy as np
import math

def get_ra_dec(a, e, M, o, i, w, sun, tolerance):
    E = odlib.newton_method(M, e, tolerance)

    r = [[0.0], [0.0], [0.0]]
    r[0][0] = a*np.cos(E)-a*e
    r[1][0] = a*np.sqrt(1-e**2)*np.sin(E)

    epi = 23.439281*math.pi/180

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
    print('ra', math.degrees(ra))
    ra = odlib.select_angle(np.arcsin(range[1]/np.cos(dec)), ra, range[0]/np.cos(dec))

    return ra, dec

# a = 1.8962438188689117
# e = 0.5378407335664053
# i = np.radians(41.35867805379716)  
# o = np.radians(63.39172506103105)  
# w = np.radians(293.1079621092694)  
# nu = np.radians(238.2246716278443) 
# M = np.radians(307.76614925788664)
# r3 = [-0.8561365679200583, -1.4441450945212515, -0.5560580412362217]
# tolerance = 1E-12
# r_sun = [-1.328846762749651E-01, 9.247459382381787E-01, 4.008654716735506E-01]

a = 2.2242792302242833
e = 0.28070544606619513
i = np.radians(9.958717986583935)   
o = np.radians(120.04214798970074)  
w = np.radians(185.2517593695463)  
M = np.radians(3.351319891971652E+02)
tolerance = 1E-12
r_sun = [-1.830897377703347E-01, 9.175716031097462E-01, 3.977577672361769E-01]

# a = 2.224969688258735E+00
# e = 2.809193479432471E-01 
# i = np.radians(9.977577397374057E+00)  
# o = np.radians(1.199984577991981E+02)  
# w = np.radians(1.852904222502092E+02)  
# M = np.radians(3.351319891971652E+02)
# tolerance = 1E-12
# r_sun = [-1.830897377703347E-01, 9.175716031097462E-01, 3.977577672361769E-01]

# ra_true = 207.706875
# dec_true = -7.90908333333
ra_true = 238.0880708
dec_true = -6.90525000

ra, dec = get_ra_dec(a, e, M, o, i, w, r_sun, tolerance)
print('ra', math.degrees(ra), 'percent error', (ra_true - math.degrees(ra))/360*100, 'arcsecond error', 3600*abs(math.degrees(ra)-ra_true))
print('dec', math.degrees(dec), 'percent error', (dec_true - math.degrees(dec))/360*100, 'arcsecond error', 3600*abs(math.degrees(dec)-dec_true))

print(odlib.get_jd('03:08:00 UT on June 13, 2024'))

import odlib
import math

r = [5.939980793970498E+07, -1.832684174377829E+08, 7.102046951975648E+07]
v = [1.973659030148810E+01, 4.640012630472489E+00, 6.494439731611566E+00]
curr_time =  '00:00:00 UT on July 14, 2018'
time = '00:00:00 UT on August 3, 2018'

ra, dec = odlib.get_ra_dec(r, v, time, curr_time, 1E-06)
print(ra)
print('ra: ' + str(ra*180/math.pi))
print(dec)
print('dec: ' + str(dec*180/math.pi))



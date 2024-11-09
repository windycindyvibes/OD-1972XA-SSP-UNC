import odlib
import numpy as np

r = [5.939980793970498E+07, -1.832684174377829E+08, 7.102046951975648E+07]
v = [1.973659030148810E+01, 4.640012630472489E+00, 6.494439731611566E+00]

filename = 'D:/SSP/OD/WangInput2.txt'

with open(filename, 'r') as file:
    lines = file.readlines()

    line1 = lines[0].strip().split()
    line2 = lines[1].strip().split()
    line3 = lines[2].strip().split()
    line4 = lines[3].strip().split()

    for j in range(0, len(line1)):
        if line1[j].startswith("EC"):
            try:
                e = float(line1[j+1])
            except ValueError:
                e = float(line1[j+2])
        if line1[j].startswith("IN"):
            try:
                inc = float(line1[j+1])
            except ValueError:
                inc = float(line1[j+2])
    
    for i in range(0, len(line2)):
        if line2[i].startswith("OM"):
            try:
                o = float(line2[i+1]) # longitude of ascending node
            except ValueError:
                o = float(line2[i+2])
        if line2[i].startswith("W"):
            try:
                w = float(line2[i+1]) # argument of perihelion
            except ValueError:
                w = float(line2[i+2])

    for i in range(0, len(line3)):
        if line3[i].startswith("TA"):
            ta = float(line3[i+1]) # mean anomaly

    for i in range(0, len(line4)):
        if line4[i].startswith("A") and (not line4[i].startswith("AD")):
            try:
                a = float(line4[i+1])
            except ValueError:
                a = float(line4[i+2])

a = odlib.km_to_au(a)
inc = odlib.deg_to_rad(inc)
o = odlib.deg_to_rad(o)
w = odlib.deg_to_rad(w)
ta = odlib.deg_to_rad(ta)

print('angular momentum: ' + str(odlib.get_angular_momentum(r, v)))
print('semimajor axis: ' + 'expected value ' + str(a) + 'AU' + ' calculated value ' + str(odlib.get_semimajor_axis(r, v)) + 'AU' + ' percent error ' + str(odlib.get_percent_error(a, odlib.get_semimajor_axis(r, v))) + '%')
print('eccentricity: ' + 'expected value ' + str(e) + ' calculated value ' + str(odlib.get_eccentricity(r, v)) + ' percent error ' + str(odlib.get_percent_error(e, odlib.get_eccentricity(r, v))) + '%')
print('inclination: ' + 'expected value ' + str(inc) + ' rad' + ' calculated value ' + str(odlib.get_inclination(r, v)) + ' rad' + ' percent error ' + str(odlib.get_percent_error(inc, odlib.get_inclination(r, v))) + '%')
print('longitude of ascending node: ' + 'expected value ' + str(o) + ' rad' + ' calculated value ' + str(odlib.get_longitude(r, v)) + ' rad' + ' percent error ' + str(odlib.get_percent_error(o, odlib.get_longitude(r, v))) + '%')
print('argument of perihelion: ' + 'expected value ' + str(w) + ' rad' + ' calculated value ' + str(odlib.get_argument(r, v)) + ' rad' + ' percent error ' + str(odlib.get_percent_error(w, odlib.get_argument(r, v))) + '%')
print('true anomaly ' + 'expected value ' + str(ta) + ' rad' + ' calculated value ' + str(odlib.get_true_anomaly(r, v)) + ' rad' + ' percent error ' + str(odlib.get_percent_error(ta, odlib.get_true_anomaly(r, v))) + '%')

print('hi')
print(odlib.get_U(r,v))
print(odlib.get_true_anomaly(r,v))
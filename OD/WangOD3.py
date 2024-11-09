import odlib
import numpy as np

r = [5.939980793970498E+07, -1.832684174377829E+08, 7.102046951975648E+07]
v = [1.973659030148810E+01, 4.640012630472489E+00, 6.494439731611566E+00]
time =  '00:00:00 UT on July 14, 2018'

filename = 'D:/SSP/OD/WangInput2.txt'

with open(filename, 'r') as file:
    lines = file.readlines()

    line1 = lines[0].strip().split()
    line2 = lines[1].strip().split()
    line3 = lines[2].strip().split()
    line4 = lines[3].strip().split()

    for j in range(0, len(line2)):
        if line2[j].startswith("Tp"):
            try:
                Tp = float(line2[j+1])
            except ValueError:
                Tp = float(line2[j+2])
    for j in range(0, len(line3)):
        if line3[j].startswith("MA"):
            try:
                MA = float(line3[j+1])
            except ValueError:
                MA = float(line3[j+2])

print(Tp)
print(MA)
print('hi')

print(odlib.get_mean_anomaly(r, v))
print(odlib.get_percent_error(MA, odlib.get_mean_anomaly(r,v)))
print(odlib.get_jd_perihelion(r,v,time))
print(odlib.get_percent_error(Tp, odlib.get_jd_perihelion(r,v, time)))


import odlib
import math
import numpy as np
from WangODFunction import execute_OD
import matplotlib.pyplot as plt

k = 0.0172020989484 #Gaussian gravitational constant
cAU = 173.144643267 #speed of light in au/(mean solar)day
eps = math.radians(23.4374) #Earth's obliquity
order = 4
mu = 1
tolerance = 1E-12
JD_curr = 2459419.7916667
runs = 10000
print('runs', runs)

# JPL Values
a_jpl = 1.89340261181919
e_jpl = .5384716698244796
i_jpl = math.radians(41.2022527220293)
w_jpl = math.radians(293.0902755463004)
o_jpl = math.radians(63.4965666353897)
T_jpl = k*odlib.get_jd('19:53:35 UT on January 19, 2017')

time = []
ra = []
dec = []
sun = []
ra_uncertainty = [0.3833687127393558, 0.1957121745845234, 0.09847258809665424]
dec_uncertainty = [0.4000558612867812, 0.19003325280048697, 0.06688836410135077]
ra_uncertainty = [math.radians(value/3600) for value in ra_uncertainty]
dec_uncertainty = [math.radians(value/3600) for value in dec_uncertainty]

filename = 'E:/SSP/OD/2024-1972XA-testinput.txt'

a_offset = []
e_offset = []
i_offset = []
w_offset = []
o_offset = []
MA_offset = []

with open(filename, 'r') as file:
    lines = file.readlines()
    lines = [lines[0], lines[2], lines[7]]
    for line in lines:
        line_arr = line.strip().split()
        time.append(odlib.process_time(line_arr[0], line_arr[1], line_arr[2], line_arr[3]))
        ra.append(odlib.deg_to_rad(odlib.hours_to_degrees(line_arr[4])))
        dec.append(odlib.deg_to_rad(odlib.arc_to_degrees(line_arr[5])))
        sun.append([float(line_arr[6]), float(line_arr[7]), float(line_arr[8])])

if len(time) > 3:
    indices = str(input("What are the indices of the observations you want? (0 indexed)")).split(',')
    time = [time[indices[0]], time[indices[1]], time[indices[2]]]
    ra = [ra[indices[0]], ra[indices[1]], ra[indices[2]]]
    dec = [dec[indices[0]], dec[indices[1]], dec[indices[2]]]
    sun = [sun[indices[0]], sun[indices[1]], sun[indices[2]]]

print('ra', ra)
print('dec', dec)

ra_offset = []
dec_offset = []
for i in range(runs):
    ra_offset_app = []
    dec_offset_app = []
    for i in range(len(ra)):
        ra_offset_app.append(np.random.normal(ra[i], ra_uncertainty[i]))
        dec_offset_app.append(np.random.normal(dec[i], dec_uncertainty[i]))
    ra_offset.append(ra_offset_app)
    dec_offset.append(dec_offset_app)

for i in range(runs):
    try:
        a, e, inc, w, o, MA = execute_OD(time, ra_offset[i], dec_offset[i], sun)
        a_offset.append(a)
        e_offset.append(e)
        i_offset.append(inc)
        w_offset.append(w)
        o_offset.append(o)
        MA_offset.append(MA)
    except:
        print('There was an error')

MA_offset = [math.degrees(value) for value in MA_offset]

print('STD uncertainty values')
print('a STD: ', np.std(a_offset))
print('e STD: ', np.std(e_offset))
print('i STD: ', np.std(i_offset))
print('w STD: ', np.std(w_offset))
print('o STD: ', np.std(o_offset))
print('T STD: ', np.std(MA_offset))

#fig, axs = plt.subplots(3, 2)

# plt.hist(perihelion_offset, bins = 30, zorder=2, linewidth=3)
# plt.axvline(np.mean(perihelion_offset), linestyle='dashed', color='orange', label='Mean', linewidth=2)
# plt.axvline(np.mean(perihelion_offset)-np.std(perihelion_offset), linestyle='dashed', color='orange', linewidth=2)
# plt.axvline(np.mean(perihelion_offset)+np.std(perihelion_offset), linestyle='dashed', color='orange', linewidth=2)
# plt.axvline(T_jpl, linestyle='solid', label='JPL value', linewidth=2)
# plt.title('last perihelion passage (Gaussian Days)', loc='center')
# plt.legend()

plt.hist(MA_offset, bins = 30, zorder=2, linewidth=3)
plt.axvline(np.mean(MA_offset), linestyle='dashed', color='orange', linewidth=1)
plt.axvline(np.mean(MA_offset)-np.std(MA_offset), linestyle='dashed', color='orange', linewidth=2)
plt.axvline(np.mean(MA_offset)+np.std(MA_offset), linestyle='dashed', color='orange', linewidth=2)
#plt.axvline(T_jpl, linestyle='solid', linewidth=1)
plt.title('Mean Anomaly (Degrees)')

# #axs[0, 0].hist(a_offset, bins=30, range=(1.5,2.1))
# axs[0,0].hist(a_offset, bins = 30, zorder=2, linewidth=3)
# axs[0, 0].axvline(np.mean(a_offset), linestyle='dashed', color='orange', linewidth=1)
# axs[0, 0].axvline(np.mean(a_offset)-np.std(a_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[0, 0].axvline(np.mean(a_offset)+np.std(a_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[0, 0].axvline(a_jpl, linestyle='solid', linewidth=1)
# axs[0, 0].set_title('semimajor axis')

# axs[0,1].hist(e_offset, bins = 30, zorder=2, linewidth=3)
# axs[0, 1].axvline(np.mean(e_offset), linestyle='dashed', linewidth=1)
# axs[0, 1].axvline(np.mean(e_offset)-np.std(e_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[0, 1].axvline(np.mean(e_offset)+np.std(e_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[0, 1].axvline(e_jpl, linestyle='solid', linewidth=1)
# axs[0, 1].set_title('eccentricity')

# axs[1,0].hist(i_offset, bins = 30, zorder=2, linewidth=3)
# axs[1, 0].axvline(np.mean(i_offset), linestyle='dashed', linewidth=1)
# axs[1, 0].axvline(np.mean(i_offset)-np.std(i_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[1, 0].axvline(np.mean(i_offset)+np.std(i_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[1, 0].axvline(i_jpl, linestyle='solid', linewidth=1)
# axs[1, 0].set_title('inclination')

# axs[1,1].hist(w_offset, bins = 30, zorder=2, linewidth=3)
# axs[1, 1].axvline(np.mean(w_offset), linestyle='dashed', linewidth=1)
# axs[1, 1].axvline(np.mean(w_offset)-np.std(w_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[1, 1].axvline(np.mean(w_offset)+np.std(w_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[1, 1].axvline(w_jpl, linestyle='solid', linewidth=1)
# axs[1, 1].set_title('argument of perihelion')

# axs[2,0].hist(o_offset, bins = 30, zorder=2, linewidth=3)
# axs[2, 0].axvline(np.mean(o_offset), linestyle='dashed', linewidth=1)
# axs[2, 0].axvline(np.mean(o_offset)-np.std(o_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[2, 0].axvline(np.mean(o_offset)+np.std(o_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[2, 0].axvline(o_jpl, linestyle='solid', linewidth=1)
# axs[2, 0].set_title('longitude of ascending node')

# axs[2,1].hist(perihelion_offset, bins = 30, zorder=2, linewidth=3)
# axs[2, 1].axvline(np.mean(perihelion_offset), linestyle='dashed', linewidth=1)
# axs[2, 1].axvline(np.mean(perihelion_offset)-np.std(perihelion_offset), linestyle='dashed', color='orange', linewidth=2)
# axs[2, 1].axvline(np.mean(perihelion_offset)+np.std(perihelion_offset), linestyle='dashed', color='orange', linewidth=2)
# #axs[2, 1].axvline(T_jpl, linestyle='solid', linewidth=1)
# axs[2, 1].set_title('last perihelion')

# print('period', T_jpl)

#plt.subplots_adjust(hspace=0.5)
plt.show()





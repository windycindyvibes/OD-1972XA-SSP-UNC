import odlib
import math
import numpy as np

k = 0.0172020989484 #Gaussian gravitational constant
cAU = 173.144643267 #speed of light in au/(mean solar)day
eps = math.radians(23.4374) #Earth's obliquity
order = 4
mu = 1
tolerance = 1E-12
JD_curr = 2459419.7916667

def trueAnomaly_sharv(r, v, a, eccent):
    h_mag = np.linalg.norm(odlib.get_angular_momentum(r, v))
    r, v = odlib.convert_units(r, v)
    sin = ((a*(1-eccent**2))/(eccent*h_mag))*(np.dot(r,v)/np.linalg.norm(r))
    cos = (1/eccent)*(((a*(1-eccent**2))/np.linalg.norm(r))-1)
    print('sin', sin)
    if(sin>0 and cos>0):
        return math.asin(sin)
    if(sin>0 and cos<0):
        return math.acos(cos)
    if(sin<0 and cos>0):
        return 2*math.pi-math.acos(cos)
    if(sin<0 and cos<0):
        return math.pi-math.asin(sin)

def meanAnomaly_sharv(a, e, r, v):
    tA = trueAnomaly_sharv(r, v, a, e)
    r, v = odlib.convert_units(r, v)
    r_mag = np.sqrt(r[0]**2 + r[1]**2 + r[2]**2)
    e_anomaly = math.acos((1/e)*(1-(r_mag/a)))
    if(tA>math.pi):
        e_anomaly = 2*math.pi-e_anomaly
    mean_anomaly = e_anomaly - e*math.sin(e_anomaly)
    mean_anomaly = math.degrees(mean_anomaly)
    return mean_anomaly

# JPL Values
a_jpl = 3.421107170082002
e_jpl = .6771112824699317
i_jpl = 56.15414124494419
w_jpl = 300.8771350337092
o_jpl = 253.0162757620894 
T_jpl = odlib.get_jd('19:53:35 UT on January 19, 2017')
MA_jpl = 3.062537977217498E+02
r2_jpl = [-9.186211933168181E-0, -1.470878233034030E+00, -5.166596850013402E-01]
r2mag_jpl = np.linalg.norm(r2_jpl)
r2dot_jpl = [1.049136000422564E-02, 4.349273298759830E-03, -6.467467084762222E-03]
r2dotmag_jpl = np.linalg.norm(r2dot_jpl)

time = []
ra = []
dec = []
sun = []

filename = 'E:/SSP/viviinput.txt'

with open(filename, 'r') as file:
    lines = file.readlines()
    lines = [lines[8], lines[9], lines[10]]
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

rhohat = []
for i in range(len(ra)):
    rhohat.append(odlib.get_rhohat(ra[i], dec[i]))

print('rhohat', rhohat)

Ds = odlib.get_Ds(rhohat, sun)
taus = [k*(time[0]-time[1]), k*(time[2]-time[1]), k*(time[2]-time[0])] # t1, t3, t0
roots, rhos = odlib.SEL(taus, sun[1], rhohat[1], Ds)
print('Ds', Ds)
print('taus', taus)
print('rhohat2', rhohat[1])
print('Sun2', sun[1])

positive_rhos = sum(1 for x in rhos if x > 0.05)

if positive_rhos != 1:
    print('rho values', rhos)
    index = int(input("which rho value do you want? enter a zero-indexed value"))
    if rhos[index] < 0.05:
        index = int(input("please select a positive rho value"))
else:
    for i in range(len(rhos)):
        if rhos[i] > 0.05:
            index = i 

r2 = roots[index]
rho = rhos[index]

f1_i = odlib.get_f_init(r2, taus[0])
g1_i = odlib.get_g_init(r2, taus[0])
f3_i = odlib.get_f_init(r2, taus[1])
g3_i = odlib.get_g_init(r2, taus[1])

c1_i = g3_i/(f1_i*g3_i-g1_i*f3_i)
c2_i = -1
c3_i = -g1_i/(f1_i*g3_i-g1_i*f3_i)

c_i = [c1_i, c2_i, c3_i]

d1_i, d3_i = odlib.get_d(f1_i, f3_i, g1_i, g3_i)

rho_i = odlib.get_rhos(c_i, rhohat, sun)
r_i = odlib.get_r(rho_i, rhohat, sun)

r2dot_init = []
for i in range(len(r_i[0])):
    r2dot_init.append(d1_i*r_i[0][i] + d3_i*r_i[2][i])

difference = tolerance + 1
iterations = 0

rho_init = rho
rhos_init = rho_i
r2_init = r_i[1]
taus_corrected = taus

print('Main Iteration Loop')
while (difference > tolerance):
    f1, g1 = odlib.fg(taus_corrected[0], r2_init, r2dot_init, order)
    f3, g3 = odlib.fg(taus_corrected[1], r2_init, r2dot_init, order)
    print('fg', f1, f3, g1, g3)

    c1 = g3/(f1*g3-g1*f3)
    c2 = -1
    c3 = -g1/(f1*g3-g1*f3)

    c = [c1, c2, c3]
    print('c', c)

    d1, d3 = odlib.get_d(f1, f3, g1, g3)

    rho = odlib.get_rhos(c, rhohat, sun)
    r = odlib.get_r(rho, rhohat, sun)

    r2dot = []
    for i in range(len(r[0])):
        r2dot.append(d1*r[0][i] + d3*r[2][i])
    
    difference = abs(rho[1]-rho_init)
    rho_init = rho[1]
    rhos_init = rho
    iterations += 1
    time_corrected, seconds_corrected = odlib.light_correction(time, rhos_init, cAU)
    taus_corrected = odlib.get_taus(time_corrected, k)
    print(str(iterations).zfill(2) + str(':'), 'change in rho2 =', difference, 'AU; light-travel time =', seconds_corrected, 'sec')
    r2_init = r[1]
    r2dot_init = r2dot

r2_ecliptic = odlib.equatorial_to_ecliptic(r2_init, eps)
r2dot_ecliptic = odlib.equatorial_to_ecliptic(r2dot_init, eps)

print()
print('In', iterations+1, 'iterations, r2 and r2dot converged to')
print('r2 =', r2_init, '=', np.linalg.norm(r2_init), 'AU')
print('r2dot =', r2dot_init, '=', np.linalg.norm(r2dot_init), 'AU/day')
print('in cartesian equatorial coordinates')

print('or')

print('r2 =', r2_ecliptic, '=', np.linalg.norm(r2_ecliptic), 'AU')
print('r2dot =', r2dot_ecliptic, '=', np.linalg.norm(r2dot_ecliptic), 'AU/day')
print('in cartesian ecliptic coordinates')

print('with rho2 =', rho_init, 'AU')

r2_converted, r2dot_converted = odlib.AU_to_km(r2_ecliptic, r2dot_ecliptic)

print()
print('ORBITAL ELEMENTS')
a = odlib.get_semimajor_axis(r2_converted, r2dot_converted)
e = odlib.get_eccentricity(r2_converted, r2dot_converted)
i = odlib.get_inclination(r2_converted, r2dot_converted)
w = odlib.get_argument(r2_converted, r2dot_converted)
o = odlib.get_longitude(r2_converted, r2dot_converted)
n = odlib.get_true_anomaly(r2_converted, r2dot_converted)
M = meanAnomaly_sharv(a, e, r2_converted, r2dot_converted)
MA_central = odlib.get_mean_anomaly_quad_check(r2_converted, r2dot_converted, n)
MA_future = odlib.get_mean_anomaly_time_jd_time(JD_curr, time[1], a) + odlib.get_mean_anomaly_quad_check(r2_converted, r2dot_converted, n)
E = odlib.get_eccentric_anomaly(r2_converted, r2dot_converted)
perihelion = odlib.get_jd_perihelion_jd_time(JD_curr, a, k, MA_future)

if not n < math.pi:
    E = 2*math.pi - E

print('a =', a, 'AU', 'percent error:', str(odlib.get_percent_error(a_jpl, a)) + '%')
print('e =', e, 'percent error:', str(odlib.get_percent_error(e_jpl, e)) + '%')
print('i =', math.degrees(i), 'degrees', 'percent error:', str(odlib.get_percent_error(i_jpl, math.degrees(i))) + '%')
print('omega =', math.degrees(w), 'degrees', 'percent error:', str(odlib.get_percent_error(w_jpl, math.degrees(w))) + '%')
print('Omega =', math.degrees(o), 'degrees', 'percent error:', str(odlib.get_percent_error(o_jpl, math.degrees(o))) + '%')
print('JD of last perihelion passage =', perihelion, 'percent error:', str(odlib.get_percent_error(T_jpl, perihelion)) + '%')

print()
print('Nu =', math.degrees(n), 'deg/day')
print('Mean anomaly sharv =', M, 'percent error', odlib.get_percent_error(MA_jpl, M))
print('M =', math.degrees(MA_central), 'degrees at central obs. (JD =', str(time[1]) + ')')
print('M =', math.degrees(MA_future), 'degrees at 07/24/2021 07:00 (JD =', str(JD_curr) + ')')
print('E =', math.degrees(E), 'degrees at central obs')


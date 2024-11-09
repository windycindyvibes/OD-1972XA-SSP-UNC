import odlib
import math
import numpy as np

months = ['January', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
mu = 1

def process_time(year, month, day, hour):
    month_str = months[int(month)-1]
    hour_split = hour.split(':')
    if float(hour_split[2]) == 0.0:
        time_str = hour.rstrip('.0') + '00 UT on ' + month_str + ' ' + str(day) + ', ' + str(year)
    else:
        time_str = hour.rstrip('.0') + ' UT on ' + month_str + ' ' + str(day) + ', ' + str(year)
    jd = odlib.get_jd(time_str)
    return jd

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
    
# RA DEC to rhohat and Ds
def get_rhohat(ra, dec):
    return [np.cos(ra)*np.cos(dec), np.sin(ra)*np.cos(dec), np.sin(dec)]

# D0, D21, D22, D23
def get_Ds(rhohat, sun):
    D0 = np.dot(rhohat[0], np.cross(rhohat[1], rhohat[2]))
    D21 = np.dot(np.cross(rhohat[0], sun[0]), rhohat[2])
    D22 = np.dot(np.cross(rhohat[0], sun[1]), rhohat[2])
    D23 = np.dot(np.cross(rhohat[0], sun[2]), rhohat[2])
    return [D0, D21, D22, D23]

def get_D0(rhohat):
    return np.dot(rhohat[0], np.cross(rhohat[1], rhohat[2]))

def get_D(rhohat, sun, i, j):
    if i == 1:
        return np.dot(np.cross(sun[j-1], rhohat[1]), rhohat[2])
    elif i == 2:
        return np.dot(np.cross(rhohat[0], sun[j-1]), rhohat[2])
    elif i == 3:
        return np.dot(rhohat[0], np.cross(rhohat[1], sun[j-1]))

def get_f_init(r2, tau):
    u = mu/r2**3
    return (1 - 0.5*u*tau**2)

def get_g_init(r2, tau):
    u = mu/r2**3
    return (tau - 1/6*(u*tau**3))

def get_rhos(c, rhohat, sun):
    rho1 = (c[0]*get_D(rhohat, sun, 1, 1) + c[1]*get_D(rhohat, sun, 1, 2) + c[2]*get_D(rhohat, sun, 1, 3))/(c[0]*get_D0(rhohat))
    rho2 = (c[0]*get_D(rhohat, sun, 2, 1) + c[1]*get_D(rhohat, sun, 2, 2) + c[2]*get_D(rhohat, sun, 2, 3))/(c[1]*get_D0(rhohat))
    rho3 = (c[0]*get_D(rhohat, sun, 3, 1) + c[1]*get_D(rhohat, sun, 3, 2) + c[2]*get_D(rhohat, sun, 3, 3))/(c[2]*get_D0(rhohat))
    return [rho1, rho2, rho3]

def get_r(rhos, rhohat, sun):
    r = []
    for i in range(len(rhos)):
        r.append(np.subtract(rhos[i]*np.array(rhohat[i]), np.array(sun[i])))
    r_list = [arr.tolist() for arr in r]
    return r_list

def get_d(f1, f3, g1, g3):
    d1 = -f3/(f1*g3-f3*g1)
    d3 = f1/(f1*g3-f3*g1)
    return d1, d3

def iterate_to_r2dot(f1, f3, g1, g3, rhohat, sun):
    c1 = g3/(f1*g3-g1*f3)
    c2 = -1
    c3 = -g1/(f1*g3-g1*f3)

    c = [c1, c2, c3]

    rho = odlib.get_rhos(c, rhohat, sun)
    r = odlib.get_r(rho, rhohat, sun)

    d1, d3 = odlib.get_d(f1, f3, g1, g3)

    r2dot = []
    for i in range(len(r[0])):
        r2dot.append(d1*r[0][i] + d3*r[2][i])

    return r, r2dot

def light_correction(time, rhos, c):
    time_arr = []
    for i in range(len(time)):
        time_arr.append(time[i] - rhos[i]/c)
        if i == 1:
            seconds_corrected = rhos[i]/c*86400
    return time_arr, seconds_corrected

def get_taus(time, k):
    taus = [k*(time[0]-time[1]), k*(time[2]-time[1]), k*(time[2]-time[0])] # t1, t3, t0
    return taus

def equatorial_to_ecliptic(mat, epi):
    rotation_mat = [[1,0,0], [0, np.cos(epi), np.sin(epi)], [0, -np.sin(epi), np.cos(epi)]]
    ecliptic_mat = np.dot(rotation_mat, mat)
    return ecliptic_mat
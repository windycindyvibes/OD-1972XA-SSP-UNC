from .OD1 import *
from .OD2 import *
import numpy as np
from datetime import datetime
import math

def get_eccentric_anomaly(position, velocity):
    e = get_eccentricity(position, velocity)
    a = get_semimajor_axis(position, velocity)
    position, velocity = convert_units(position, velocity)
    return np.arccos((1-np.linalg.norm(position)/a)/e)

def get_mean_anomaly(position, velocity):
    E_0 = get_eccentric_anomaly(position, velocity)
    e = get_eccentricity(position, velocity)
    return E_0-e*np.sin(E_0)

def get_mean_anomaly_quad_check(position, velocity, n):
    E_0 = get_eccentric_anomaly(position, velocity)
    if not n < math.pi:
        E_0 = 2*math.pi - E_0
    e = get_eccentricity(position, velocity)
    return E_0-e*np.sin(E_0)

def get_jd(time):
    date = datetime.strptime(time, '%H:%M:%S UT on %B %d, %Y')
    hour = date.hour
    minute = date.minute
    second = date.second
    year = date.year
    month = date.month
    day = date.day
    j = 367*year-math.floor(7*(year+math.floor((month+9)/12))/4)+math.floor(275*month/9)+day+1721013.5
    j += (hour+minute/60+second/3600)/24
    return j

def get_jd_perihelion(position, velocity, time):
    return get_jd(time) - np.sqrt(get_semimajor_axis(position, velocity)**3)*get_mean_anomaly(position, velocity)

def get_jd_perihelion_jd_time(JD_curr, a, k, MA_future):
    return JD_curr - np.sqrt(a**3/k**2)*MA_future



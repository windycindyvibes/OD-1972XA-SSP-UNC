import numpy as np
import math

def convert_units(position, velocity):
    # converts position vector from km to AU, velocity vector from km/sec to AU/Gaussian Day
    position = [6.6846E-09*float(value) for value in position]
    velocity = [6.6846E-09*5022642.89055*float(value) for value in velocity]

    return position, velocity

def AU_to_km(position, velocity):
    position = [1/6.6846E-09*float(value) for value in position]
    velocity = [1/6.6846E-09*1/5022642.89055*float(value) for value in velocity]

    return position, velocity

def get_percent_error(expected, calculated):
    percent_error = abs((calculated - expected) / expected) * 100
    return percent_error

def km_to_au(km):
    return (6.6846E-09*km)

def deg_to_rad(deg):
    return deg*np.pi/180

def normalize_angle(angle):
    while angle < 0:
        angle += 2 * math.pi
    while angle >= 2 * math.pi:
        angle -= 2 * math.pi
    return angle

def select_angle(arcsin, arccos, cos):
    if arccos == arcsin:
        return normalize_angle(arccos)
    else:
        if cos < 0:
            return normalize_angle(math.pi-arcsin)
        else:
            return normalize_angle(arcsin)

def get_angular_momentum(position, velocity):
    position, velocity = convert_units(position, velocity)
    angular_momentum = np.cross(position, velocity)
    angular_momentum = [round(value, 6) for value in angular_momentum]
    return angular_momentum

def get_semimajor_axis(position, velocity):
    position, velocity = convert_units(position, velocity)
    return float(1/(2/(np.linalg.norm(position)) - np.dot(velocity, velocity)))

def get_eccentricity(position, velocity):
    return np.sqrt(1-(np.linalg.norm(get_angular_momentum(position, velocity))**2)/get_semimajor_axis(position, velocity))

def get_inclination(position, velocity):
    h = get_angular_momentum(position, velocity)
    return np.arctan(np.sqrt(h[0]**2 + h[1]**2)/h[2])

def get_longitude(position, velocity):
    h = get_angular_momentum(position, velocity)
    i = get_inclination(position, velocity)
    x = -1*h[1]/np.linalg.norm(h)/np.sin(i)
    cos_o = np.arccos(x)
    sin_o = np.arcsin(h[0]/np.linalg.norm(h)/np.sin(i))
    return select_angle(sin_o, cos_o, x)

def get_U(position, velocity):
    i = get_inclination(position, velocity)
    o = get_longitude(position, velocity)
    position, velocity = convert_units(position, velocity)
    x = (position[0]*np.cos(o)+position[1]*np.sin(o))/np.linalg.norm(position)
    cos_u = np.arccos(x)
    sin_u = np.arcsin(position[2]/(np.linalg.norm(position)*np.sin(i)))
    return select_angle(sin_u, cos_u, x)

def get_true_anomaly(position, velocity):
    h = get_angular_momentum(position, velocity)
    e = get_eccentricity(position, velocity)
    a = get_semimajor_axis(position, velocity)
    position, velocity = convert_units(position, velocity)
    x = 1/e * (a*(1-e**2)/np.linalg.norm(position) - 1)
    sin_v = np.arcsin(a * (1-e**2) / (e*np.linalg.norm(h)) * (np.dot(position, velocity) / np.linalg.norm(position)))
    cos_v = np.arccos(x)
    return select_angle(sin_v, cos_v, x)

def get_argument(position, velocity):
    return normalize_angle(get_U(position, velocity) - get_true_anomaly(position, velocity))
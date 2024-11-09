import numpy as np
import math
from .OD2 import *

#tau1 = -0.32618569435308475 
#tau3 = 0.050840808143482484 
#r2 = [0.26640998194891174, -1.382856212643199, -0.505199925482389]
#r2dot = [0.8439832722802604, -0.39937767878456487, 0.14200790188593015]
#order = 3
sec_to_gaussian_day = 365.25636*86400/2/math.pi
c = 3*(10**8)*6.6846E-12*sec_to_gaussian_day
k = 1
mu = 1

def fg(tau,r2,r2dot,order): 
    r = np.linalg.norm(r2)
    #print(r)
    #tau -= r/c #WRONG
    u = mu/r**3
    z = np.dot(r2, r2dot)/r**2
    q = np.dot(r2dot, r2dot)/r**2-u

    if order == 4:
        f = 1-0.5*u*tau**2+0.5*u*z*tau**3+1/24*(3*u*q-15*u*z**2+u**2)*tau**4
        g = tau-1/6*u*tau**3+1/4*u*z*tau**4
    elif order == 3:
        f = 1-0.5*u*tau**2+0.5*u*z*tau**3
        g = tau-1/6*u*tau**3
    elif order == 0:
        f = newton_method(tau, r2, r2dot, 1E-12)
    return(f,g)

def f(x, tau,r2,r2dot):
    a = get_semimajor_axis(r2, r2dot)
    n = k * np.sqrt(mu/a**3)
    return x - (1-np.linalg.norm(r2)/a)*np.sin(x) + np.dot(r2, r2dot)/n/a**2*(1-np.cos(x)) - n*tau

def f_prime(x, tau, r2, r2dot):
    a = get_semimajor_axis(r2, r2dot)
    n = k * np.sqrt(mu/a**3)
    return 1-(1-np.linalg.norm(r2)/a)*np.cos(x) + np.dot(r2, r2dot)*np.sin(x)/n/a**2

def newton_method(tau, r2, r2dot, tol):
    a = get_semimajor_axis(r2, r2dot)
    n = k * np.sqrt(mu/a**3)
    e = get_eccentricity(r2, r2dot)
    sign = np.dot(r2, r2dot)*np.cos(n*tau-np.dot(r2, r2dot)/n/a**2)/n/a**2 + (1-np.linalg.norm(r2)/a)*np.sin(n*tau-np.dot(r2, r2dot)/n/a**2)
    if sign > 0:
        x_0 = n*tau + 0.85*e - np.dot(r2, r2dot)/n/a**2
    else:
        x_0 = n*tau - 0.85*e - np.dot(r2, r2dot)/n/a**2
    init = x_0
    diff = tol+1
    iterations = 0
    while (diff > tol):
        new = init - f(init, tau, r2, r2dot)/f_prime(init, tau, r2, r2dot)
        diff = abs(init-new)
        init = new
        iterations += 1
    return new

# f1,g1 = fg(tau1,r2,r2dot,order) 
# f3,g3 = fg(tau3,r2,r2dot,order)
# print(f1, g1)
# print(f3, g3)
#worked exactly
from vpython import *
import numpy as np

G = 6.67430e-11  
M_earth = 5.972e24  
M_sun = 1.989e30 

a = 1.8962438188689117
e = 0.5378407335664053
i = np.radians(41.35867805379716)  
Omega = np.radians(63.39172506103105)  
omega = np.radians(293.1079621092694)  
nu = np.radians(238.2246716278443) 

n = np.sqrt(G * (M_sun + M_earth) / a**3)
r_pqw = a * (1 - e**2) / (1 + e * np.cos(nu)) * np.array([np.cos(nu), np.sin(nu), 0])

R_pqw_to_ecliptic = np.array([[np.cos(omega), -np.sin(omega), 0],
                              [np.sin(omega), np.cos(omega), 0],
                              [0, 0, 1]])

r_ecliptic = np.dot(R_pqw_to_ecliptic, r_pqw)

scene = canvas(title='Orbit Simulation', width=800, height=600)

sun = sphere(pos=vector(0, 0, 0), radius=0.2, color=color.yellow)
earth = sphere(pos=vector(1, 0, 0), radius=0.1, color=color.blue)
asteroid = sphere(pos=vector(r_ecliptic[0], r_ecliptic[1], r_ecliptic[2]), radius=0.05, color=color.red)

while True:
    rate(1) 
    nu += n * 60
    r_pqw = a * (1 - e**2) / (1 + e * np.cos(nu)) * np.array([np.cos(nu), np.sin(nu), 0])
    
    r_ecliptic = np.dot(R_pqw_to_ecliptic, r_pqw)
    asteroid.pos = vector(r_ecliptic[0], r_ecliptic[1], r_ecliptic[2])

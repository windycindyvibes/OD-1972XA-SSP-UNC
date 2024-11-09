import odlib
import math

tau1 = -0.32618569435308475 
tau3 = 0.050840808143482484 
r2 = [0.26640998194891174, -1.382856212643199, -0.505199925482389]
r2dot = [0.8439832722802604, -0.39937767878456487, 0.14200790188593015]
order = 0
sec_to_gaussian_day = 365.25636*86400/2/math.pi
c = 3*(10**8)*6.6846E-09*sec_to_gaussian_day
k = 1
mu = 1

f1,g1 = odlib.fg(tau1,r2,r2dot,order) 
f3,g3 = odlib.fg(tau3,r2,r2dot,order)
print(f1, g1)
print(f3, g3)

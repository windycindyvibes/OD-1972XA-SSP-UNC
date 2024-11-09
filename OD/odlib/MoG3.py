import numpy as np
import math

def estimate_pi(n):
    count = 0
    for i in range(0, n):
        x = 2*np.random.random()
        y = 2*np.random.random()
        distance = np.sqrt((x-1)**2+(y-1)**2)
        if distance <= 1:
            count += 1
    pi = count / n * 4
    return pi

pis = []
n = 10000
for i in range(0, 100):
    pis = np.append(pis, estimate_pi(n))

mean = pis.mean()
#print('mean', mean)
#print('std', pis.std())
#print('percent error', (mean-math.pi)/math.pi*100)
import numpy as np
from numpy import roots

'''tau = [-0.15481889055, 0.15481889055, 0.3096377811] 
Sun2 = [-0.2398478458274071, 0.9065739917845802, 0.3929623749770952] 
rhohat2 = [-0.8518563498182248, -0.2484702599212149, 0.4610892421311239] 
Ds = [-0.0010461861084885213, -0.17297581974209159, -0.17201260125558127, 
-0.16712421570714076]'''
mu = 1

def SEL(tau,Sun2,rhohat2,Ds): 
    roots = [] 
    rhos = []  
    A_1 = tau[1]/tau[2]
    B_1 = A_1/6*(tau[2]**2-tau[1]**2)
    A_3 = -tau[0]/tau[2]
    B_3 = A_3/6*(tau[2]**2-tau[0]**2)
    A = (A_1*Ds[1]-Ds[2]+A_3*Ds[3])/(-Ds[0])
    B = (B_1*Ds[1]+B_3*Ds[3])/(-Ds[0])
    E = -2*np.dot(rhohat2, Sun2)
    F = (np.linalg.norm(Sun2)**2)
    a = -(A**2+A*E+F)
    b = -mu*(2*A*B+B*E)
    c = -mu**2*B**2
    coeff = [1, 0, a, 0, 0, b, 0, 0, c]
    root = np.roots(coeff)
    real_roots = []
    for value in root:
        if (np.imag(value) == 0.0):
            real_roots.append(value)
    for value in real_roots:
        if value > 0:
            roots.append(np.real(value))
    
    for value in roots:
        rhos.append(A + mu*B/value**3)
            
    return(roots,rhos)

#roots,rhos = SEL(tau,Sun2,rhohat2,Ds) 
#print(roots)
#print(rhos)
#worked exactly
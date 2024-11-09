import numpy as np
import math

def f(M, e, x):
    return (x-e*np.sin(x)-M)

def f_prime(M, e, x):
    return (1-e*np.cos(x))

def newton_method(M, e, tol):
    init = 0
    diff = tol+1
    iterations = 0
    while (diff > tol):
        new = init - f(M, e, init)/f_prime(M, e, init)
        diff = abs(init-new)
        init = new
        iterations += 1
    return new

def execute_newton_method(M, e, tol):
    E = newton_method(M, e, tol)
    print('E = ' + str(E))
    print('Convergence parameter = ' + str(tol))
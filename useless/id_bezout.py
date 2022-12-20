import euclide
import math


def getCoeffBezout(a, b):
    if b == 0:
        return 1,0
    else:
        u , v = getCoeffBezout(b , a % b)
        return v , u - (a//b)*v

def invWithBezout(a, mod):
    if euclide.pgcdEuclide(a,mod) == 1:
        inv = getCoeffBezout(a, mod)[0] % mod
        return inv 
    else:
        return "Pas possible de calculer l'inverse de {} avec cette méthode".format(a)




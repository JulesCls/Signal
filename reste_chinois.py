import id_bezout

def resteChinois(a, m):
    x = 0
    M = 1
    Mk = []
    y = []
    xk = []
    for i in m:
        M *= i
    for i in m:
        Mk.append(M/i)
    for i,j in zip(Mk,m):
        y.append(id_bezout.invWithBezout(i,j))
    for i,j,k in zip(a,y,Mk):
        xk.append(i*j*k)
    for i in xk:
        x += i
    return "x = {}".format(int(x % M))

print(resteChinois([2,5],[11,7]))
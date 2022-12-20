import math,timeit,inspect


def divisionEuclidienne(a, b):
    reste = a % b
    quotient = int((a-reste)/b)
    print("{} = {} * {} + {}".format(a, b, quotient, reste))
    return {"reste": reste, "quotient": quotient}


def pgcdEuclide(a, b):
    int(a)
    int(b)
    r = -1
    while r != 0:
        r = a % b
        q = (a-r)/b
        # print("{} = {} * {} + {}".format(a, b, q, r))
        a = b
        b = r
    return a

def recEuclide(a, b):
    if b == 0:
        return a
    else:
        return recEuclide(b, a % b)

def gcd(a, b):
    if(b == 0):
        return abs(a)
    else:
        return gcd(b, a % b)

if __name__ == "__main__":

    import_module = "import euclide"
    print(timeit.timeit(stmt='euclide.pgcdEuclide(45795047983469,55965347983469)',setup=import_module))
    print(timeit.timeit(stmt='euclide.recEuclide(45795047983469,55965347983469)',setup=import_module))
    print(timeit.timeit(stmt='math.gcd(45795047983469,55965347983469)',setup='import math'))
    print(timeit.timeit(stmt='numpy.gcd(45795047983469,55965347983469)',setup='import numpy'))
    print(timeit.timeit(stmt='euclide.gcd(45795047983469,55965347983469)',setup=import_module))
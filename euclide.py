import math


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

# print(divisionEuclidienne(781,127))
# print(pgcdEuclide(781,127))
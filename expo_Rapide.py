def exponentiationRapide(a,e,mod):
    result = 1
    while e > 0:
        if e%2 == 1:
            result = (result * a) % mod
        pass
        e = e//2
        a = (a*a) % mod
    return result

print(exponentiationRapide(13,172,23))


        
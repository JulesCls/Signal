import secrets, json, random

def expo_rapide(base, exponent, modulus):
  result = 1
  while exponent > 0:
    if exponent % 2 == 1:
      result = result * base % modulus
    exponent = exponent // 2
    base = base * base % modulus
  return result

def get_prime_number(length=2048):
    primaryNumber = None
    while primaryNumber==None:
        # print("generate prime")
        numToTest = secrets.randbits(length)
        if (rabin_miller(numToTest,40)):
            primaryNumber = numToTest
    return primaryNumber

def _find_generator_element(p):
    generatorElement = None
    p1 = p-1
    q = p1//2
    while not(generatorElement):
        g = secrets.randbelow(p1)
        v3 = expo_rapide(g,p1,p)
        if (v3 != 1):
            continue
        v1 = expo_rapide(g,q,p)
        v2 = expo_rapide(g,2,p)
        # print("testing generator")
        if len(set([p,v1,v2,v3])) == 4 and v3 == 1:
            generatorElement = g
    return generatorElement

def get_number_with_generator_element(length=2048):
    q = get_prime_number(length)
    p = q* 2 + 1
    while not(rabin_miller(p,40)):
        q = get_prime_number(length)
        p = q* 2 + 1
    g = _find_generator_element(p)
    return {"prime_number" : p, "generator_element" : g}
    

def get_prime_number_under_n(n):
    primeNumber = get_prime_number()
    if primeNumber < n :
        return primeNumber
    else:
        get_prime_number_under_n(n)

def write_to_file(data,filename):
    with open(filename,"w") as f:
        f.write(json.dumps(data))


def rabin_miller(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = expo_rapide(a,s,n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = expo_rapide(x,2,n)
            if x == n - 1:
                break
        else:
            return False
    return True

if __name__ == "__main__":

    print(bin(ord('é')))
    # n = 100
    # print(groupByBits(16,n))




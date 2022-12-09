def exponentiationRapide(a,e,mod):
    result = 1
    while e > 0:
        if e%2 == 1:
            result = (result * a) % mod
        pass
        e = e//2
        a = (a*a) % mod
    return result

def exponentiation_rapide(base, exposant, modulo):
  if exposant == 0:
    return 1
  elif exposant == 1:
    return base
  else:
    resultat = exponentiation_rapide(base, exposant // 2, modulo)
    resultat = (resultat * resultat) % modulo
    if exposant % 2 == 1:
      resultat = (resultat * base) % modulo
    return resultat


def mod_pow(base, exponent, modulus):
  result = 1
  while exponent > 0:
    if exponent % 2 == 1:
      result = result * base % modulus
    exponent = exponent // 2
    base = base * base % modulus
  return result
        
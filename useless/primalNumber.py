import  secrets, time, json, utils_old
from utils_old import expo_rapide

def isPrime(n):
  if n == 1:
    result = True
  else:
    for i in range(2,n):
        if (n%i) == 0:
            result = False
            break
    else:
        result = True  
    return result

def calculateNFirstPrimeNumber(n):
    primeNumbers = [2]
    numberToTest = 3
    while(len(primeNumbers) < n):
        for primeNumber in primeNumbers:
            if(numberToTest % primeNumber ) == 0:
                break
        else:
            primeNumbers.append(numberToTest)
        numberToTest+=1
    primeNumbers.insert(0,1)
    return(primeNumbers)
    
def calculatePrimeNumberUnderN(n):
    primeNumbers = [2]
    for i in range(3,n,2):
        for primeNumber in primeNumbers:
            if(i % primeNumber ) == 0:
                break
        else:
            primeNumbers.append(i)
    primeNumbers.insert(0,1)
    return(primeNumbers)

def acceleratedPrimeNumbersGeneration(n):
    sieve = [True] * (n//2)
    for i in range(3,int(n**0.5)+1,2):
        if sieve[i//2]:
            sieve[i*i//2::i] = [False] * ((n-i*i-1)//(2*i)+1)
    return [2] + [2*i+1 for i in range(1,n//2) if sieve[i]]


def primeFactorization(n, primeNumbers , factorsList = {}):
    if n in primeNumbers:
        utils_old.addIterationToDictionary(n,factorsList)
        return factorsList
    for i in primeNumbers:
        if n % i == 0:
            utils_old.addIterationToDictionary(i,factorsList)
            n //= i
            break
    primeFactorization(n,primeNumbers,factorsList)
    return factorsList


def generatePrimeNumbersList(n):
    primeNumbers = calculatePrimeNumberUnderN(n)
    primeNumbers.pop(0)
    print("end")
    return primeNumbers

def phi(n):
    result = 1
    if n == 1:
        return 1
    else:
        eachPrimeFacto = primeFactorization(n,generatePrimeNumbersList(n)).keys()
        for number in eachPrimeFacto:
            number = (1-(1/number))
            result *= number
        result *= n
    return int(result)


def getPrimeNumber(length=2048):
    primaryNumber = None
    while primaryNumber==None:
        # print("generate prime")
        numToTest = secrets.randbits(length)
        if (utils_old.miller_rabin(numToTest,40)):
            primaryNumber = numToTest
    return primaryNumber

def findGeneratorElement(p):
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

def getNumberWithGeneratorElement(length=2048):
    q = getPrimeNumber(length)
    p = q* 2 + 1
    while not(utils_old.rabin_miller(p,40)):
        q = getPrimeNumber(length)
        p = q* 2 + 1
    g = findGeneratorElement(p)
    return {"prime_number" : p, "generator_element" : g}
    

def getPrimeNumberUnderN(n):
    primeNumber = getPrimeNumber()
    if primeNumber < n :
        return primeNumber
    else:
        getPrimeNumberUnderN(n)

def write_to_file(data,filename):
    with open(filename,"w") as f:
        f.write(json.dumps(data))

if __name__ == "__main__":
    start_time = time.time()
    p_g = getNumberWithGeneratorElement()
    print(p_g)
    write_to_file(p_g,"2048bits.txt")
    end_time = time.time()

    print('Temps d\'exécution de la fonction :', end_time - start_time)
    



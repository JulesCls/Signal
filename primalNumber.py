import utils

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
    for i in range(3,n//2,2):
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
        utils.addIterationToDictionary(n,factorsList)
        return factorsList
    for i in primeNumbers:
        if n % i == 0:
            utils.addIterationToDictionary(i,factorsList)
            n //= i
            break
    primeFactorization(n,primeNumbers,factorsList)
    return factorsList


def generatePrimeNumbersList(n):
    primeNumbers = acceleratedPrimeNumbersGeneration(n)
    primeNumbers.pop(0)
    print("end")
    return primeNumbers

if __name__ == "__main__":
    x = 8_000_0089
    # print(generatePrimeNumbersList(x))
    
    print(primeFactorization(x,generatePrimeNumbersList(x)))



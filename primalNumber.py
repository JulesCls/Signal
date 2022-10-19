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
    numberToTest = 3
    while(numberToTest < n):
        for primeNumber in primeNumbers:
            if(numberToTest % primeNumber ) == 0:
                break
        else:
            primeNumbers.append(numberToTest)
        numberToTest+=1
    primeNumbers.insert(0,1)
    return(primeNumbers)

def primeFactorization(n, primeNumbers , factorsList = {}):
    if isPrime(n):
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
    primeNumbers = calculatePrimeNumberUnderN(n//2)
    primeNumbers.pop(0)
    return primeNumbers

if __name__ == "__main__":
    x = 7
    # print(generatePrimeNumbersList(x))
    print(primeFactorization(x,generatePrimeNumbersList(x)))



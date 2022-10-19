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

def primeFactorization(n, primeNumbers):
    tmp = []
    factoList = []
    if isPrime(n):
        return [n]
    else:
        for i in primeNumbers:
            r = n/i
            if r == n//i:
                tmp.append(i)
                n = r
                break
        tmp.append(primeFactorization(int(n),primeNumbers))
        for i in tmp:
            if isinstance(i, int):
                factoList.append(i)
            else:
                for j in i:
                    factoList.append(j)                
        return factoList

def generatePrimeNumbersList(n):
    primeNumbers = calculatePrimeNumberUnderN(n//2)
    primeNumbers.pop(0)
    return primeNumbers

# def phi(n):



if __name__ == "__main__":
    x = 1000000
    # print(generatePrimeNumbersList(x))
    print(primeFactorization(x,generatePrimeNumbersList(x)))



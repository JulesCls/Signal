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

def primeFactorization(n):
    primeNumbers =[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
    factoList = []
    if isPrime(n):
        return n
    else:
        for i in primeNumbers:
            r = n/i
            if r == n//i:
                factoList.append(i)
                n = r
                break
        factoList.append(primeFactorization(int(n)))
        return factoList
        
print(primeFactorization(345))
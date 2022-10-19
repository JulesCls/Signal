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

if __name__ == "__main__":
    x = 200
    print(f"Prime numbers under {x}:")
    print(calculatePrimeNumberUnderN(x))
    print(f"\nFirst {x} prime numbers:")
    print(calculateNFirstPrimeNumber(x))
    print(f"\nIs {x} Prime")
    print(isPrime(x))


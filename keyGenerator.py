import random
import euclide

def generateKeys():
     public = random.getrandbits(128)
     privateKeys = []
     while len(privateKeys) < 100:
         privateKey = random.getrandbits(128)
         if euclide.pgcdEuclide(public,privateKey) == 1:
             privateKeys.append(privateKey)
     print(privateKeys)
    
if __name__ == "__main__":
    generateKeys()
    
import euclide, secrets, prng 

def generatePublicKey():
    public = prng.xorshift()
    return public

def generatePrivateKeys(public):
     privateKeys = []
     while len(privateKeys) < 100:
        privateKey = prng.xorshift()
        if euclide.pgcdEuclide(public,privateKey) == 1:
             privateKeys.append(privateKey)
     return privateKeys

def definePrivateKey(privateKeys):
    rank = secrets.randbelow(len(privateKeys))
    print(rank)
    privateKey = privateKeys[rank]
    return privateKey

def testPgcdKeys(public, privateKeys):
    for i in privateKeys:
        if euclide.pgcdEuclide(public, i) != 1:
            return "Pas bon ta fonction"
    
if __name__ == "__main__":
    # for i in range(0,10000):
    #     print(f"Step: {i}")
    #     public = generatePublicKey()
    #     privateKeys = generatePrivateKeys(public)
    #     if testPgcdKeys(public, privateKeys) == "Pas bon ta fonction":
    #         break
    #     else:
    #         pass
    
    public = generatePublicKey()
    privateKeys = generatePrivateKeys(public)
    privateKey = definePrivateKey(privateKeys)
    print(privateKey)

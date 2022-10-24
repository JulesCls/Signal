import utils

def xorshift():
    seed = utils.generateRandomSplitInt(128,4)
    t = seed[3] ^ (seed[3] << 11)
    u = seed[0] ^ (seed[0] >> 8)
    O = u ^ (t ^ (t >> 19))
    O >>= 12
    output = []
    output.insert(0,O)
    for i in [0,1,2]:
        output.insert(i+1,seed[i])
    result = utils.concatenateInteger(output)
    return result

if __name__ == "__main__":
        print(xorshift())



    
import random

def miller_rabin(n, k):
    if n == 2:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

#imported from https://gist.github.com/Ayrx/5884790
   

if __name__ == "__main__":
    number = 67073
    # genEle = getGeneratorElement(number)
    # print("Elément générateur : ",  genEle)
    # eleList = []
    # for i in range(number-1):
    #     eleList.append(pow(genEle,i)%number)
    # eleList.sort()
    # print([*range(1,number)] == eleList)
    print(miller_rabin(140645969594959594934055696594939459696945969679749355696994340394959949330395967,32567980))


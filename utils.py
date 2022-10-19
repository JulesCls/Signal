def addIterationToDictionary(number,dictionary):
    if(number in dictionary):
        dictionary[number] +=1
    else:
        dictionary[number] = 1

if __name__ == "__main__":
    dic = {2 : 3, 1:1}
    addIterationToDictionary(2,dic)
    addIterationToDictionary(2,dic)
    addIterationToDictionary(4,dic)
    print(dic)
    
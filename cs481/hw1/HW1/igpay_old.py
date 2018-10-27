stringA = {'a', 'e', 'i', 'o', 'u'}

def tail(String, a, len):
    #print(a)
    #print(len)
    if a == len:
        String = String
    elif a > 1:
        String += 'ay'
    else:
        String += 'way'

    return String


def turnCase(inputString, resultstring):
    i = 0
    compileString = ""
    for y in inputString:
        if y<='z' and y>='a':
            compileString += resultstring[i].lower()
        else:
            compileString += resultstring[i].upper()
        i += 1

    while i < len(resultstring):
        if compileString[len(compileString)-1] <= 'z' and compileString[len(compileString)-1] >= 'a':
            i = i
            compileString += resultstring[i].lower()
        else:
            i = i
            compileString += resultstring[i].upper()
        i += 1

    return compileString

def igpay(inputString):
    resultstring = inputString
    resultstring = resultstring.lower()
    leftString = rightString = ""
    switch = False
    a = 0
    for x in resultstring:
        if(switch != True):
            for y in stringA:
                if y == x:
                    switch = True
                    break

            if switch == True:
                rightString += x
                a += 1
            else:
                leftString += x
                a += 1

        else:
            rightString += x

    resultstring = rightString + leftString
    resultstring = tail(resultstring, a, len(inputString))
    resultstring = turnCase(inputString, resultstring)
    return resultstring

#returnString = igpay(input())
#print("\n" + returnString)

if __name__ == "__main__":
    stringTest = ["yes", "parrot", "knights", "add", "office", "why", "STUFF"]
    print("\nPart 1 test sample :")
    for testWord in stringTest:
        returnString = igpay(testWord)
        print(testWord + " -> " + returnString)
    print("\n")
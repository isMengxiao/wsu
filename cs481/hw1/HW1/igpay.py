# -*- coding: utf-8 -*-
#!/usr/bin/env python3

stringt = {'a', 'e', 'i', 'o', 'u'}

def tail(astring, a, lens):
    if a == lens:
        astring = astring
    elif a > 1:
        astring += 'ay'
    else:
        astring += 'way'
    return astring

def turnCase(inputString, resultString):
    i = 0
    compileString = ""
    for y in inputString:
        if y <= 'z' and y >= 'a':
            compileString += resultString[i].lower()
        else:
            compileString += resultString[i].upper()
        i += 1

    while i < len(resultString):
        if compileString[len(compileString)-1] >= 'a':
            compileString += resultString[i].lower()
        else:
            compileString += resultString[i].upper()
        i += 1
    return compileString

def igpay(inputString):
    resultString = inputString.lower()
    leftString = rightString = ""
    switch = False
    a = 0
    for x in resultString:
        if(switch != True):
            for y in stringt:
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

    resultString = rightString+leftString
    resultString = tail(resultString, a, len(inputString))
    resultString = turnCase(inputString, resultString)
    return resultString

if __name__ == "__main__":
    stringTest = ["yes", "parrot", "knights", "add", "office", "why", "STUFF"]
    print("\nPart 1 test sample: ")
    for testWord in stringTest:
        returnString = igpay(testWord)
        print(testWord + " -> " + returnString)
    print("\n")






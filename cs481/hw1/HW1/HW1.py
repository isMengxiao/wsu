import sys
import igpay
##from igpay import igpay as newIgpay

def latinfy(word):
    return igpay.igpay(word)

def cutLine(line):
    FullString = word = ""
    for x in line:
        if x <= 'z' and x >= 'a':
            word += x
        elif x <= 'Z' and x >= 'A':
            word += x
        else:
            FullString += latinfy(word)
            FullString += x
            word = ""
    print(FullString)

def readFile(myfile):
    print("Open file : " + myfile)
    file = open(myfile, "r")

    while True:
        line = file.readline()
        #print(line)
        if len(line) == 0:
            break
        else:
            cutLine(line)

    file.close()

if __name__ == '__main__':
    #fileName = sys.argv[1]
    fileName = "test.txt"
    readFile(fileName)

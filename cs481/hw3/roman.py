#!/usr/bin/env python3
# -*- coding: utf-8 -*-


##RomanStr = ['I', 'V', 'X', 'L', 'C', 'D', 'M',
 ##           '(V)', '(X)', '(L)', '(C)', '(D)', '(M)']
RomanStrA = [
    'I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX',
    'X', 'XX', 'XXX', 'XL', 'L', 'LX', 'LXX', 'LXXX', 'XC',
    'C', 'CC', 'CCC', 'CD', 'D', 'DC', 'DCC', 'DCCC', 'CM',
    'M', 'MM', 'MMM', '(IV)', '(V)', '(VI)', '(VII)', '(VIII)', '(IX)',
    '(X)', '(XX)', '(XXX)', '(XL)', '(L)', '(LX)', '(LXX)', '(LXXX)', '(XC)',
    '(C)', '(CC)', '(CCC)', '(CD)', '(D)', '(DC)', '(DCC)', '(DCCC)', '(CM)',
    '(M)']

class Roman(int):
    def __init__(self, num):
        self.Rnum = self.NtoR(num)
        self.num = num

    @staticmethod
    def NtoR(num):
        if num > 2000000:
            raise ValueError
        string = ''
        nCC =  num // 1000000
        nXX = (num % 1000000) // 100000
        nM  = (num % 100000 ) // 10000
        nC  = (num % 10000)   // 1000
        nX  = (num % 1000)    // 100
        nI  = (num % 100)     // 10
        n   =  num % 10
        if num == 0:
            return 'N'
        if nCC:
            nCC = '(M)'
            string += nCC
        if nXX:
            nXX += 44
            string += str(RomanStrA[nXX])
        if nM:
            nM += 35
            string += str(RomanStrA[nM])
        if nC:
            nC += 26
            string += str(RomanStrA[nC])
        if nX:
            nX += 17
            string += str(RomanStrA[nX])
        if nI:
            nI += 8
            string += str(RomanStrA[nI])
        if n:
            n -= 1
            string += str(RomanStrA[n])
        #if ~num:
        #    string += 'N'
        return string

    def __str__(self,):
        return str(self.Rnum)
    def __repr__(self):
        return "Roman("+str(self.num)+")"


    ##start rebuild +-*/
    ##+++++++++++++++++++++++++++++++++++++++
    def __add__(self, other):
        if type(other) == Roman:
            return Roman(self.num + other.num)
        elif type(other) == int:
            return Roman(self.number + other)
        else:
            print('Wrong type')
            return 0
    def __radd__(self, other):
        return Roman.__add__(self, other)

    ##---------------------------------------
    def __sub__(self, other):
        if type(other) == Roman:
            return Roman(self.num - other.num)
        elif type(other) == int:
            return Roman(self.num - other)
        else:
            print('Wrong type')
            return 0
    def __rsub__(self, other):
        if type(other) == Roman:
            return Roman(other.num - self.num)
        elif type(other) == int:
            return Roman(other - self.num)
        else:
            print('Wrong type')
            return 0

    #****************************************
    def __mul__(self, other):
        if type(other) == Roman:
            return Roman(self.num * other.num)
        elif type(other) == int:
            return Roman(self.num * other)
        else:
            print('Wrong type')
            return 0
    def __rmul__(self, other):
        return Roman.__mul__(self, other)

    ##///////////////////////////////////////
    def __floordiv__(self, other):
        if type(other) == Roman:
            return Roman(self.num // other.num)
        elif type(other) == int:
            return Roman(self.num // other)
        else:
            print('Wrong type')
            return 0
    def __rfloordiv__(self, other):
        if type(other) == Roman:
            return Roman(other.num // self.num)
        elif type(other) == int:
            return Roman(other // self.num)
        else:
            print('Wrong type')
            return 0
    def __truediv__(self, other):
        if type(other) == Roman:
            return (Roman(self.num // other.num),
                    Roman(self.num % other.num))
        elif type(other) == int:
            return (Roman(self.num // other),
                    Roman(self.num % other))
        else:
            print('Wrong type')
            return 0
    def __rtruediv__(self, other):
        if type(other) == Roman:
            return (Roman(other.num // self.num),
                    Roman(other.num % self.num))
        elif type(other) == int:
            return (Roman(other // self.num),
                    Roman(self.num % other))
        else:
            print('Wrong type')
            return 0

    #pow
    def __pow__(self, other):
        if type(other) == Roman:
            return (Roman(self.num ** other.num))
        elif type(other) == int:
            return (Roman(self.num ** other))
        else:
            print('Wrong type')
            return 0
    def __rtruediv__(self, other):
        if type(other) == Roman:
            return (Roman(other.num ** self.num))
        elif type(other) == int:
            return (Roman(other ** self.num))
        else:
            print('Wrong type')
            return 0


    ##>>>>>>>>>>>>>>>>>==============<<<<<<<<<<<<<
    def __re__(self, other):
        if type(other) == Roman:
            return self.num == other.num
        elif type(other) == int:
            return self.num == other
        else:
            print('Wrong type')
            return 0
    def __ne__(self, other):
        if type(other) == Roman:
            return self.num != other.num
        elif type(other) == int:
            return self.num != other
        else:
            print('Wrong type')

    def __gt__(self, other):
        if type(other) == Roman:
            return self.num > other.num
        elif type(other) == int:
            return self.num > other
        else:
            print('Wrong type')
    def __lt__(self, other):
        if type(other) == Roman:
            return self.num < other.num
        elif type(other) == int:
            return self.num < other
        else:
            print('Wrong type')

    def __ge__(self, other):
        if type(other) == Roman:
            return self.num >= other.num
        elif type(other) == int:
            return self.num >= other
        else:
            print('Wrong type')
    def __le__(self, other):
        if type(other) == Roman:
            return self.num <= other.num
        elif type(other) == int:
            return self.num <= other
        else:
            print('Wrong type')

    def __neg__(self):
        return -self.num

for i in range(1, 1000):
    #globals()[i] = Roman.NtoR(i)
    globals()[Roman.NtoR(i)] = Roman(i)
    globals()['N'] = Roman(0)
    globals()['M'] = Roman(1000)

"""if __name__ == "__main__":
   III = Roman(3)
    VII = Roman(7)
    print(type(III))
    print(type(VII))
    print(III+VII)
"""







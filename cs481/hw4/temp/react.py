# -*- coding: utf-8 -*-
#! /usr/bin/env python3
global em, ep, p, n, nu_e, gamma

class Nucleus:
    def __init__(self, sym, chg, massnumber):
        self.sym = sym
        self.chg = chg
        self.num = massnumber
    def __str__(self):
        return self.sym
    def __add__(self, *other):
        result = (self,)
        if type(other) == tuple:
            result += other
        else:
            result += (other,)
        return result
    def __radd__(self, *other):
        result = (self,)
        if type(other) == tuple:
            result += other[0]
        else:
            result += (other,)
        return result

    def __mul__(self, other):
        result = (self,)
        other -= 1
        for i in range(other):
            result += (self,)
        return result

    def __rmul__(self, other):
        return Nucleus.__mul__(self, other)





class Reaction:
    def __init__(self, left, right):
        self.left = []
        self.right = []
        if type(left) == tuple:
            for item in left:
                self.left.append(item)
        else:
            self.left.append(left)
        if type(right) == tuple:
            for item in right:
                self.right.append(item)
        else:
            self.right.append(right)
        self.check()

    def check(self):
        lchg = 0
        lnum = 0
        rchg = 0
        rnum = 0
        for item in self.left:
            lchg += item.chg
            lnum += item.num
        for item in self.right:
            rchg += item.chg
            rnum += item.num
        if lchg == rchg:
            #print('Charge equal')
            pass
        else:
            raise UnbalancedCharge(abs(lchg-rchg))
            #pass
        if lnum == rnum:
            #print('Number equal')
            pass
        else:
            raise UnbalancedNumber(abs(lnum-rnum))
            #pass

    def action(self):
        left = []
        right = []
        strs = ''
        #######################
        for item in self.left:
            if item.num > 1:
                strs = '(%d)%s'%(item.num, item.sym)
            else:
                strs = '%s'%item.sym
            left.append(strs)
        #######################
        for item in self.right:
            if item.num > 1:
                strs = '(%d)%s'%(item.num, item.sym)
            else:
                strs = '%s'%item.sym
            right.append(strs)
        ####################
        return (left, right)

    def __str__(self):
        left, right = self.action()
        result = self.transfer(left, right)
        return result

    def transfer(self, left, right):
        leftset = set()
        rightset = set()
        result = ''
        for i in left:
            if left.count(i) > 1:
                leftset.add(str(left.count(i))+i)
            else:
                leftset.add(str(i))
        result = ' + '.join(leftset)
        result += ' -> '
        for i in right:
            if right.count(i) > 1:
                rightset.add(str(right.count(i))+i)
            else:
                rightset.add(str(i))
        result += ' + '.join(rightset)
        return result


class ChainReaction(Reaction):
    def __init__(self, name):
        self.name = name
        self.actions = []

    def addReaction(self, reaction):
        self.actions.append(reaction)

    def network(self):
        left = []
        right = []
        for i in self.actions:
            left += i.action()[0]
            right+= i.action()[1]
        for i in left:
            if (i in right):
                left.remove(i)
                right.remove(i)

        for i in left:
            if i == ' + ':
                left.remove(i)
        for i in right:
            if i == ' + ':
                right.remove(i)
        return self.transfer(left, right)

    def __str__(self):
        print(self.name, ':')
        for i in self.actions:
            print(i)
        print('net:')
        return self.network()

class UnbalancedCharge(Exception):
    def __init__(self, diff):
        self.diff = diff
class UnbalancedNumber(Exception):
    def __init__(self, diff):
        self.diff = diff
em   = Nucleus("e-", -1, 0)
ep   = Nucleus("e+",  1, 0)
p    = Nucleus("p",   1, 1)
n    = Nucleus("n",   0, 1)
nu_e = Nucleus("nu_e",0, 0)
gamma= Nucleus("gamma", 0, 0)
he3  = Nucleus('He', 2, 3)
he4  = Nucleus('He', 2, 4)
li6  = Nucleus('li', 3, 6)
d    = Nucleus('H',  1, 2)

if __name__ == '__main__':
    try:
        print(2*d)
        print(d+he3+li6)
        print(Reaction(he3+d, he4+li6))
        chnpp = ChainReaction("proton branch")
        for r in (Reaction((d,d,d,d), (he3, he4, n)),
                  Reaction(he3+d+li6+ep, he3+he4+n+3*p),
                  Reaction((li6, d, d), (he3,he3, d, n,n))):
            chnpp.addReaction(r)
        print(chnpp)
    except UnbalancedCharge as e:
        pass
    except UnbalancedNumber as e:
        pass
    # print(Reaction((li6, d), (he4, he4, d)))

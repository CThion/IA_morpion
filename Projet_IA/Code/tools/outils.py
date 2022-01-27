#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Sized
import functools
try:
    from ezCLI import testcode
except:
    try:
        from tools.ezCLI import testcode
    except:
        print("missing ezCLI and tools.ezCLI")
        

def count(func):
    """ count the recursive calls """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.tick += 1
        return func(*args, **kwargs)

    wrapper.tick = 0
    return wrapper

def p2c(pos:int, nc:int) -> tuple:
    """ provides a 2D value from a 1D value """
    return pos//nc, pos%nc

def c2p(coord:Sized, nc:int) -> int:
    """ provides a 1D value from a 2D value """
    return coord[0]*nc+coord[1]

#======================== chaine ==============================#
#================ usefull for morpion and alike ===============#
#==============================================================#

def lines(state:str, nbl:int, nbc:int) -> list:
    """ get the all the lines """
    return [ state[i*nbc:(i+1)*nbc] for i in range(nbl) ]
def columns(state:str, nbl:int, nbc:int) -> list:
    """ get the all the columns """
    return [ state[i::nbc] for i in range(nbc) ]
def diag_plus(state:str, nbl:int, nbc:int, tore:bool) -> list:
    """ get all the diagonals right to left
        if tore is True, all diags have same length
        else size of substrings increase """
    return [ ''.join([state[i*nbc+j]
                      for i in range(nbl)
                      for j in range(nbc)
                      if ((i+j)%nbc == k if tore else (i+j) == k)])
             for k in range(nbc) ]
def diag_moins(state:str, nbl:int, nbc:int, tore:bool) -> list:
    """ get all the diagonals left to right
        if tore is True, all diags have same length
        else size of substrings decrease """
    return [ ''.join([state[i*nbc+j]
                      for i in range(nbl)
                      for j in range(nbc)
                      if ((i-j)%nbc == k if tore else (i-j) == k)])
             for k in range(nbc) ]

def test_dim():
    code = '''
c = (3,4)
col = 5
print("test1: p2c(c2p) = Id",end=' ')
print("... {}".format(p2c(c2p(c, col), col) == c))


p = 42
print("test2: c2p(p2c) = Id", end=' ')
print("... {}".format(c2p(p2c(p, col), col) == p))
''' ; testcode(code)

def test_str():
    code = '''
_ = "."*7
_t = _
_t +=  "....XO."
_t += ".....XO"
_t += "......X"
_t += "XO....."
_t += ".XO...."
_t += _
print(len(_t), _t.count('X'), _t.count('O'), _t.count('.'))

_s =  "....XO."
_s += "...XO.."
_s += _ * 2
_s += "X"+"."*6
_s += ".....OX"
_s += "....OX."
print(len(_s), _s.count('X'), _s.count('O'), _s.count('.'))

lines(_t, 7, 7)
lines(_s, 7, 7)

columns(_t, 7, 7)
columns(_s, 7, 7)

diag_plus(_t, 7, 7, False)
diag_plus(_t, 7, 7, True)

diag_plus(_s, 7, 7, False)
diag_plus(_s, 7, 7, True)

diag_moins(_t, 7, 7, False)
diag_moins(_t, 7, 7, True)

diag_moins(_s, 7, 7, False)
diag_moins(_s, 7, 7, True)
''' ; testcode(code)
    
if __name__ == '__main__':
    test_dim()
    test_str()

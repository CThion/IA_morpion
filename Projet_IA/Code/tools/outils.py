#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Sized
import functools
try:
    from ezCLI import testcode, grid
except:
    try:
        from tools.ezCLI import testcode, grid
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

def get_index(i:int, j:int, nbl:int, nbc:int, tore:bool) -> list:
    """ given i: type (line, column, diag+, diag-
        given j: the position
        return the index involved
    """
    if i == 0: # line
        return [k for k in range(j*nbc, (j+1)*nbc)]
    if i == 1: # column
        return [k for k in range(j,nbl*nbc,nbc)]
    if i == 2: # diag_plus
        return [a*nbc+b for a in range(nbl) for b in range(nbc)
                if ((a+b)%nbc == j if tore else (a+b) == j)]
    return [a*nbc+b for a in range(nbl) for b in range(nbc)
                if ((a-b)%nbc == j if tore else (a-b) == j)]

def intersection(state:str, pawn:str, candidates:list,
                 nbl:int, nbc:int, tore:bool) -> set:
    """ check that there is one common point """
    _ = [set() for x in candidates]
    for a,(i,j) in enumerate(candidates):
        substring = get_index(i, j, nbl, nbc, tore)
        for p in substring:
                if state[p] == pawn: _[a].add(p)
    return set.intersection(*_)

def longuest_chain(string:str, tore:bool, pawn:str) -> list:
    """ return list of contiguous positions """
    _sz1 = len(string)
    _ = [i for i in range(_sz1) if string[i] == pawn]
    _sz = len(_)
    _bag = []
    for p,x in enumerate(_):
        j = 1 ; _ok = True
        while j < _sz and _ok:
            if tore :
                if (_[(p+j)%_sz] != (x+j)%_sz1):
                    _ok = False
                else:
                    j += 1
            elif p+j < _sz:
                if (_[p+j] != x+j):
                    _ok = False
                else:
                    j += 1
            else:
                _ok = False
                
        _bag.append( j)
    return _bag


def display_grid(state:str, pawns:str, nbl:int):
    """ basic display from a string, usefull for debug """
    board = [ [pawns[0] for _ in range(nbl)] for _ in range(nbl) ]
    count = [0,0,0]
    for i,x in enumerate(state):
        a,b = p2c(i, nbl)
        j = pawns.index(x)
        count[j] += 1
        board[a][b] = x
    print(grid(board, size=3))
    print("count {}".format(count))

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

def test_chain():
    code = '''
s = "OOXOO"
longuest_chain(s, False, 'O')
longuest_chain(s, True, 'O')

t = "XXXOX"
longuest_chain(t, False, 'X')
longuest_chain(t, True, 'X')
''' ; testcode(code)

if __name__ == '__main__':
    test_chain()

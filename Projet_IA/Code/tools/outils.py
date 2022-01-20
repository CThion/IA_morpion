#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import Sized
import functools

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

if __name__ == '__main__':
    c = (3,4)
    col = 5
    print("test1: p2c(c2p) = Id",end=' ')
    print("... {}".format(p2c(c2p(c, col), col) == c))


    p = 42
    print("test2: c2p(p2c) = Id", end=' ')
    print("... {}".format(c2p(p2c(p, col), col) == p))

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players of players_mc
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random
import math
from tools.outils import count
import time

def scoring(win:int, loss:int, draw:int) -> float:
    """ 
        from counters win/loss/draw makes some metrics
        return a value in [-1, 1] 
    """
    _sum = win + loss + draw
    if _sum == 0: return 0
    _upper = win + .5 * draw - loss
    _ratio = _upper / _sum
    return _ratio 

#=========== les classes à mettre en oeuvre pour le jalon 03 ===========#

#====================== exemples de code test ==========================#
def usage():
    print("""
> test_clever(cls)
  prend en paramètre une classe n'ayant besoin que de pf
> test_morpion(cls)
  prend en paramètre une classe ayant besoin de pf ou nbSim
  prend en paramètre une classe ayant besoin de pf et secondes
> test_hexapawn(cls)
  prend en paramètre une classe ayant besoin de pf ou nbSim
  prend en paramètre une classe ayant besoin de pf et secondes
""")
    
def test_clever(joueur):
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
jeu.state == (13, 0) # on attend True au test

joueur.decision.memory = {}
moi = joueur('toto', jeu, pf=3)
moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 3 # on attend True au test
moi.game.state == (3, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 2 # on attend True au test
moi.game.state == (6, 4) # on attend True au test

jeu2 = Matches(13, False) # le but ne pas prendre la dernière allumette
joueur.decision.memory = {}
moi = joueur('toto', jeu2, pf=3)
moi.who_am_i = jeu2.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 2# on attend True au test
moi.game.state == (3, 4)  # on attend True au test

moi.decision( (4, 4) ) == 3 # on attend True au test
moi.game.state == (4, 4) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 1 # on attend True au test
moi.game.state == (6, 4) # on attend True au test

from divide_left import Divide
jeu3 = Divide(7, 17)
joueur.decision.memory = {}
moi = joueur('malin', jeu3, pf=3)
moi.who_am_i = jeu3.turn # moi est le premier joueur
moi.decision( ((3,4), 4) ) == ('A', 1)
moi.game.state == ((3,4), 4)
''' ; testcode(code)
    
def  test_morpion(joueur):
    code = '''
from morpion import Morpion
klass = 'IterativeDeepening' == joueur.__name__
kargs = {'pf':43, 'secondes':2.} if klass else {'pf':3, 'nbSim': 100}
jeu = Morpion(phase=2) 
_state = "X...O..OX", 4
jeu.state = _state
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.perf_counter()
print(a.decision(_state))
_end = time.perf_counter() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)

jeu = Morpion(5)
_attack = '.'*5+"..XO."*3+'.'*5, 6
_defence = "X..O."+"."*5+"..XO."*2+'.'*5, 6

jeu.state = _attack
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.perf_counter()
print(a.decision(_attack))
_end = time.perf_counter() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_attack[0], None)

jeu.state = _defence
print(jeu)

joueur.decision.memory = {}
_start = time.perf_counter()
print(a.decision(_defence))
_end = time.perf_counter() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_defence[0], None)
''' ; testcode(code)

def  test_hexapawn(joueur):
    code = '''
from hexapawn import Hexapawn
klass = 'IterativeDeepening' == joueur.__name__
kargs = {'pf':43, 'secondes':2} if klass else {'pf':3, 'nbSim': 100}
jeu = Hexapawn()
_state = "X.."+"O.X"+".O.",4

jeu.state = _state
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.perf_counter()
print(a.decision(_state))
_end = time.perf_counter() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)

jeu = Hexapawn(4,3)
_state = "X.X.X.O...OO", 2
jeu.state = _state
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.perf_counter()
print(a.decision(_state))
_end = time.perf_counter() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)
''' ; testcode(code)

if __name__ == "__main__":
    usage()

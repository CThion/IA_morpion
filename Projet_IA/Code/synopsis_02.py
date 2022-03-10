#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random

#=========== les classes à mettre en oeuvre pour le jalon 02 ===========#

#====================== exemples de code test ==========================#
def test_decision(joueur):
    """ joueur est une classe telle que Human, Randy, MinMax """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
print(jeu) # on attend 13 allumettes

moi = joueur('toto', jeu, pf=3)
moi.decision( (3, 4) ) is None # on attend True au test
moi.game.state == (3,4) # on attend True
jeu.state == (13,0) # on attend True

moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (7, 3) ) is None # on attend True au test
moi.game.state == (7,3) # on attend 7 allumettes
jeu.state == (13,0) # on attend True

moi.decision( (7, 4) ) in (1, 2, 3) # on attend True au test
moi.game.state == (7, 4)  # on attend True au test
jeu.state == (13,0) # on attend True

from divide_left import Divide
jeu = Divide(7, 17) # le but partager les jetons en 2
print(jeu)

moi = joueur('boxer', jeu, pf=3)
moi.decision( ((3, 4), 1) ) is None # on attend True au test
moi.game.state == ((3,4), 1) # on attend True
jeu.state == ((7,17), 0) # on attend True

moi.who_am_i = jeu.opponent # moi est le second joueur
moi.decision( ((7, 3), 4) ) is None # on attend True au test
moi.game.state == ((3,7), 4) # on attend True
jeu.state == ((7,17), 0) # on attend True

moi.decision( ((7, 4), 3)) in (('A',1),('A',2),('A',3),('B',1),('B',2)) # on attend True au test
moi.game.state == ((4, 7), 3)  # on attend True au test
jeu.state == ((7,17), 0) # on attend True
''' ; testcode(code)

def test_clever(joueur):
    """ on attend que joueur soit MinMax Negamax AlphaBeta Neg_AlphaBeta """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
jeu.state == (13, 0) # on attend True au test

moi = joueur('toto', jeu, pf=3)
moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 3 # on attend True au test
moi.game.state == (3, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

moi.decision( (6, 4) ) == 2 # on attend True au test
moi.game.state == (6, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

jeu2 = Matches(13, False) # le but ne pas prendre la dernière allumette
moi = joueur('toto', jeu2, pf=3)
moi.who_am_i = jeu2.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 2# on attend True au test
moi.game.state == (3, 4)  # on attend True au test
jeu2.state == (13, 0) # on attend True au test

moi.decision( (4, 4) ) == 3 # on attend True au test
moi.game.state == (4, 4) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 1 # on attend True au test
moi.game.state == (6, 4) # on attend True au test

from divide_left import Divide
jeu3 = Divide(7, 17)
moi = joueur('malin', jeu3, pf=3)
moi.who_am_i = jeu3.turn # moi est le premier joueur
moi.decision( ((3,4), 4) ) == ('A', 1)
moi.game.state == ((3,4), 4)
''' ; testcode(code)
    

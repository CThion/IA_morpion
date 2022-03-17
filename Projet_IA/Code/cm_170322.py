#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Illustration du cours
from allumettes import Matches # choix du jeu
jeu = Matches(13, True) # prendre la derniere allumettes
from sol_j02 import Human # choix d'un joueur
# (sans importance, on prend les plus simples Human ou Randy)

moi = Human('mmc', jeu)
moi.who_am_i = jeu.turn # le premier à jouer

compteur = moi.simulation(100) # on fait 100 simulations
# dans les allumettes il n'y a pas de match nul possible
print(moi.game)
print(">> nb de victoires, defaites et nuls",compteur) # victoire, defaite, nul

from synopsis_03 import scoring # la fonction qui à partir de compteurs
# donne une valeur entre -1 et +1
# 2 ecritures possibles
print('>> scoring(compteur[0], compteur[1], compteur[2]) =',
      scoring(compteur[0], compteur[1], compteur[2]))
print('>> scoring(*compteur) =',
      scoring(*compteur)) # on laisse python faire l'énumération des paramètres

# comment choisir l'action la plus prometteuse
# pour chaque action, jouer, simuler, dejouer
L = []
for a in moi.game.actions:
    moi.game.move(a)
    L.append( moi.simulation(1000) )
    moi.game.undo()

print(">> liste des compteurs pour chaque action possible\n", L)

# On calcule l'utilité
Esperance = [ scoring(*cpt) for cpt in L ]
print("Espérance de gain", Esperance)
pos = Esperance.index(max(Esperance))
print("choix de l'action ayant plus grande espérance",
      "pos {}, action {}".format(pos, moi.game.actions[pos]))

input('jeu du morpion')
#============================= Morpion ===============================#
# Autre jeu meme code
from morpion import Morpion
jeu = Morpion(5)
moi = Human('mmc', jeu)
moi.who_am_i = jeu.turn # le premier à jouer

compteur = moi.simulation(100) # on fait 100 simulations
# dans le morpion match nul possible
print(moi.game)
print(">> nb de victoires, defaites et nuls",compteur) # victoire, defaite, nul

print('>> scoring(*compteur) =',
      scoring(*compteur)) # on laisse python faire l'énumération des paramètres

# comment choisir l'action la plus prometteuse
# pour chaque action, jouer, simuler, dejouer
L = []
for a in moi.game.actions:
    moi.game.move(a)
    L.append( moi.simulation(100) )
    moi.game.undo()

print(">> liste des compteurs pour chaque action possible\n", L)

# On calcule l'utilité
Esperance = [ scoring(*cpt) for cpt in L ]
print("Espérance de gain", Esperance)
pos = Esperance.index(max(Esperance))
print("choix de l'action ayant plus grande espérance",
      "pos {}, action {}".format(pos, moi.game.actions[pos]))

input("UCB")
#---------------------- UCB ---------------------------------#
# au lieu de répartir équitablement les simulations, on choisit
# à chaque tour quelle est l'action ayant le meilleur potentiel
#============================================================#
from math import sqrt, log
L = []

for a in moi.game.actions:
    moi.game.move(a)
    L.append( moi.simulation(1) )
    moi.game.undo()

_nbMax = len(moi.game.actions) * 100
_nsims = [ sum(cpt) for cpt in L ] # normalement 1 pour tous
nbS = sum(_nsims)

while nbS < _nbMax:
    # calcul utilité
    _utilite = [ scoring(*cpt) for cpt in L ]
    # calcul formul UCB avec C = 1
    _ucb = [ u+sqrt(log(nbS)/_nsims[i]) for i,u in enumerate(_utilite) ]

    pos = _ucb.index(max(_ucb)) # où est le plus gros score
    choix = moi.game.actions[ pos ] # quelle est l'action
    # print('choix', choix)

    # nouvelle simulation 
    moi.game.move(choix)
    cpt = moi.simulation(1)
    moi.game.undo()
    nbS += 1
    _nsims[pos] += 1
    L[pos] = [ x+y for x,y in zip(L[pos], cpt) ]
    


print("répartition", _nsims)
print("nb total de simulation", nbS)
# calcul utilité
_utilite = [ scoring(*cpt) for cpt in L ]
# calcul formul UCB avec C = 1
_ucb = [ u+sqrt(log(nbS)/_nsims[i]) for i,u in enumerate(_utilite) ]

p = _ucb.index(max(_ucb))
q = _utilite.index(max(_utilite))

print("meilleure action avec UCB {}, avec Utilite {}".format(p,q))
print("UCB {} vs Utilite {}".format(moi.game.actions[p],
                                    moi.game.actions[q]))



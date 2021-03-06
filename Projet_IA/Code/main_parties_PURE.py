#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
from classes.abstract_player import Player
from classes.abstract_game import Game
from tools.checkTools import check_property
from typing import Sized

try:
    from players import * # les joueurs du Jalon 02
except Exception as _e:
    print("Missing players Jalon02")

try:
    from players_mc import * # les joueurs du Jalon 03
except Exception as _e:
    print("Missing players Jalon03")
    
# initialisation
if len(sys.argv) == 1:
    param = "morpion" # input("quel est le fichier de description du jeu ? ")
    if not os.path.isfile(param): ValueError("need a python file")
else: param = sys.argv[1]

target = param.split('.')[0]

_out = check_property(target != '','acces au fichier')
print("tentative de lecture de {}".format(target))
try:
    jeu = __import__(target) # revient à faire import XXX as jeu
    assert hasattr(jeu, 'Game')
except Exception as _e:
    print(_e)
    sys.exit(-1)


class Statistics:
    """ collect information about victories """
    def __init__(self, p1:str, p2:str, g:Game):
        """
        p1 the name of 1st player
        p2 the name of 2nd player
        g a game subclass of Game
        """
        g.reset() # to be sure the names are fine
        self.__game = repr(g)
        self.__colors = (g.turn, g.opponent)
        self.__names = p1, p2
        self.__keys = "pv moves avg_victories avg_moves".split()
        self.__labels = {self.__keys[i+2]: self.__keys[i]
                         for i in range(2)}
        self.__data = {k:
                       {ident:0 for ident in (p1, p2, g.turn, g.opponent)}
                       for k in self.__keys}
        self.reset()

    def reset(self):
        """ restart data """
        for k in self.__data:
            for q in self.__data[k]: self.__data[k][q] = 0
        self.__count = 0
        self.__built = False

    @property
    def keys(self): return tuple(self.__keys)
    @property
    def subkeys(self): return tuple(self.__data['pv'].keys())
        
    def __repr__(self):
        return "{0}({1}, {2}, {3})".format(self.__class__.__name__,
                             *self.__names, self.__game)
                                             
    def add_result(self, values:Sized, names:Sized):
        """ update pv and moves information 
            requires pv, moves in self.__keys
        """

        if len(values) != 2 or len(names) != 2:
            raise ValueError("Rubish data")
        if names[0] not in self.subkeys:
            raise ValueError("wrong information {}".format(names[0]))
        if names[1] not in self.subkeys:
            raise ValueError("wrong information {}".format(names[1]))
        self.__count += 1 ; self.__built = False
        
        if values[0] == 0: # win red
            self.__data['pv'][self.__colors[1]] += 1
            self.__data['pv'][names[1]] += 1
            
        elif values[1] == 0: # win yellow
            self.__data['pv'][self.__colors[0]] += 1
            self.__data['pv'][names[0]] += 1
        else: # draw
            for i in range(2):
                self.__data['pv'][self.__colors[i]] += 1
                self.__data['pv'][names[i]] += 1
        for i in range(2):
            self.__data['moves'][self.__colors[i]] += values[i]
            self.__data['moves'][names[i]] += values[i]
            
    def __build_avg(self):
        """ helper to build avg points 
            requires self.__count > 0
        """
        if self.__built: return
        for q in self.__labels:
            _vkey = self.__labels[q]
            for k in self.__data[q]:
                self.__data[q][k] = round(self.__data[_vkey][k]/self.__count,
                                          2)
        self.__built = True


    @property
    def statistics(self):
        if self.__count != 0: self.__build_avg()
        return self.__data.copy()
        
    def main_statistic(self, key=None) -> dict:
        """ provides main statistics """
        if self.__count != 0: self.__build_avg()
        if key is None or key not in self.keys:
            return self.__data.copy()
        return self.__data[key].copy()

    def specific_statistic(self, subkey:str) -> dict:
        """ provides statistic for a specific key """
        if self.__count != 0: self.__build_avg()
        if subkey not in self.subkeys:
            print("subkey expected belongs to {}".format(self.subkeys))
            return {}
        return {key: self.__data[key][subkey]
            for key in self.keys}

def manche(yellow:Player, red:Player, g:Game) -> tuple:
    """
    requires 2 different players and a Game
    requires j.game to be similar to g
    """
    g.reset() # new start
    print(g)
    yellow.who_am_i = g.turn
    red.who_am_i = g.opponent

    while not g.over():
        if g.timer % 2 == 0:
            x = yellow.decision(g.state)
        else:
            x = red.decision(g.state)
        g.move(x)

    print("final Game\n{}".format(g))
    print("waiting ...", end='')
    time.sleep(.5)
    print(" Done")

    if g.winner is None: # a draw
        return (g.timer/2, g.timer/2)
    else:
        _ = [0, 0]
        if isinstance(g.winner, int): _[g.winner] = g.timer
        else:
            _who = 0 if yellow.who_am_i == g.winner else 1
            _[_who] = g.timer
        return tuple(_)

def partie(yellow:Player, red:Player,
           g:Game, nbParties:int=1) -> Statistics:
    """ given 2 players,  a board and a number N
        runs 2*N manches and return Statistics
    """
    nbManches = 2 if nbParties <= 1 else 2*nbParties
    if yellow == red:
        _red = red.clone()
    else:
        _red = red
    stat = Statistics(yellow.name, _red.name, g)
    for i in range(nbManches):
        if i%2 == 0:
            _ = manche(yellow, _red, g)
            stat.add_result(_,(yellow.name, _red.name))
        else:
            _ = manche(_red, yellow, g)
            stat.add_result(_,(_red.name, yellow.name))
    return stat

            
def usage() -> str:
    return """
Vous devez créer un 'Game', par exemple
>>> g = jeu.Hexapawn(4, 5, cylindre=True, priorite=True)
ou
>>> g = jeu.Morpion(5, tore=True)

Vous devez créer 2 joueurs, par exemple
>>> alea = Randy('alea', g)
>>> moi = Human('mmc', g)

Vous pouvez maintenant opposer les 2 joueurs pour une manche
>>> s = manche(alea, moi, g)

Qui opposera 'alea' à 'mmc', le résultat sera le
nombre de points de chaque joueur à la fin de la partie

Vous pouvez aussi opposer les 2 joueurs pour plusieurs manches
à chaque manche le premier à jouer change
>>> partie(alea, moi, b, 1)

Il y aura 2 manches alea-mmc, le résultat sera une statistique
(nombre de victoires pour 'J', nombre de victoire pour 'R',
 nombre de victoires pour alea, nombre de victoires pour mmc,
 points totaux obtenus pour 'J', points totaux obtenus pour 'R',
 points totaux obtenus pour alea, points totaux obtenus pour mmc,
 points moyens obtenus pour 'J', points moyens obtenus pour 'R',
 points moyens obtenus pour alea, points moyens obtenus pour mmc)

>>> s = partie(....)
>>> s.statistics # all information
>>> s.main_statistic(key) # key in pv / sigma / avg_victories / avg_stones
>>> s.specific_statistic(key) # key in players names 

>>> test_matches() # joueur Randy vs MinMax
>>> test_heaxapawn() # joueur Randy vs MinMax
>>> test_morpion() # joueur Randy vs MinMax
"""

def test_matches():
    from tools.ezCLI import testcode
    from allumettes import Matches as m
    code = '''
from mes_players import Randy, MinMax
game = m(13, False)
print(game)

a = Randy('alea', game)
a.who_am_i = game.opponent
_s = 5, 4
game.valid_state(_s)

b = MinMax(2, game, pf=5)
b.who_am_i = game.turn
print(game)
b.decision(_s)
print(game)

stat = partie(b, a, game, 1)
stat.statistics

game = m(13, True)
print(game)

a = Randy('alea', game)
a.who_am_i = game.opponent
_s = 5, 4
game.valid_state(_s)

b = MinMax(2, game, pf=5)
b.who_am_i = game.turn
print(game)
b.decision(_s)
print(game)

stat = partie(b, a, game, 1)
stat.statistics
''' ; testcode(code)

def test_morpion():
    from tools.ezCLI import testcode
    from morpion import Morpion as m
    code = '''
from mes_players import Randy, MinMax
morpion = m()
a = Randy('alea', morpion)
a.who_am_i = morpion.opponent
_s = "X...O..OX", 4
morpion.valid_state(_s)
b = MinMax(2, morpion, pf=5)
b.who_am_i = morpion.turn
print(morpion)
b.decision(_s)
print(morpion)
stat = partie(b, a, morpion, 1)
stat.statistics
''' ; testcode(code)
    
def test_hexapawn():
    from tools.ezCLI import testcode
    from hexapawn import Hexapawn as m
    code = '''
from mes_players import Randy, MinMax
hexapawn = m()
a = Randy('alea', hexapawn)
a.who_am_i = hexapawn.opponent
_s = "X...O..O.", 4
hexapawn.valid_state(_s)
b = MinMax(2, hexapawn, pf=3)
b.who_am_i = hexapawn.turn
print(hexapawn)
b.decision(_s)
print(hexapawn)
stat = partie(b, a, hexapawn, 1)
stat.statistics
''' ; testcode(code)

def fight(agent1, agent2, nbPartie):
    """
    """
    g = jeu.Morpion(3, tore=False)
    agent1.who_am_i = g.opponent
    agent2.who_am_i = g.turn
    stat = partie(agent1, agent2, g, nbPartie)
    return stat


    
if __name__ == '__main__':
    
    # #----le jeu----
    # g = jeu.Morpion(3, tore=False) #morpion de taille 5*5 forme torique
    
    # #----les paramètres
    pf=[k for k in range(1,10)] #différentes valeurs pour la profondeur
    nbSim=[_ for _ in range(100, 10000, 100)] #et pour le nombre de simulations
    
    # #----les joueurs
    # Agents = {
    # 'randy' : Randy('randy', g),
    # #--
    # 'minmax' : MinMax('minmax', g),
    # #--
    # 'toto_MMC' : NegAlphaBeta_Memory_MC('toto_MMC', g, pf=pf[0], nbSim=nbSim[0]),
    # #--
    # 'toto_M': NegAlphaBeta_Memory('toto_M', g, pf=pf[0]),
    # #--
    # 'toto_MC' :NegAlphaBeta_MC('toto_MC', g, pf=pf[0], nbSim=nbSim[0]),
    # #--
    # 'toto_UCB' : UCB('toto_UCB', g, pf=pf[0], nbSim=nbSim[0])}

    
    # advers=[randy, minmax]
    # agents=[MMC, M, MC, UCB]
    # STATS=[]
    # # for agent in advers:
    # #     for advers in agents:
    # #         STATS.append(fight(agent, advers, 4))
    # # print(STATS)
    
    # #STATS.append(fight(agents[0], advers[0], 4))
    
    # # f3=fight(randy,MC,2)
    # # f4=fight(minmax,MC,2)
    # f3=fight(randy,M,2)
    # # f4=fight(minmax,M,2)
    # # f5=fight(randy,UCB,2)
    # # f6=fight(minmax,UCB,2)
    
    # # f1=fight(randy,MMC,2)
    # # f2=fight(minmax,MMC,2)
    
    # #===============
    
    # # a.who_am_i = g.opponent
    # # _s = "X...O..OX", 4
    # # g.valid_state(_s)
    
    # # toto_MC.who_am_i = g.turn
    # # print(g)
    # # toto_MC.decision(_s)
    # # print(g)
    
    # # stat = partie(a, toto_MC, g, 3)
    # # stat[0].statistics
    # # print(stat)
    
    # # jeu = jeu.Morpion(3, tore=False) #morpion de taille 3*3 forme non torique
    # # Agents=[NegAlphaBeta_Memory('toto', jeu, pf=2), UCB('toto', jeu, nbSim=500), NegAlphaBeta_Memory_MC('toto', jeu, pf=2, nbSim=500)] #agents testés
    # # Advers=[Randy('randy', jeu), MinMax('minmax', jeu, pf=2)]
    
    
    
    # # print(rapidite(Agents, Advers, jeu, 10))
    
    
    # #==========================================PERFORMANCES
    
    
    # MMC = NegAlphaBeta_Memory_MC('toto_MMC', g, pf=pf[0], nbSim=nbSim[0])
    # M = NegAlphaBeta_Memory('toto_M', g, pf=pf[0])
    # MC = NegAlphaBeta_MC('toto_MC', g, pf=pf[0], nbSim=nbSim[0])
    # UCB = UCB('toto_UCB', g, pf=pf[0], nbSim=nbSim[0])   
    
    #====MEMORY====
    #==randy
    g0 = jeu.Morpion(3, tore=False)
    randy = Randy('randy', g0)
    M = NegAlphaBeta_Memory('toto_M', g0, pf=pf[0])
    randy.who_am_i = g0.opponent
    M.who_am_i = g0.turn
    stat0 = partie(randy, M, g0, 10)
    print(stat0.statistics)
    #==minmax
    g1 = jeu.Morpion(3, tore=False)
    minmax = MinMax('randy', g1)
    M = NegAlphaBeta_Memory('toto_M', g1, pf=pf[0])
    randy.who_am_i = g1.opponent
    M.who_am_i = g1.turn
    stat1 = partie(minmax, M, g1, 10)
    print(stat1.statistics)

    
    
    # randy.who_am_i = g.opponent
    # UCB.who_am_i = g.turn
    # stat1 = partie(randy, M, g, 10)
    # print(stat.statistics)
    
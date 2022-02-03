#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
require a 'jeu' with specific attributes
allow extra named parameters accessible by get_value(name_parameter)
provides:
read-only 'name' and 'game'
read-write 'who_am_i'
an abstract 'decision' method to be redefined in subclasses
a simple 'estimation' method that might be redefined in subclasses
estimation is made wrt to the root player 
> root_estimation for minmax / alphabeta
> turn_estimation for negamax approaches
"""

from typing import Iterable

class Player:
    """ classe abstraite d'où dériveront tous les joueurs """
    ID = 0
    WIN = 100
    def __init__(self, nom:str='default',
                 jeu:any=None, **kargs):
        """ nom: le nom du joueur pour l'affichage si on le souhaite
            jeu: le jeu auquel on veut faire joueur
            kargs: un dictionnaire permettant qui sera utile
        """

        if (self.WIN <0): self.WIN = 100
        # on verifie que l'on a tout ce qui nous est nécessaire
        # pour travailler
        latt = "__str__ state turn opponent timer"
        latt += " winner over actions move undo reset"
        for _att in latt.split():
            if not hasattr(jeu, _att):
                raise TypeError("cannot use this game, {} is missing"
                                "".format(_att))

        self.__name = str(nom).strip()
        jeu.reset()
        self.__game = jeu
        self.__who = None
        self.__idnum = self.ID+1
        Player.ID += 1
        self.__local = kargs

    def clone(self):
        """ duplicate player, same behavior but name is different """
        return self.__class__(self.__name, self.__game, **self.__local)

    def __eq__(self, other:'Player'):
        """ basic comparaison """
        return self.name == other.name
    @property
    def idnum(self) -> int:
        return self.__idnum
    @property
    def name(self) -> str:
        return self.__name+"_{:02d}".format(self.idnum)
    @property
    def game(self) -> any:
        return self.__game
    @property
    def who_am_i(self) -> any:
        return self.__who
    @who_am_i.setter
    def who_am_i(self, v):
        """ ignore if v is not valid """
        if v in (self.game.turn, self.game.opponent):
            self.__who = v
            
    def get_value(self, key:str) -> any:
        """ return the value for a given key, None if key doesnt exist """
        return self.__local.get(key, None)

    def decision(self, state:Iterable) -> 'action':
        """ given some state, provides one authorized action """
        raise NotImplementedError("decision is undefined")

    def estimation(self):
        """ a 3 states simple estimation for root's player
        require WIN > 0
        require WIN = - LOSS
        ensure return is one of the 3 values
        """
        if not self.game.over(): _e = 0
        elif self.game.winner is None: _e = 0
        elif self.game.winner == self.who_am_i: _e = self.WIN
        else: _e = - self.WIN
        return _e


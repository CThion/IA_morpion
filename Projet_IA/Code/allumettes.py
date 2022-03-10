#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à deux joueurs
Le jeu est constitué de N [1 à 25] allumettes
A tour de rôle 
un joueur retire de 1 à 3 allumettes

2 formes de jeu
A: le gagnant est celui qui prend la dernière allumette [True]
B: le perdant est celui qui prend la dernière allumette [False]
"""

from classes.abstract_game import Game
from tools.ezCLI import testcode
import random

class Matches(Game):
    def __init__(self, allumettes:int, prendre:bool=False):
        """ allumettes: 0 < nombre d'allumettes au départ <= 25
            prendre: True, gain si prend la dernière
                     False, gain si ne pas prendre la dernière
        """
        self.__board = max(min(25, allumettes), 1), bool(prendre)
        self.__init_board = self.__board[:]
        super().__init__(self.__init_board[0], prendre=self.__init_board[1])

    def reset(self):
        super().reset()
        self.__board = self.__init_board[:]

    def valid_state(self, cfg:tuple) -> bool:
        """ on peut enlever de 1 à 3 allumettes """
        _matches, _timer = cfg
        _max = self.__init_board[0]
        return _max - _timer >=  _matches >= _max - 3*_timer
    
    @property
    def board(self): return tuple(self.__board)

    @property
    def state(self): return self.board[0], self.timer
    @state.setter
    def state(self, cfg:tuple):
        if self.valid_state(cfg):
            self.__board = cfg[0], self.__board[1]
            self.timer = cfg[1]

    @property
    def actions(self) -> tuple:
        """ Choose the numer of matches """
        if self.over(): return ()
        return tuple(list(range(1, min(3, self.__board[0])+1)))

    @property
    def winner(self):
        """ defines the winner """
        if self.over():
            return self.opponent if self.board[1] else self.turn
        return None

    def over(self) -> bool:
        """ no move """
        return self.board[0] == 0

    def win(self) -> bool:
        """ no move available """
        return self.over()

    def move(self, action):
        if action in self.actions:
            _old, _rule = self.__board
            self.add_history(self.state)
            self.__board = _old - action, _rule
            self.timer += 1

    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.state = _
            
    def __str__(self):
        """ Modification de l'affichage par défaut """
        _msg = """
Il y a {:02} allumettes. Retirez de 1 à 3 allumettes.
Pour gagner vous {} prendre la dernière allumette\n
""".format(self.board[0],
           "devez" if self.board[1] else "ne devez pas")
        return _msg + self.show_msg()
    
    def show_msg(self):
        _msg = ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))
        if self.win():
            _msg += ("Partie terminée, gagnant '{}'\n"
                     .format(self.winner+1))
        return _msg

    @property
    def hash_code(self):
        """ hash value """
        return self.board[0]


if __name__ == "__main__":
    code = '''
jeu = Matches(13)
jeu.state
print(jeu)

jeu.move(3)
print(jeu)

jeu.move(2)
print(jeu)

jeu.undo()
print(jeu)

_s = 11, 4
jeu.valid_state(_s) # False
''' ; testcode(code)

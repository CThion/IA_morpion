#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à deux joueurs
Le jeu est constituée de 2 boites contenant des jetons
A tour de rôle un joueur 
- choisit une boite, qu'il vide
- répartit les jetons restant dans les deux boites

chaque boite doit contenir au moins un jeton
* la partie s'arrete quand un joueur ne peut pas respecter les règles
* le gagnant est celui qui a empêcher l'autre de jouer
* gauche <= droite (traitement symmétrique)

exemple
[ 2, 5]. Le joueur qui a le trait vide la boite B
et répartit les jetons de la boite A
l'adversaire doit jouer avec [1, 1]
il ne peut pas respecter les règles (impossible de répartir le résidu)
la partie s'arrête et le joueur est déclaré perdant
"""

from classes.abstract_game import Game
from tools.ezCLI import testcode
from typing import Sized
import random

class Divide(Game):
    def __init__(self, box1:int, box2:int, label:bool=True):
        """
        box1: nombre de jetons dans la boite 1
        box2: nombre de jetons dans la boite 2
        """
        if self.__valid(box1, box2):
            self.__board = [min(box1, box2), max(box1, box2)]
        else:
            a, b = random.choices(range(1,11), k=2)
            self.__board = [min(a, b), max(a, b)]
        self.__init_board = self.__board[:]
        super().__init__(*self.__init_board, label=bool(label))

    def reset(self):
        super().reset()
        self.__board = self.__init_board[:]

    @property
    def board(self): return tuple(self.__board)
    @property
    def state(self): return self.board, self.timer
    @state.setter
    def state(self, cfg:tuple):
        if self.__valid(*cfg[0]):
            self.__board = min(cfg[0]), max(cfg[0])
            self.timer = cfg[1]
    def __valid(self, *cfg):
        """ is this configuration fine """
        if len(cfg) != 2: return False
        if cfg[0] <= 0 or cfg[1] <= 0: return False
        if any([not isinstance(x, int) for x in cfg]): return False
        return True
    @property
    def actions(self) -> tuple:
        """ which box to remove, how many in 1st box """
        if self.over(): return ()
        _boxes = "AB"
        return tuple([ (_boxes[i], k)
                       for i in range(2)
                       for k in range(1, self.board[(i+1)%2]//2+1) ])
    @property
    def winner(self):
        """ defines the winner """
        if self.over(): return self.opponent
        return None
    def over(self) -> bool:
        """ no move """
        return sum(self.board) == 2
    def win(self) -> bool:
        """ no move available """
        return self.over()
    def move(self, action):
        _boxes = "AB"
        if action in self.actions:
            i = _boxes.index(action[0])
            j = action[1]
            k = self.__board[(i+1)%2]-j
            self.add_history(self.state)
            self.__board = j,k
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.state = _
    def show_msg(self):
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))
    def __str__(self):
        """ Modification de l'affichage par défaut """
        _msg = """
A & B : 2 boites contenant des jetons

Choisissez une boite qui sera vidée
Répartissez les jetons de l'autre boite dans A & B
- il faut au moins 1 jeton par boite

Le perdant est celui qui ne peut pas respecter les règles

"""
        return _msg+super().__str__()
    
    @property
    def hash_code(self):
        return int("{:02d}{:02d}".format(*self.board))


if __name__ == '__main__':
    code = '''
jeu = Divide(7, 17)
print(jeu)
jeu.hash_code

jeu.actions
jeu.move(jeu.actions[3])
print(jeu)
''' ; testcode(code)
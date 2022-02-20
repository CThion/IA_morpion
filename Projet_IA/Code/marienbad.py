#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Jeu à 2 joueurs

Le jeu est constitué de 3 lignes d'allumettes
A tour de rôle un joueur
* choisit une ligne
* retire de cette ligne des allumettes

La partie s'arrête quand il n'y a plus d'allumettes

Variantes
> configuration des lignes
1 -> k / k+1 -> 2k / 2k+1 -> 3k
k / random(k+1, 2k) / random(2k+1, 3k)

> nombre d'allumettes à prendre (1 à 3) ou (1 à toutes)
> le gagnant prend la dernière, le perdant prend la dernière
"""

from classes.abstract_game import Game
from tools.ezCLI import testcode
from typing import Sized
import random

class Marienbad(Game):
    def __init__(self, a:int, variante:int,
                 prise:bool=True, prendre:bool=True):
        """
        a: le nombre d'allumettes de référence entre 5 et 13
        variante: 0/1/2
        prise: True 1 à 3, False 1 à n
        prendre: True 'prendre la dernière pour gagner', 
                 False 'ne pas prendre la dernière pour gagner
        """
        random.seed()
        _a = int(a) if 5 <= a <= 13 else random.choice(range(5, 14))
        _b = variante if variante in range(3) else random.choice(range(3))
        _c, _d = bool(prise), bool(prendre)
        if _b == 0:
            _board = [ _a, 2*_a, 3*_a]
        elif _b == 1:
            _board = [_a, random.randrange(_a+1, 2*_a+1),
                      random.randrange(2*_a+1, 3*_a+1) ]
        else:
            _board = [int(2**(i-2) * _a) for i in range(3)]
        self.__board = _board, _c, _d
        self.__init_board = tuple(_board), _c, _d
        super().__init__(*self.__init_board)

    def reset(self):
        super().reset()
        self.__board = (list(self.__init_board[0]),
                        self.__init_board[1], self.__init_board[-1])

        
    @property
    def board(self): return tuple(self.__board[0])
    @property
    def state(self): return self.board, self.timer
    @state.setter
    def state(self, cfg:tuple):
        if self.valid_state(cfg):
            _, _1, _2 = self.__board
            self.__board = list(cfg[0]), _1, _2
            self.timer = cfg[1]

    def valid_state(self, cfg:tuple) -> bool:
        """ is this configuration fine """
        if len(cfg) != 2: return False
        _state, _timer = cfg
        if not self.__valid(*_state): return False
        # raws are constrained
        if any([cfg[0][i] > self.__init_board[0][i]
                for i in range(3)]): return False
        _a = sum(self.__init_board[0])
        _x = sum(cfg[0])
        _delta = [ a != b for a,b in zip(cfg[0], self.__init_board[0]) ]
        if _timer == 0:
            return tuple(cfg[0]) == self.__init_board[0]
        if _timer == 1: # exactly one change
            return _delta.count(True) == 1
        if _timer == 2: # at most 2 changes
            return 2 >= _delta.count(True) >= 1
        if self.__init_board[1]: # au moins 1, au plus 3
            return _a - 3*_timer <= _x <= _a - _timer
        # au moins 1
        return _x <= _a - _timer
        
        
    def __valid(self, *cfg) -> bool:
        """ check that it's fine """
        if len(cfg) != 3: return False
        if any([0 > cfg[i] for i in range(3)]): return False
        if any([not isinstance(x, int) for x in cfg]): return False
        return True
    @property
    def actions(self) -> tuple:
        """ access which box, remove how much matches """
        if self.over(): return ()
        _boxes = "ABC"
        _sz = len(_boxes)
        return tuple([ (_boxes[i], k+1)
                      for i in range(_sz)
                      for k in (range(min(3, self.board[i]))
                                if self.__board[1] else
                                range(self.board[i]))
                    ])
    def over(self) -> bool:
        """ no more move """
        return sum(self.board)==0
    @property
    def winner(self):
        """ defines the winner """
        if self.over():
            return self.opponent if self.__board[-1] else self.turn
        return None
    def win(self) -> bool:
        """ the only win is when it's over """
        return self.over()
    def move(self, action:tuple):
        """ action is a tuple of size 2 """
        if action in self.actions:
            _boxes = "ABC"
            i = _boxes.index(action[0])
            j = action[1]
            self.add_history(self.state)
            _v, _h, _p = self.__board
            _v[i] -= j
            self.__board = _v, _h, _p
            self.timer += 1
    def undo(self):
        _ = self.pop_history()
        if _ is not None:
            self.state = _

    def show_msg(self) -> str:
        return ("Coup(s) joué(s) = {}, trait au joueur {}\n"
                "".format(self.timer, self.turn+1))


    def __str__(self) -> str:
        """ Modification de l'affichage par défaut """
        _prise = ("1 à 3 allumettes" if self.__board[1] else
                  "au moins 1 allumette")
        _prendre = ("devez" if self.__board[-1] else
                    "ne devez pas")
        _msg = """
Vous avez devant vous 3 groupes d'allumettes
A votre tour de jeu vous devez choisir 1 groupe
et, dans ce groupe, vous enlevez {}

Pour gagner vous {} prendre la dernière allumette de la dernière boîte

""".format(_prise, _prendre)

        return _msg + super().__str__()

    @property
    def hash_code(self):
        return int("{:02d}{:02d}{:02d}".format(*self.board))    


if __name__ == '__main__':
    code = '''
jeu = Marienbad(5, 0)
s0 = jeu.state
print(jeu)
jeu.hash_code

jeu.move(jeu.actions[3])
s1 = jeu.state
jeu.move(jeu.actions[-1])
s2 = jeu.state

jeu.undo()
s1 == jeu.state # state after 1 move

jeu.valid_state( ((0,0,10), 7) ) # True
jeu.valid_state(s0) # True
jeu.valid_state(s1) # True
jeu.valid_state(s2) # True

jeu.valid_state( (s0[0], 1) ) # False
jeu.valid_state( ((4,9,14), 1) ) # False
jeu.valid_state( ((4,9,14), 3) ) # True
''' ; testcode(code)

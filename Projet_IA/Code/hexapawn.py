#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.abstract_game import Game
from tools.ezCLI import testcode
from tools.outils import p2c
import copy

class Hexapawn(Game):
    """ classe pour le jeu Hexapawn 
        2 joueurs 'X' est en haut
                  'O' est en bas
        '.' représente les cases vides
    """
    PAWN = ".XO"
    def __init__(self, nbl:int=3, nbc:int=3, cylindre:bool=False,
                 priorite:bool=False):
        # on définit la grille de jeu
        board = [ [ self.PAWN[0] for _ in range(nbc) ]
                  for _ in range(nbl) ]
        board[0] = [self.PAWN[1] for _ in range(nbc) ] # premiere rangee
        board[-1] = [self.PAWN[-1] for _ in range(nbc) ] # derniere rangee
        # on crée une variable pour stocker les informations
        self.__init_board = copy.deepcopy(board)
        super().__init__(nbl=nbl, nbc=nbc,
                         cylindre=bool(cylindre), priorite=bool(priorite))

    def reset(self):
        super().reset() # on appelle reset de la classe parente
        self.__board = copy.deepcopy(self.__init_board) # copie
        self.__winner = None

    @property
    def board(self): return tuple(self.__board)

    def show_msg(self) -> str:
        """ le message à ajouter """
        _cyl = "est" if self.get_parameter('cylindre') else "n'est pas"
        _prise = "est" if self.get_parameter('priorite') else "n'est pas"
        _str1 = "Le terrain {} cylindrique, la prise {} obligatoire"
        _str2 = "\nCoup(s) joué(s) = {}, trait au joueur '{}'\n"
        _msg = _str1.format(_cyl, _prise)
        _msg += _str2.format(self.timer, self.PAWN[self.turn+1])

        return _msg

    @property
    def hash_code(self) -> str:
        return ''.join([''.join([c for c in l])
                        for l in self.board])

    def valid_state(self, cfg:tuple) -> bool:
        """ control the data provided """
        return False
    
    @property
    def state(self) -> tuple:
        return self.hash_code, self.timer
    @state.setter
    def state(self, cfg:tuple):
        """ change board and timer """
        if not self.valid_state(cfg): return
        super().reset() # no history
        _, self.timer = cfg
        for i,x in enumerate(_):
            a,b = p2c(i, self.get_parameter('nbc'))
            self.__board[a][b] = x

    
if __name__ == "__main__":
    code = '''
jeu = Hexapawn()
jeu # test repr

print(jeu) # pour voir la grille
_x = "XXX...OOO", 0
jeu.valid_state(_x) # True

# comment accéder aux paramètres
jeu.key_arguments
jeu.get_parameter('nbl') # renvoie 3
jeu.get_parameter('nb lignes') # renvoie rien
jeu.PAWN # le vide le pion du 1er joueur le pion du second joueur

_s = "X.X.XOOO.", 2
jeu.valid_state( _s ) # renvoie True
jeu.state = _s
print(jeu) 

jeu.reset()
jeu.state # renvoie ('XXX...OOO', 0)

_t = "..XXXOOO.", 3
jeu.valid_state(_t)

_u = "XOX...XOO", 2
jeu.valid_state( _u ) # renvoie False

j1 = Hexapawn()
j2 = Hexapawn(cylindre=True)
j3 = Hexapawn(priorite=True)
j4 = Hexapawn(cylindre=True, priorite=True)
_s = "X.X.X.OOO", 1

j1.valid_state(_s) # True
j2.valid_state(_s) # True
j3.valid_state(_s) # True
j4.valid_state(_s) # True

_s = ".XXX..OOO", 1
j1.valid_state(_s) # True
j2.valid_state(_s) # True
j3.valid_state(_s) # True
j4.valid_state(_s) # True

jeu = Hexapawn(5, 4, True, True)
_s = "X"*4
_s += "."*12
_s += "O"*4
jeu.valid_state((_s, 0))

_t = "X.XX"
_t += ".X.."
_t += "."*4
_t += "...O"
_t += "O"*3+"."
jeu.valid_state( (_t, 2) ) # True
''' ; testcode(code)

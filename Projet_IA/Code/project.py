#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.abstract_game import Game
from tools.ezCLI import testcode
from tools.outils import p2c
import copy

class Morpion(Game):
    """ classe pour le jeu du Morpion
        le premier joueur a les pierres 'X'
        le second joueur a les pierres 'O'
        les cases vides sont représentées par '.'
    """
    PAWN = ".XO"
    def __init__(self, taille:int=3, tore:bool=False,
                 phase:int=0):
        """ on controle les paramètres pour éviter les problèmes """
        size = 3 if taille not in (3, 5, 7) else taille
        style = 0 if phase not in range(3) else phase
        # on définit la grille de jeu
        board = [ [ self.PAWN[0] for _ in range(size) ]
                  for _ in range(size) ]
        # on crée une variable pour stocker les informations
        self.__init_board = copy.deepcopy(board)
        # les variables utiles
        stones = (size*size -1)
        lines = {3:3, 5:4, 7:5}
        # on crée une variable pour stocker l'information
        self.__init_board = copy.deepcopy(board)
        # voisinage
        # Von Neumann, Moore
        self.__vicinity = [[ (-1,0), (0, 1), (1,0), (0,-1) ],
                           [ (i,j) for i in (-1,0,1) for j in (-1,0,1)
                             if (i != 0 and j != 0)]]
        super().__init__(nbl=size, nbc=size,
                         pierres=stones, ligne=lines[size],
                         tore=bool(tore), phase=style)

    def reset(self):
        super().reset() # reset classe parente
        self.__board = copy.deepcopy(self.__init_board) # copie
        # on sait que le tablier est carré
        self.__free = [ (x,y) for x in range(len(self.__board))
                        for y in range(len(self.__board)) ]
        self.__winner = None

    @property
    def board(self): return tuple(self.__board)

    def show_msg(self) -> str:
        """ le message à ajouter """
        _1 = "est un tore" if self.get_parameter('tore') else "est plan"
        _msg = "\nLe terrain {}\n".format(_1)
        _msg += "Coup(s) joué(s) = {}, trait au joueur '{}'\n"

        return _msg.format(self.timer, self.PAWN[self.turn+1])
        
    @property
    def hash_code(self) -> str:
        return ''.join([''.join([c for c in l])
                        for l in self.board])

    def valid_state(self, cfg:tuple):
        """ check that the cfg is valid :"""
        prmt = self.get_parameter('nbl')
        print(prmt)
        #1.  Que le tuple est de taille 2
        if len(cfg)!=2: return
        #2.  Que la première valeur est une chaîne de caractères de la bonne longueur
        
        #3.  Que la seconde valeur est un entier
        #4.  Que la chaîne ne contient que des valeurs dansself.PAWN
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
        _free = []
        for i,x in enumerate(_):
            a,b = p2c(i, self.get_parameter('nbc'))
            self.__board[a][b] = x
            if x == self.PAWN[0]: _free.append((a,b))
        self.__free = _free
        
    
if __name__ == "__main__":
    a=Morpion()
    t = ("XOX......", 3)
    a.valid_state(t)
    code = '''
jeu = Morpion()
jeu # test repr

jeu.state == (".........", 0) # True

# accéder aux paramètres
jeu.key_arguments
jeu.get_parameter('nbl') # renvoie 3
jeu.get_parameter('nbcol') # renvoie rien
# vide, pion joueur 1, pion joueur 2
jeu.PAWN

_t = "XOX......", 3
jeu.valid_state( _t )

_u = "XOX...XOO", 2
jeu.valid_state( _u ) # False

_v = "XOXOXXOO.", 11
jeu.valid_state( _v ) # False

jeu = Morpion(phase=1)
_v = "XOXOXXOO.", 11
jeu.valid_state( _v ) # True

jeu = Morpion(7, phase=2)
_v = "XOXOXXOO.", 11
jeu.valid_state( _v ) # False

_v = "XOXOXXOO."+'.'*40, 11
jeu.valid_state( _v ) # False

_v = "XOXOXXOO."+'.'*40, 8
jeu.valid_state( _v ) # True
''' ; #testcode(code)

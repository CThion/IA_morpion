#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.abstract_game import Game
from tools.ezCLI import testcode
import tools.outils as tool

import copy

class Morpion(Game):
    """ classe pour le jeu du Morpion
        le premier joueur a les pierres 'X'
        le second joueur a les pierres 'O'
        les cases vides sont représentées par '.'
        -----
        valeur intière: = cfg[1] = timer = sorte d'indice du tour courrant
        phase: \in (0,1,2), constante définie en début de partie, détermine mouvement possible dans la seconde partie du jeu
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
        stones = (size*size -1) #nombre de pierres totales
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
        """convert board state into a lingle line string"""
        return ''.join([''.join([c for c in l]) for l in self.board])

    def valid_state(self, cfg:tuple):
        """ check that the cfg is valid :"""
        nbl = self.get_parameter('nbl')
        nbc = self.get_parameter('nbc')
        pierres = self.get_parameter('pierres')
        phase = self.get_parameter('phase')
        ligne = self.get_parameter('ligne')
        #--le tuple est de taille 2
        if len(cfg)!=2: return False
        move, timer = cfg[0], cfg[1]
        #--première valeur est une string de la bonne longueur
        if type(move)!=str or len(move)!= nbl*nbc: 
          print(1)
          return False
        #--la seconde valeur est un entier
        if type(timer)!=int: 
          print(2)
          return False
        #--la chaîne ne contient que des valeurs dans self.PAWN
        for _ in move : 
            if _ not in self.PAWN : 
              print(3)
              return False
        #----stone check
        nbX = move.count(self.PAWN[1]); nbO = move.count(self.PAWN[2]) #nombre X et O
        #--nombre de ’X’ et le nombre de ’O’ sont compatibles avec timer
        if nbO+nbX > timer: 
          print(4)
          return False
        #--nombre de ’X’ est égal au nombre de ’O’ ou au nombre de ’O’+1
        if nbX not in (nbO, nbO+1): 
          print(5)
          return False
        #----phase check
        #--si phase==0, timer n’excède pas le nombre de pierres
        if phase == 0 and timer > pierres: 
          print(6)
          return False
        #--si phase!=0, timer n’excède pas la limite du temps de jeu
        elif phase!=0 and timer > pierres+2*nbl: 
          print(7)
          return False 
        #--
        if nbO+nbX < pierres and timer>nbO+nbX: 
          print(8)
          return False
        #--teste tous les alignements
        nbalign=0 #compteur d'alignement
        #parcours des liste de str d'orientation
        for func in [tool.lines,
                        tool.columns,
                        lambda s, l, c: tool.diag_moins(s, l, c, self.get_parameter('tore')),
                        lambda s, l, c: tool.diag_plus(s, l, c, self.get_parameter('tore'))]:  
          vectList = func(move, nbl, nbc)
          print('vectList', vectList)
          for vect in vectList: #parcours des str de la liste
            if ligne*self.PAWN[1] in vect or ligne*self.PAWN[2] in vect: #'OOO' or 'XXX' for 3*3
              nbalign +=1 #nouvel alignement trouvé
              print('nbalign', nbalign)
          if nbalign > 1: return False
        #--tous les tests sont passés
        return True
    
    @property
    def state(self) -> tuple:
        return self.hash_code, self.timer
    @state.setter
    def state(self, cfg:tuple):
        """ change board and timer """
        print("in")
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
    jeu=Morpion()
    _t = "XXXOO....", 5
    jeu.valid_state( _t ) #True
    code = '''
jeu = Morpion()
jeu # test repr

print(jeu) #affichage board

jeu.state= ("......X..", 0) #True
jeu.state

jeu.state == (".........", 0) # True

# accéder aux paramètres
jeu.key_arguments
jeu.get_parameter('nbl') # renvoie 3
jeu.get_parameter('nbcol') # renvoie rien
# vide, pion joueur 1, pion joueur 2
jeu.PAWN

_t = "XOX......", 3
jeu.valid_state( _t ) #True

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
''' ; testcode(code)

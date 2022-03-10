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
        """ restart the game """
        super().reset() # on appelle reset de la classe parente
        self.__board = copy.deepcopy(self.__init_board) # copie
        self.__winner = None

    @property
    def board(self):
        """ internal representation of the board """
        return tuple(self.__board)

    def show_msg(self) -> str:
        """ le message à ajouter """
        _cyl = "est" if self.get_parameter('cylindre') else "n'est pas"
        _prise = "est" if self.get_parameter('priorite') else "n'est pas"
        _str1 = "Le terrain {} cylindrique, la prise {} obligatoire"
        _str2 = "\nCoup(s) joué(s) = {}, trait au joueur {}\n"
        _msg = _str1.format(_cyl, _prise)
        _msg += _str2.format(self.timer, self.PAWN[self.turn+1])
        if self.over():
            if self.win():
                _msg += ("Partie terminée, gagnant '{}'\n"
                         .format(self.PAWN[self.winner+1]))
            else:
                _msg += "Partie terminée, match nul\n"

        return _msg

    @property
    def hash_code(self) -> str:
        """ required to be stored in memolry """
        return ''.join([''.join([c for c in l])
                        for l in self.board])

    def valid_state(self, cfg:tuple) -> bool:
        """ control the data provided """
        nbl = self.get_parameter('nbl')
        nbc = self.get_parameter('nbc')
        sz = nbl * nbc
        if (len(cfg) != 2 or
            not isinstance(cfg[0], str) or
            len(cfg[0]) != sz or
            not isinstance(cfg[1], int)):
            return False
        _ok = all([x in self.PAWN for x in cfg[0]])
        for i in (1, 2):
            _ok = _ok and (cfg[0].count(self.PAWN[i]) <= nbc)
        if not _ok : return _ok
        _up = cfg[0][:nbc]
        _down = cfg[0][-nbc:]
        _a = _up.count(self.PAWN[-1])
        _b = _down.count(self.PAWN[1])
        if _a > 1 or _b > 1 or _a * _b != 0: return False
        # moves
        _mD, _mU = 0, 0
        for i in range(nbl):
            _mD += i* cfg[0][i*nbc:(i+1)*nbc].count(self.PAWN[1])
            _mU += (nbl-1-i)* cfg[0][i*nbc:(i+1)*nbc].count(self.PAWN[2])
        return _mD + _mU <= cfg[1]


    @property
    def state(self) -> tuple:
        """ return the current state of the game """
        return self.hash_code, self.timer
    @state.setter
    def state(self, cfg:tuple):
        """ change board and timer """
        if not self.valid_state(cfg): return
        self.reset() # no history
        _, self.timer = cfg
        for i,x in enumerate(_):
            a,b = p2c(i, self.get_parameter('nbc'))
            self.__board[a][b] = x

    def __stones(self, player:str, _nbl:int, _nbc:int) -> list:
        """ collect the places where player has his stones """
        return [ (x,y) for x in range(_nbl)
                 for y in range(_nbc) if self.__board[x][y] == player ]

    def __target_move(self, x:int, y:int, d:int) -> tuple:
        """ if possible get the next move, else None """
        _x = x+d
        return (_x,y) if self.__board[_x][y] == self.PAWN[0] else None
    
    def __target_catch(self, x:int, y:int, d:int,
                       nbc:int, c:bool, o:str) -> list:
        """ given (x,y) and d find target point of opponent o """
        _x = x+d
        _rep = []
        for _d in (-1, +1):
            _y = y + _d
            if c: _y = _y%nbc
            if _y in range(nbc):
                _rep.append( None if self.board[_x][_y] != o else (_x, _y) )
        return _rep
    
    @property
    def actions(self):
        """ allowed actions
            who is the player
            what kind of board
            what kind of rule """
        if self.win(): return () # no move
        _cyl = self.get_parameter('cylindre')
        _prio = self.get_parameter('priorite')
        _nbl = self.get_parameter('nbl')
        _nbc = self.get_parameter('nbc')
        # find the player
        _d = 1 if self.turn == 0 else -1
        _p = self.PAWN[_d]
        _o = self.PAWN[-1] if self.turn == 0 else self.PAWN[1]
        _s = self.__stones(_p, _nbl, _nbc)
        # collect the moves
        _rep = []
        for a in _s:
            for b in self.__target_catch(*a, _d, _nbc, _cyl, _o):
                if b is not None: _rep.append( (a,b) )
        # if priorite and moves, no more moves
        if _prio and _rep !=[]: return tuple(_rep)
        # the standard moves
        for a in _s:
            _ = self.__target_move(*a, _d)
            if _ is not None: _rep.append( (a,_) )

        # no moves: the game is lost
        if _rep == []: self.__winner = self.opponent
        return tuple(_rep)

    def move(self, action:tuple):
        """ we got some action ((x,y), (a,b))
            we store the current state <board, timer>
            we change board and timer 
            return NOTHING, changes state !!!
        """
        if action in self.actions: # move is allowed
            src, target = action
            x,y = src
            a,b = target
            # store for undo
            _data = (src, self.__board[x][y],
                     target, self.__board[a][b],
                     self.timer)
            self.add_history( _data )
            if a in (0, self.get_parameter('nbl')-1):
                self.__winner = self.turn
            self.__board[a][b] = self.__board[x][y]
            self.__board[x][y] = self.PAWN[0]
            self.timer += 1
            
    def undo(self):
        """ undo, if possible the last move """
        _ = self.pop_history()
        if _ is not None:
            for i in (0, 2):
                x,y = _[i]
                self.__board[x][y] = _[i+1]
            self.timer = _[-1]
            self.__winner = None

    @property
    def winner(self):
        """ who is the winner """
        return self.__winner
    
    def win(self) -> bool:
        """ win is True iff there is a winner """
        return self.__winner is not None

    def over(self) -> bool:
        """ the game ended when there is a win (no draw allowed) """
        return self.actions == ()

def test_1():
    code = '''
jeu = Hexapawn()
jeu # test repr

print(jeu) # pour voir la grille

jeu.valid_state(("XXX...OOO", 0)) # True

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

def test_2():
    code = '''
jeu = Hexapawn()
jeu # test repr

print(jeu)
print(jeu.hash_code)

jeu.state == ("XXX...OOO", 0)

jeu.key_arguments
jeu.get_parameter('nbl')
jeu.get_parameter('nb lignes')

_s = "X.X.XOOO.", 2
jeu.valid_state( _s )
jeu.state = _s
print(jeu)

jeu.state == _s
jeu.actions

jeu.reset()
jeu.state
print(jeu)
jeu.actions

_t = "..XXXOOO.", 3
jeu.state = _t
jeu.state == _t
print(jeu)
jeu.actions

_u = "XOX...XOO", 2
jeu.valid_state( _u )
jeu.state = _u
jeu.state == _u
print(jeu)

j1 = Hexapawn()
j2 = Hexapawn(cylindre=True)
j3 = Hexapawn(priorite=True)
j4 = Hexapawn(cylindre=True, priorite=True)
_s = "X.X.X.OOO", 1

j1.state = _s
j2.state = _s
j3.state = _s
j4.state = _s
print(j1)

j1.actions # plan, sans priorite
j3.actions # plan avec priorite

j2.actions # cylindrique sans priorite
j4.actions # cylindrique avec priorite

_s = ".XXX..OOO", 1
j1.state = _s
j2.state = _s
j3.state = _s
j4.state = _s
print(j1)

j1.actions # plan, sans priorite
j3.actions # plan avec priorite

j2.actions # cylindrique sans priorite
j4.actions # cylindrique avec priorite

jeu = Hexapawn(5, 4, True, True)
_s = "X"*4
_s += "."*12
_s += "O"*4
jeu.state == (_s, 0)
print(jeu)

_t = "X.XX"
_t += ".X.."
_t += "."*4
_t += "...O"
_t += "O"*3+"."
jeu.valid_state( (_t, 2) )
jeu.state = (_t, 2)
print(jeu)
jeu.actions
''' ; testcode(code)
    
if __name__ == "__main__":
    print("TEST 1")
    test_1()
    print("TEST 2")
    test_2()

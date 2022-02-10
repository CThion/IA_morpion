#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from classes.abstract_game import Game
from tools.ezCLI import testcode
from tools.outils import p2c
from tools.outils import lines, columns, diag_plus, diag_moins
from tools.outils import longuest_chain, display_grid, intersection
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
        # les variables utiles
        stones = (size*size -1)
        lines = {3:3, 5:4, 7:5}
        # on crée une variable pour stocker l'information
        self.__init_board = copy.deepcopy(board)
        # voisinage
        # Von Neumann, Moore
        self.__vicinity = [[ (-1,0), (0, 1), (1,0), (0,-1) ],
                           [ (i,j) for i in (-1,0,1) for j in (-1,0,1)
                             if (i != 0 or j != 0)]]
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
        if self.over():
            if self.win():
                _msg += "Partie terminée, gagnant '{}'\n".format(self.winner)
            else:
                _msg += "Partie terminée, match nul\n"

        return _msg.format(self.timer, self.PAWN[self.turn+1])
        
    @property
    def hash_code(self) -> str:
        return ''.join([''.join([c for c in l])
                        for l in self.board])

    
    def valid_state(self, cfg:tuple):
        """ check that the cfg is valid """
        _nbl = self.get_parameter('nbl')
        _nbc = self.get_parameter('nbc')
        _sz = _nbl * _nbc

        # tests simples de typage et de taille
        if (len(cfg) != 2 or
            not isinstance(cfg[0], str) or
            len(cfg[0]) != _sz or
            not isinstance(cfg[1], int)):
            # print(0)
            return False
        for x in cfg[0]:
            if x not in self.PAWN:
                return False # bad markers
        _stones = self.get_parameter('pierres')
        _phase = self.get_parameter("phase")
        if _phase == 0 and cfg[1] > _stones:
            # print(2)
            return False
        if cfg[1] > _stones + 2 * _nbl:
            # print(3)
            return False
        _a = cfg[0].count(self.PAWN[1])
        _b = cfg[0].count(self.PAWN[2])
        if _a - _b not in (0, 1):
            # print(4)
            return False
        if cfg[1] < _stones:
            if _a + _b != cfg[1]:
                # print(5)
                return False
        else:
            if _a != _b or _a+_b != _stones:
                # print(6)
                return False
        """
        # recherche des alignements
        if _nbl == 3:
            _lines = lines(cfg[0], 3, 3)
            _cols = columns(cfg[0], 3, 3)
            _wins = [0,0]
            for line in _lines:
                for i in range(2):
                    _wins[i] += 1 if line.count(self.PAWN[i+1]) == 3 else 0
            for col in _cols:
                for i in range(2):
                    _wins[i] += 1 if col.count(self.PAWN[i+1]) == 3 else 0
            # print(7)
            return sum(_wins) <= 1
        else: # cas complexes
        """
        _tore = self.get_parameter('tore')
        _alignments = [ lines(cfg[0], _nbl, _nbc),
                        columns(cfg[0], _nbl, _nbc),
                        diag_plus(cfg[0], _nbl, _nbc, _tore),
                        diag_moins(cfg[0], _nbl, _nbc, _tore), ]
        _row = self.get_parameter('ligne')
        i,j = 0, 0
        _sol = [],[]
        for substrings in _alignments:
            #i = 0 lines, 1 columns, ...
            for string in substrings:
                # j = 0 1st substring
                if (len(string) < _row or
                    (string.count(self.PAWN[1]) < _row and
                     string.count(self.PAWN[-1]) < _row)
                    ): j = j+1 ; continue # no win possible
                for p in range(2):
                    # given the pawn
                    if any([x >= _row # winning row
                            for x in longuest_chain(string,
                                                    _tore,
                                                    self.PAWN[p+1])]):
                        _sol[p].append( (i,j) ) 
                j = j+1
            i,j = i+1, 0
        if len(_sol[0])*len(_sol[1]) !=0: # 2 joueurs gagnants
            # for _ in range(2): print(_sol[_])
            # print(8)
            return False
        _sol, _player = (_sol[0], 1) if len(_sol[0]) != 0 else (_sol[1], 2)
        if len(_sol) > 1: # conflict detection is needed
            # i,j : j position in _alignements[i], i kind  of alignment
            # no more than 1 row for each i
            _ = [0 for i in range(4)]
            for i,j in _sol: _[i] += 1
            if max(_) > 1:
                # print(9)
                return False
            # time for non intersected winning row
            if (len(_sol) > 2 # 3 rows might be problematic
                and intersection(cfg[0], self.PAWN[_player],
                                 _sol, _nbl, _nbc, _tore) == set()):
                # print(10)
                return False
        # print("ok", _sol, _player)
        # print(11)
        return True
    
    @property
    def state(self) -> tuple:
        return self.hash_code, self.timer
    @state.setter
    def state(self, cfg:tuple):
        """ change board and timer """
        if not self.valid_state(cfg): return
        #self.reset() # no history
        _, self.timer = cfg
        _free = []
        _count = [0, 0]
        _line = self.get_parameter('ligne')
        for i,x in enumerate(_):
            a,b = p2c(i, self.get_parameter('nbc'))
            self.__board[a][b] = x
            if x == self.PAWN[0]: _free.append((a,b))
            else:
                _idx = self.PAWN.index(x)-1
                _count[_idx] += 1
                if self.timer >= 2*_line -1 and _count[_idx] >= _line:
                    self.__check_win( (a,b), x )
        self.__free = _free
        
    def __check(self, c:tuple) -> bool:
        """ check coordinate is correct """
        sz = self.get_parameter('nbl')
        return c[0] in range(sz) and c[1] in range(sz)
            
    def __find(self, c:tuple, v:list, pawn:str) -> list:
        """ 
            c: coordinate (of the empty cell)
            v: vicinity 
            pawn: the content we are looking for
            :return: the list of pawn's coordinates which can move to c 
        """
        sz = self.get_parameter('nbl')
        _rep = []
        x,y = c
        for a,b in v:
            _x, _y = ( ((x+a)%sz, (y+b)%sz) if self.get_parameter('tore')
                      else (x+a, y+b) )
            if self.__check((_x, _y)) and self.__board[_x][_y] == pawn:
                _rep.append( (_x, _y) )
        return _rep

    def __diagnostic(self, candidates:list, last:tuple,
                     size:int, c:int) -> bool:
        """ candidates: coordinate to examine
            last: the last stone
            size: the number of stones in a row (get_parameter('ligne'))
            c: do we look at the line or the column

            return True if a win is detected
        """
        
        _sz = len(candidates)
        _ok = [False for i in range(_sz)]
        _pos = candidates.index(last)
        _tore = self.get_parameter('tore')
        _ = 'nbl' if c==0 else 'nbc'
        _nb = self.get_parameter(_)

        # # print("list {} index {}".format(candidates, _pos))
        # invariant between position and coordinates
        if _tore:
            for i in range(_sz):
                if candidates[(_pos+i)%_sz][c] == (last[c]+i)%_nb:
                    _ok[ (_pos+i)%_sz] = True
                else:
                    break
            for i in range(_sz):
                if candidates[(_pos-i)%_sz][c] == (last[c]-i)%_nb:
                    _ok[ (_pos-i)%_sz] = True
                else:
                    break
        else:
            for i in range(_pos, _sz): # from _pos to _sz
                if candidates[i][c] == last[c]+i-_pos: _ok[i] = True
                else: break
            for i in range(_pos-1, -1, -1): # from _pos-1 to 0
                if candidates[i][c] == last[c]+i-_pos: _ok[i] = True
                else: break
            
        # print(_ok)
        return _ok.count(True) >= size
    
    def __win_col(self, stones:list, last:tuple, size:int) -> bool:
        """ win in a column """
        _fun = lambda x: x[1] == last[1]
        _candidates = sorted([x for x in stones if _fun(x)],
                             key = lambda x: x[0])
        if len(_candidates) < size: return False
        return self.__diagnostic(_candidates, last, size, 0)
    
    def __win_line(self, stones:list, last:tuple, size:int) -> bool:
        """ win in a row """
        _fun = lambda x: x[0] == last[0]
        _candidates = sorted([x for x in stones if _fun(x)],
                             key = lambda x: x[1])
        if len(_candidates) < size: return False
        return self.__diagnostic(_candidates, last, size, 1)
    
    def __win_diag_up(self, stones:list, last:tuple, size:int) -> bool:
        """ win in a diag x+y """
        _nbc = self.get_parameter('nbc')
        _tore = self.get_parameter('tore')
        if _tore:
            _fun = lambda x: ((x[0]+x[1])%_nbc ==
                              (last[0]+last[1])%_nbc)
        else:
            _fun = lambda x: ((x[0]+x[1]) == (last[0]+last[1]))
        _candidates = sorted([x for x in stones if _fun(x)],
                             key = lambda x: x[1])
        if len(_candidates) < size: return False
        return self.__diagnostic(_candidates, last, size, 1)
            
    def __win_diag_down(self, stones:list, last:tuple, size:int) -> bool:
        """ win in a  diag x-y """
        _nbc = self.get_parameter('nbc')
        _tore = self.get_parameter('tore')
        if _tore:
            _fun = lambda x: ((x[0]-x[1])%_nbc ==
                              (last[0]-last[1])%_nbc)
        else:
            _fun = lambda x: ((x[0]-x[1]) == (last[0]-last[1]))
        _candidates = sorted([x for x in stones if _fun(x)],
                             key = lambda x: x[1])
        if len(_candidates) < size: return False
        return self.__diagnostic(_candidates, last, size, 1)

    def __check_win(self, c:tuple):
        """ given the last stone position, check alignment """
        _line = self.get_parameter('ligne')
        _nbl =  self.get_parameter('nbl')
        _nbc =  self.get_parameter('nbc')
        if self.timer+1 < 2*_line -1: return False
        _pawns = [ (x,y) for x in range(_nbl) for y in range(_nbc)
                   if self.__board[x][y] == self.PAWN[self.turn+1] ]
        # lazy evaluation, simplest first
        if (self.__win_col(_pawns, c, _line) or
            self.__win_line(_pawns, c, _line) or
            self.__win_diag_up(_pawns, c, _line) or
            self.__win_diag_down(_pawns, c, _line)):
            self.__winner = self.turn
    
    @property
    def actions(self):
        """ allowed actions """
        if self.win(): return ()
        _stones = self.get_parameter('pierres')
        _sz = self.get_parameter('nbl')
        _phase = self.get_parameter('phase')
        if self.timer < _stones:
            # pierres à poser sur case vide
            return tuple(self.__free)
        elif ( _phase > 0 and
              self.timer < _stones + 2 * _sz):
            _vide = self.__free[0] # on sait un vide
            _rep = self.__find(_vide, self.__vicinity[_phase-1],
                               self.PAWN[self.turn+1])
            return tuple(_rep)
        return ()
    
    def move(self, action:any):
        """
        action is a cell coordinates
        a,b is the coordinate where the last stone has been played
        """
        if action in self.actions: # move is allowed
            if self.timer < self.get_parameter('pierres'):
                a,b = action
                self.__board[a][b] = self.PAWN[self.turn+1]
                self.__free.remove( (a,b) )
                _data = (0, action, self.timer)
            else:
                x,y = action
                a,b = self.__free[0]
                _data = (1, action, self.__free[0], self.timer)
                self.__board[a][b] = self.__board[x][y]
                self.__board[x][y] = self.PAWN[0]
                self.__free = [ action ] # one cell is free
            self.add_history(_data)
            self.__check_win( (a,b) )
            self.timer += 1

    def undo(self):
        """ undo, if possible the last move """
        _ = self.pop_history()
        if _ is not None:
            if _[0] == 0:
                a,b = _[1]
                self.__board[a][b] = self.PAWN[0]
                self.__free.append( _[1] )
            else:
                a,b = _[1]
                x,y = _[2]
                self.__board[a][b] = self.__board[x][y]
                self.__board[x][y] = self.PAWN[0]
                self.__free = [ _[2] ]
            self.timer = _[-1]
            self.__winner = None
            
    def over(self) -> bool:
        """ it's over when there is no action """
        _stones = self.get_parameter('pierres')
        _phase = self.get_parameter('phase')
        _nl = self.get_parameter('nbl')
        _max = _stones if _phase == 0 else _stones + 2*_nl
        return (self.win() or self.timer == _max)
    
    @property
    def winner(self):
        """ None it's either a draw or non ending game """
        return self.__winner

    def win(self) -> bool:
        """ win is True iff there is a winner """
        return self.__winner is not None
    
def test_1():
    """ valid_test """
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
''' ; testcode(code)

def test_2():
    """ valid_test """
    code = '''
jeu = Morpion()
jeu # test repr

print(jeu)
print(jeu.hash_code)

jeu.state == (".........", 0) # True

jeu.key_arguments
jeu.get_parameter('nbl') # renvoie 3
jeu.get_parameter('nbcol') # renvoie rien

_t = "XOX......", 3
jeu.state = _t
jeu.state == _t # True
print(jeu)
jeu.actions

_u = "XOX...XOO", 2
jeu.valid_state( _u ) # False
jeu.state = _u
jeu.state == _u # False
print(jeu)
jeu.actions

_v = "XOXOXXOO.", 11
jeu.valid_state( _v ) # False
jeu.state = _v
jeu.state == _v # False
print(jeu)

jeu = Morpion(phase=1)
_v = "XOXOXXOO.", 11
jeu.valid_state( _v ) # True
jeu.state = _v
jeu.state == _v # True
print(jeu)
jeu.actions
''' ; testcode(code)

def test_3():
    """ winner detection: column """
    code = '''
_1 = "..XO..."
_0 = "."*7
_2 = "..X"+'.'*4
_t = _1*2+_0*2+_1*2 + _2
_s = _0*2 + _2 + _1*4

jeu = Morpion(7) # _s gagnante, _t non gagnante
jeu.valid_state( (_t, 9) )
jeu.valid_state( (_s, 9) )

jeu.state = _t, 9
print(jeu)

jeu.state = _s, 9
print(jeu)

jeu = Morpion(7, True) # _s & _t gagnantes
jeu.state = _t, 9
print(jeu)

jeu.state = _s, 9
print(jeu)
''' ; testcode(code)

def test_4():
    """ winner detection: line """
    code = '''
_1 = "." * 7
_2 = "XXOOXXX"
_3 = "OO"+"."*5
_s = _1*2+_3+_1+_2+_1*2

_4 = "OXXXXXO"
_t = _1*2+_3+_1+_4+_1*2

jeu = Morpion(7) # _s non gagnante, _t gagnante
jeu.valid_state( (_s, 9) )
jeu.valid_state( (_t, 9) )

jeu.state = _s, 9
print(jeu)

jeu.state = _t, 9
print(jeu)

jeu = Morpion(7, True) # _s et _t gagnantes
jeu.state = _s, 9
print(jeu)

jeu.state = _t, 9
print(jeu)
''' ; testcode(code)

def test_5():
    """ winner detection: diag1 """
    code = '''
_ = "."*7
_t = _
_t += "..XO..."
_t += ".XO...."
_t += "XO....."
_t += "O.....X"
_t += ".....X."+_
print(len(_t), _t.count('X'), _t.count('O'), _t.count('.'))

_s = "X"+"."*6
_s += ".XO"+"."*4
_s += "..XO"+"."*3
_s += "...XO.."
_s += "....XO."
_s += _*2
print(len(_s), _s.count('X'), _s.count('O'), _s.count('.'))

jeu = Morpion(7) # _s gagnante, _t non
jeu.valid_state( (_t, 9) )
jeu.valid_state( (_s, 9) )

jeu.state = (_t, 9)
print(jeu)

jeu.state = (_s, 9)
print(jeu)

jeu = Morpion(7, True) # _s et _t gagnantes
jeu.state = (_t, 9)
print(jeu)

jeu.state = (_s, 9)
print(jeu)
''' ; testcode(code)

def test_6():
    """ winner detection diag2 """
    code = '''
_ = "."*7
_t = _
_t +=  "....XO."
_t += ".....XO"
_t += "......X"
_t += "XO....."
_t += ".XO...."
_t += _
print(len(_t), _t.count('X'), _t.count('O'), _t.count('.'))

_s =  "....XO."
_s += "...XO.."
_s += _ * 2
_s += "X"+"."*6
_s += ".....OX"
_s += "....OX."
print(len(_s), _s.count('X'), _s.count('O'), _s.count('.'))

jeu = Morpion(7) # pas de situation gagnante
jeu.valid_state( (_t, 9) )
jeu.valid_state( (_s, 9) )

jeu.state = (_t, 9)
print(jeu)

jeu.state = (_s, 9)
print(jeu)

jeu = Morpion(7, True) # 2 situations gagnantes
jeu.state = (_t, 9)
print(jeu)

jeu.state = (_s, 9)
print(jeu)
''' ; testcode(code)

def test_7():
    code = '''
cfg = "XXX...OOO", 6
jeu = Morpion(3) 
jeu.valid_state(cfg) # False

cfg = "O.X"*3, 6
jeu.valid_state(cfg) # False

cfg = "XOXXO.OX...X...OOX...O..X", 13
jeu = Morpion(5, True)
jeu.valid_state( cfg ) # False

game = Morpion(5)
cfg = "XXOXX"+"O.O.O"+"XXXX."+"."*5+"O.O.O", 15
game.valid_state(cfg) # True
jeu.valid_state(cfg) # False

cfg = "XO..O"+"X.X.."+"OOX.O"+"X.X.."+"XOX.O", 15
game.valid_state(cfg) # True
jeu.valid_state(cfg) # False
''' ; testcode(code)

def test_8():
    code = '''
jeu = Morpion(5)
jeu1 = Morpion(5, tore=True)

_0 = "O.OXO"+"XXXXO"+".XXOO"+"XOX.."+"OOXO."
display_grid(_0, ".XO", 5)

_1 = [p for p in range(25) if _0[p] == "O"]
_2 = [_0[:x]+'.'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 20) ) # True
for s in _2: print(jeu.valid_state( (s, 19) )) # True

_0 = "OXO.X"+"XX.XX"+"O.XOO"+"OX.OO"+".XO.."
display_grid(_0, ".XO", 5)

_1 = [p for p in range(25) if _0[p] == "O"]
_2 = [_0[:x]+'.'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 18) ) # True
for s in _2: print(jeu.valid_state( (s, 17) )) # True

jeu1.valid_state( (_0, 18) ) # False
for s in _2: print(jeu1.valid_state( (s, 17) )) # False

_0 = "OXO.X"+".XXXX"+"OXXOO"+"OX.OO"+"..O.."
display_grid(_0, ".XO", 5)

_1 = [p for p in range(25) if _0[p] == "O"]
_2 = [_0[:x]+'.'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 18) ) # False
for s in _2: print(jeu.valid_state( (s, 17) )) # False

_0 = "OO.XO"+"XXXXO"+".XO.O"+"XXO.."+".XO.."
display_grid(_0, ".XO", 5)

_1 = [p for p in range(25) if _0[p] == "."]
_2 = [_0[:x]+'O'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 17) ) # False
for s in _2: print(jeu.valid_state( (s, 18) )) # False

jeu1.valid_state( (_0, 17) ) # False
for s in _2: print(jeu1.valid_state( (s, 18) )) # False

jeu = Morpion(7)
jeu1 = Morpion(7, True)
_0 = "OXO.XO.XXXXXO.OXXOOO..X.OO..XX.O....O"+"."*12
display_grid(_0, ".XO", 7)

_1 = [p for p in range(7*7) if _0[p] == 'O']
_2 = [_0[:x]+'.'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 24) ) # False
for s in _2: print(jeu.valid_state( (s, 23) )) # False

jeu1.valid_state( (_0, 24) ) # False
for s in _2: print(jeu1.valid_state( (s, 23) )) # False

_0 = "OX....XXXOOXXXOX..X..OOO.OO.O......OX...O.XX....."
display_grid(_0, ".XO", 7)

_1 = [p for p in range(7*7) if _0[p] == 'O']
_2 = [_0[:x]+'.'+_0[x+1:] for x in _1]
jeu.valid_state( (_0, 24) ) # True
for s in _2: print(jeu.valid_state( (s, 23) )) # True

jeu1.valid_state( (_0, 24) ) # False
for s in _2: print(jeu1.valid_state( (s, 23) )) # False
''' ; testcode(code)
    
if __name__ == "__main__":
    print("use test_x() for x in 1..8")

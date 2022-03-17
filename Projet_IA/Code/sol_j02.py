#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random
from tools.outils import count

#=========== les classes à mettre en oeuvre pour le jalon 02 ===========#

class Human(Player):
    """ the human interface 
        valid for any game, choices are numbered
    """
    def decision(self, state):
        """ get the state """
        self.game.state = state
        print(self.game)
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None

        _yes = 'oO0Yy'
        _n = len(self.game.actions)
        _a = ''
        while not _a.isnumeric() or int(_a) not in range(_n):
            _y = input("Voulez vous voir les choix disponibles ? "
                       "[default is yes] ")
            if _y in _yes: self.__menu()
            _a = input("Votre choix parmi 0..{} ? "
                       "".format(_n-1))
        return self.game.actions[int(_a)]
    
    def __menu(self):
        """ print the choices """
        _str = ""
        for i,a in enumerate(self.game.actions):
            _str+= "choix {:02d}: action {}\n".format(i, a)
        print(_str)
        

class Randy(Player):
    """ random player """
    def decision(self, state):
        """ get the state """
        self.game.state = state

        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        
        return random.choice(self.game.actions)
        
class MinMax(Player):
    """ 
        the minmax player: parameter pf 
    """

    @property
    def nbCalls(self):
        return self.__eval_min.tick + self.__eval_max.tick
    
    def decision(self, state):
        """ the main method """
        #===== these lines are usefull for @count =======#
        self.__class__.__eval_min.tick = 0   # reset tick
        self.__class__.__eval_max.tick = 0   # reset tick
        #======== normal decision starts here ===========#
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        
        _v, _a = -self.WIN -1, None
        pf = self.get_value('pf')
        for a in self.game.actions:
            self.game.move(a)
            _ = self.__eval_min(pf-1)
            if _ > _v: _v, _a = _, a
            self.game.undo()

        if __debug__:
            print(">>> best is {}, with value {}".format(_a, _v))
            print(">>> Recursive calls {}".format(self.nbCalls))
            if _a is None:
                print(self.game)
                raise ValueError("this shoudlnt be")
        return _a

    @count # might be removed
    def __eval_min(self, pf:int) -> float:
        if pf == 0 or self.game.over():
            return self.estimation()

        _m = self.WIN+1
        for a in self.game.actions:
            self.game.move(a)
            _m = min(_m, self.__eval_max(pf-1))
            self.game.undo()

        return _m

    @count # might be removed
    def __eval_max(self, pf:int) -> float:
        if pf == 0 or self.game.over():
            return self.estimation()

        _M = -self.WIN-1
        for a in self.game.actions:
            self.game.move(a)
            _M = max(_M, self.__eval_min(pf-1))
            self.game.undo()

        return _M

class Negamax(Player):
    """ 
        the negamax player: parameter pf
    """
    @property
    def nbCalls(self): return self.__eval_negamax.tick

    def decision(self, state):
        """ the main method """
        #===== this line is usefull for @count =============#
        self.__class__.__eval_negamax.tick = 0  # reset tick
        #=========== normal decision starts here ===========#
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        _v, _a = -self.WIN-1, None
        pf = self.get_value('pf')
        for a in self.game.actions:
            self.game.move(a)
            _ = - self.__eval_negamax(pf-1)
            if _ > _v: _v, _a = _, a
            self.game.undo()

        if __debug__:
            print(">>> best is {}, with value {}".format(_a, _v))
            print(">>> Recursive calls {}".format(self.nbCalls))
            if _a is None:
                print(self.game)
                raise ValueError("this shoudlnt be")
        return _a

    @count
    def __eval_negamax(self, pf:int) -> float:
        """ this is eval_max """
        if pf == 0 or self.game.over():
            _c = 1 if self.who_am_i == self.game.turn else -1
            return _c * self.estimation()

        _m = -self.WIN-1
        for a in self.game.actions:
            self.game.move(a)
            _m = max(_m, -self.__eval_negamax(pf-1))
            self.game.undo()

        return _m
    
class AlphaBeta(Player):
    """ 
        the alphabeta player: parameter pf
    """
    @property
    def nbCalls(self):
        return self.__cut_alpha.tick + self.__cut_beta.tick

    def decision(self, state):
        """ the main method """
        #===== these lines are usefull for @count =======#
        self.__class__.__cut_alpha.tick = 0  # reset tick
        self.__class__.__cut_beta.tick = 0   # reset tick
        #======== normal decision starts here ===========#
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        _bound = self.WIN+1
        _v, _a = -_bound, None
        alpha, beta = -_bound, _bound
        pf = self.get_value('pf')
        for a in self.game.actions:
            if alpha >= beta: break
            self.game.move(a)
            _ = self.__cut_alpha(pf-1, alpha, beta)
            self.game.undo()
            if _ > _v: _v, _a = _, a
            alpha = max(_, alpha)
            
        if __debug__:
            print(">>> best is {}, with value {}".format(_a, _v))
            print(">>> Recursive calls {}".format(self.nbCalls))
            if _a is None:
                print(self.game)
                raise ValueError("this shoudlnt be")
        return _a

    @count
    def __cut_alpha(self, pf:int, alpha:float, beta:float) -> float:
        if pf == 0 or self.game.over():
            return self.estimation()

        for a in self.game.actions:
            if alpha >= beta: return beta
            self.game.move(a)
            _m = self.__cut_beta(pf-1, alpha, beta)
            self.game.undo()
            beta = min(_m, beta)

        return beta

    @count
    def __cut_beta(self, pf:int, alpha, beta) -> float:
        if pf == 0 or self.game.over():
            return self.estimation()

        for a in self.game.actions:
            if alpha >= beta: return beta
            self.game.move(a)
            _M = self.__cut_alpha(pf-1, alpha, beta)
            self.game.undo()
            alpha = max(_M, alpha)

        return alpha

class NegAlphaBeta(Player):
    """ 
        the alphabeta player: parameter pf
    """
    @property
    def nbCalls(self): return self.__cut.tick
        
    def decision(self, state):
        """ the main method """
        #===== this line is usefull for @count ======#
        self.__class__.__cut.tick = 0    # reset tick
        #====== normal decision starts here =========#
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        beta = self.WIN+1
        alpha = -beta
        _v, _a = alpha, None
        pf = self.get_value('pf')
        for a in self.game.actions:
            self.game.move(a)
            _ = - self.__cut(pf-1, alpha, beta)
            self.game.undo()
            if _ > _v: _v, _a = _, a
            
        if __debug__:
            print(">>> best is {}, with value {}".format(_a, _v))
            print(">>> Recursive calls {}".format(self.nbCalls))
            if _a is None:
                print(self.game)
                raise ValueError("this shoudlnt be")
        return _a

    @count
    def __cut(self, pf:int, alpha:float, beta:float) -> float:
        """ we use, max thus cut_beta """
        
        if pf == 0 or self.game.over():
            _c = 1 if self.who_am_i == self.game.turn else -1
            return _c * self.estimation()

        for a in self.game.actions:
            if alpha >= beta: return beta
            self.game.move(a)
            _M = - self.__cut(pf-1, -beta, -alpha)
            self.game.undo()
            alpha = max(_M, alpha)

        return alpha

#====================== exemples de code test ==========================#
def test_decision(joueur):
    """ joueur est une classe telle que Human, Randy, MinMax """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
print(jeu) # on attend 13 allumettes

moi = joueur('toto', jeu, pf=3)
moi.decision( (3, 4) ) is None # on attend True au test
moi.game.state == (3,4) # on attend True
jeu.state == (13,0) # on attend True

moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (7, 3) ) is None # on attend True au test
moi.game.state == (7,3) # on attend 7 allumettes
jeu.state == (13,0) # on attend True

moi.decision( (7, 4) ) in (1, 2, 3) # on attend True au test
moi.game.state == (7, 4)  # on attend True au test
jeu.state == (13,0) # on attend True

from divide_left import Divide
jeu = Divide(7, 17) # le but partager les jetons en 2
print(jeu)

moi = joueur('boxer', jeu, pf=3)
moi.decision( ((3, 4), 1) ) is None # on attend True au test
moi.game.state == ((3,4), 1) # on attend True
jeu.state == ((7,17), 0) # on attend True

moi.who_am_i = jeu.opponent # moi est le second joueur
moi.decision( ((7, 3), 4) ) is None # on attend True au test
moi.game.state == ((3,7), 4) # on attend True
jeu.state == ((7,17), 0) # on attend True

moi.decision( ((7, 4), 3)) in (('A',1),('A',2),('A',3),('B',1),('B',2)) # on attend True au test
moi.game.state == ((4, 7), 3)  # on attend True au test
jeu.state == ((7,17), 0) # on attend True
''' ; testcode(code)

def test_clever(joueur):
    """ on attend que joueur soit MinMax Negamax AlphaBeta Neg_AlphaBeta """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
jeu.state == (13, 0) # on attend True au test

moi = joueur('toto', jeu, pf=3)
moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 3 # on attend True au test
moi.game.state == (3, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

moi.decision( (6, 4) ) == 2 # on attend True au test
moi.game.state == (6, 4) # on attend True au test
jeu.state == (13, 0) # on attend True au test

jeu2 = Matches(13, False) # le but ne pas prendre la dernière allumette
moi = joueur('toto', jeu2, pf=3)
moi.who_am_i = jeu2.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 2# on attend True au test
moi.game.state == (3, 4)  # on attend True au test
jeu2.state == (13, 0) # on attend True au test

moi.decision( (4, 4) ) == 3 # on attend True au test
moi.game.state == (4, 4) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
moi.game.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 1 # on attend True au test
moi.game.state == (6, 4) # on attend True au test

from divide_left import Divide
jeu3 = Divide(7, 17)
moi = joueur('malin', jeu3, pf=3)
moi.who_am_i = jeu3.turn # moi est le premier joueur
moi.decision( ((3,4), 4) ) == ('A', 1)
moi.game.state == ((3,4), 4)
''' ; testcode(code)
    

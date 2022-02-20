#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Classe abstraite de jeu à 2 joueurs 
"""
from tools.ezCLI import grid

class Game:
    def __init__(self, *args, **kargs):
        self.__args = args
        self.__kargs = kargs
        self.reset()

    def reset(self):
        """ what should be restarted """
        self.timer = 0
        self.__history = []

    def clone(self):
        """ clonage might be redefined """
        return self.__class__(*self.__args, **self.__kargs)
    
    @property
    def arguments(self):
        """ return unamed arguments of the class """
        return self.__args
    @property
    def key_arguments(self) -> dict:
        """ return named arguments of the class """
        return self.__kargs.copy()

    def get_parameter(self, att:str) -> any:
        """ given a parameter provides value 
            les attributs valides: sont dans self.key_arguments
        """
        return self.__kargs.get(att, None)
    
    @property
    def turn(self):
        """ return the player who should play aka current player """
        return self.timer%2
    @property
    def opponent(self):
        """ return the opponent of the current player """
        return (self.turn+1)%2

    def add_history(self, value):
        """ store useful info that might be undone """
        self.__history.append(value)
    def pop_history(self):
        """ go one step back """
        if self.__history != []:
            return self.__history.pop(-1)
    def display_history(self):
        for _ in range(len(self.__history), 0, -1):
            print("step {} val {}".format(_,self.__history[_-1]))

    def __repr__(self):
        return ("{0}({1.arguments}, {1.key_arguments})"
                "".format(self.__class__.__name__,self))

    def __str__(self) -> str:
        """ display board + msg """
        if not isinstance(self.board[0], (list, tuple)):
            _grid = [ self.board ]
        else:
            _grid = self.board

        _lab = bool(self.get_parameter('label'))
        return grid(_grid, label=_lab, size=3)+"\n"+self.show_msg()
    
    def show_msg(self) -> str:
        """ msg to be displayed after the board """
        return ''

    @property
    def winner(self):
        """ the winner of the game """
        return None
    @property
    def hash_code(self):
        """ required the hash value: either int or str """
        raise NotImplementedError("hash_code: a property to define")
    @property
    def board(self):
        """ internal storage of the board """
        raise NotImplementedError("board getter: to be defined")
    
    def valid_state(self, st) -> bool:
        """ verify that the state provided is valid """
        raise NotImplementedError("valid_state(value): to be defined")
    @property
    def state(self):
        """ return the current state of the game """
        raise NotImplementedError("state getter: to be defined")
    @state.setter
    def state(self, val):
        """ set the current state if it's valid """
        raise NotImplementedError("state setter: to be defined")
    
    def over(self) -> bool:
        """ game is over """
        raise NotImplementedError("over(): to be defined")        
    def win(self) -> bool:
        """ game is won """
        raise NotImplementedError("win(): to be defined")
    
    @property
    def actions(self) -> tuple:
        """ the legal actions """
        raise NotImplementedError("actions getter: to be defined")

    def move(self, act):
        """ given an action modify board, history and timer """
        raise NotImplementedError("move(action): to be defined")

    def undo(self):
        """ undo the last move if exists """
        raise NotImplementedError("undo(): to be defined")
            

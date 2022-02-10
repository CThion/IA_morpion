#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "19.02.21"
__usage__ = "Project 2022: tests jalon 02: Randy"
__update__ = "04.02.22"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk
from allumettes import Matches as A
from divide_left import Divide as B

THAT="Randy"

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

class TestKlass(unittest.TestCase):
    """ Is 'THAT' correctly setup """
    def test_sub(self):
        """ THAT is a Player """
        klass = THAT
        player = "Player"
        game = "Game"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        self.assertTrue(issubclass(getattr(tp, klass),
                                   getattr(tp, player)),
                        "{} should be a subclass of {}".format(klass, player))
        if hasattr(tp, game):
            self.assertFalse(issubclass(getattr(tp, klass),
                                        getattr(tp, game)),
                             "{} should be a subclass of {}"
                             "".format(klass, player))
        self.assertFalse(hasattr(getattr(tp, klass), 'winner'),
                         "{} should not have winner's attribute")
        
class TestPrivacy(unittest.TestCase):
    """ all attributes are provided by 'Player' """
    def test_privacy(self):
        """ one expects only to find 'decision' """
        klass = THAT
        player = "Player"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        _1 = getattr(tp, klass)
        _2 = _1.__dict__
        _4 = "_{}__".format(_1.__name__)
        _3 = _1.__slots__ if hasattr(_1, '__slots__') else None
        self.assertTrue('decision' in _2,
                        "missing decision in {}"
                        "".format(_1.__name__))
        self.assertFalse('__init__' in _2,
                         "'__init__' is forbidden in {}"
                         "".format(_1.__name__))
        _latt_public = [x for x in _2 if not x.startswith((_4, '__'))]
        self.assertEqual(len(_latt_public), 1,
                         "{} public methods are too numerous"
                         "".format(_latt_public))
        _latt_slots = ([] if _3 is None else
                       [x for x in _3  if not x.startswith('__')])
        self.assertEqual(len(_latt_slots), 0,
                         "{} public or protected attributes are forbiden"
                         "".format(_latt_slots))

class TestDefault(unittest.TestCase):
    """ check the correct default behavior of 'THAT' """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = A(13)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu)

    @patch('builtins.print')
    def test_None_decision_init(self, mock_prn):
        """ cant decide when I dont know who am i """
        self.assertIsNone(self.o.who_am_i, "wrong player should be None")
        self.assertIsNone(self.o.decision(self.jeu.state),
                          "wrong answer, should be None")

    @patch('builtins.print')
    def test_None_decision(self, mock_prn):
        """ cant decide when not my turn """
        self.assertIsNone(self.o.who_am_i, "wrong player should be None")
        self.o.who_am_i = self.jeu.opponent
        self.assertIsNone(self.o.decision(self.jeu.state),
                          "wrong answer, should be None")

class TestBehaviorA(unittest.TestCase):
    """ check the correct default behavior of 'THAT' """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = A(13)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu)

    def test_decision_output(self):
        """ given an answer is it ok """
        self.assertIsNone(self.o.who_am_i, "wrong player should be None")
        self.o.who_am_i = self.jeu.turn
        _0 = 10, 2
        _1 = self.o.decision( _0 )
        self.assertEqual(self.jeu.state, _0,
                         "expect a valid state")
        self.assertTrue(_1 in self.jeu.actions,
                        "expect a valid action: got {}".format(_1))

class TestBehaviorB(unittest.TestCase):
    """ check the correct default behavior of 'THAT' """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = B(7, 17)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu)

    def test_decision_output(self):
        """ given an answer is it ok """
        self.assertIsNone(self.o.who_am_i, "wrong player should be None")
        self.o.who_am_i = self.jeu.turn
        _0 = (5, 7), 2
        _1 = self.o.decision( _0 )
        self.assertEqual(self.jeu.state, _0,
                         "expect a valid state")
        self.assertTrue(_1 in self.jeu.actions,
                        "expect a valid action: got {}".format(_1))
        
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass, TestDefault,
               TestBehaviorA, TestBehaviorB)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

if __name__ == "__main__":
    param = input("quel est le fichier à traiter ? ")
    if not os.path.isfile(param): ValueError("need a python file")

    etudiant = param.split('.')[0]

    _out = chk.check_property(etudiant != '','acces au fichier')
    print("tentative de lecture de {}".format(etudiant))
    tp = __import__(etudiant) # revient à faire import XXX as tp

    unittest.main()
    



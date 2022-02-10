#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "19.02.21"
__usage__ = "Project 2022: tests jalon 02: MinMax"
__update__ = "07.02.22"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk
from allumettes import Matches as A
from divide_left import Divide as B
from hexapawn import Hexapawn
from morpion import Morpion


###
THAT="MinMax"

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

class TestKlass(unittest.TestCase):
    """ Is 'MinMax' correctly setup """
    def test_sub(self):
        """ MinMax is a Player """
        klass = THAT
        player = "Player"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        self.assertTrue(issubclass(getattr(tp, klass),
                                   getattr(tp, player)),
                        "{} should be a subclass of {}".format(klass, player))
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

        _allowed = "nbCalls nbCalls_min nbCalls_max".split()
        _latt_public = [ _ for _ in _latt_public if _ not in _allowed ]
        
        self.assertEqual(len(_latt_public), 1,
                         "{} public methods are too numerous"
                         "".format(_latt_public))
        _latt_slots = ([] if _3 is None else
                       [x for x in _3  if not x.startswith('__')])
        self.assertEqual(len(_latt_slots), 0,
                         "{} public or protected attributes are forbiden"
                         "".format(_latt_slots))
        
class TestDefault(unittest.TestCase):
    """ check the correct default behavior of 'MinMax' """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = A(17)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu, pf=3)

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

class TestMatches(unittest.TestCase):
    """ find the best action for matches """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)

    @patch('builtins.print')    
    def test_take_last(self, mock_prn):
        """ take the last match """
        self.jeu = A(13, True) # prendre la derniere
        self.o = self.K('x', self.jeu, pf=3)
        self.o.who_am_i = self.jeu.turn
        _0 = self.o.decision( (3,4) )
        self.assertEqual(_0, 3, "expected 3 found {}".format(_0))
        _1 = self.o.decision( (5,4) )
        self.assertEqual(_1, 1, "expected 1 found {}".format(_0))
        _1 = self.o.decision( (6,4) )
        self.assertEqual(_1, 2, "expected 2 found {}".format(_0))

    @patch('builtins.print')    
    def test_leave_last(self, mock_prn):
        """ dont take the last match """
        self.jeu = A(13, False) # ne pas prendre la derniere
        self.o = self.K('x', self.jeu, pf=3)
        self.o.who_am_i = self.jeu.turn
        _0 = self.o.decision( (3,4) )
        self.assertEqual(_0, 2, "expected 2 found {}".format(_0))
        _1 = self.o.decision( (5,4) )
        self.assertEqual(_1, 1, "expected 1 found {}".format(_0))
        _1 = self.o.decision( (6,4) )
        self.assertEqual(_1, 1, "expected 1 found {}".format(_0))
        
class TestBoxes(unittest.TestCase):
    """ find the best action for matches """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = B(7,17)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu, pf=3)
        self.o.who_am_i = self.jeu.turn

    @patch('builtins.print')    
    def test_split(self, mock_prn):
        """ force next move to a win """
        _s = (3,4), 4
        _0 = self.o.decision(_s)
        self.assertEqual(_0, self.jeu.actions[0],
                         "wrong choice {}".format(_0))


class TestHexaPawn(unittest.TestCase):
    """ do we find the best move """
    def setUp(self):
        klass = THAT
        chk.check_class(tp, klass)
        self.jeu = Hexapawn() # à définir
        self.K = getattr(tp, klass)

    @patch('builtins.print')    
    def test_attak(self, mock_prn):
        """ find the winning play at depth 1..4 """
        pfl = range(1, 5)
        _rep = []
        _0 = "X.."+"O.X"+".O.",4
        for pf in pfl:
            self.o = self.K('bidon', self.jeu, pf=pf)
            self.o.who_am_i = self.jeu.turn
            _rep.append(self.o.decision(_0))
        _val = [_rep[0] == x for x in _rep ]
        self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep))
        _1 = self.jeu.actions[0]
        self.assertEqual(_rep[0], _1,
                         "expected {}, found {}".format(_1, _rep[0]))
        
class TestMorpion(unittest.TestCase):
    """ do we find the best move """
    def setUp(self):
        klass = THAT
        chk.check_class(tp, klass)
        self.jeu = Morpion(5) # à définir
        self.K = getattr(tp, klass)
        
    @patch('builtins.print')    
    def test_attak(self, mock_prn):
        """ find the winning play at depth 1..4 """
        pfl = range(1, 5)
        _rep = []
        _0 = '.'*5+"..XO."*3+'.'*5, 6
        for pf in pfl:
            self.o = self.K('bidon', self.jeu, pf=pf)
            self.o.who_am_i = self.jeu.turn
            _rep.append(self.o.decision(_0))
        _val = [_rep[0] == x for x in _rep ]
        self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
        _1 = self.jeu.actions[2]
        self.assertEqual(_rep[0], _1,
                         "expected {}, found {}".format(_1, _rep[0]))

    @patch('builtins.print')    
    def test_defence(self, mock_prn):
        """ find the key play at depth 2..5 """
        pfl = range(2, 6)
        _0 = "X..O."+"."*5+"..XO."*2+'.'*5, 6
        _rep = []
        for pf in pfl:
            self.o = self.K('bidon', self.jeu, pf=pf)
            self.o.who_am_i = self.jeu.turn
            _rep.append(self.o.decision(_0))
            _rep.append(self.o.decision(self.jeu.state))
        _val = [_rep[0] == x for x in _rep ]
        self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
        _1 = self.jeu.actions[6]
        self.assertEqual(_rep[0], _1,
                         "expected {}, found {}".format(_1, _rep[0]))

    @patch('builtins.print')    
    def test_blind_spot(self, mock_prn):
        """ cant find the right answer at depth 1 """
        _0 = "X..O."+"."*5+"..XO."*2+'.'*5, 6
        self.o = self.K('bidon', self.jeu, pf=1)
        self.o.who_am_i = self.jeu.turn
        _val = self.o.decision(_0)
        _1 = self.jeu.actions[0]
        self.assertEqual(_val, _1,
                         "Expected {}, found {}".format(_1, _val))
        
        
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass, TestDefault,
               TestMatches, TestBoxes, TestHexaPawn, TestMorpion)
    
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
    



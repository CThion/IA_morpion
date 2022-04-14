#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "01.04.21"
__usage__ = "Project 2022: tests jalon 03: UCB"
__update__ = "11.04.22"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk
from allumettes import Matches # TestAnswersMatches
from divide_left import Divide # TestAnswersBoxes
from dice import Dice # TestAnswersDice
from morpion import Morpion # TestAnswersTTT
import random

THAT="UCB"

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
        self.jeu = Matches(13)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu, nbSim=1)

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

class TestAnswersMatches(unittest.TestCase):
    """ check that 'THAT' can find good answers in some cases """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.jeu = Matches(7, False)
        self.sims = (10, 50, 100)

    @patch('builtins.print')
    def test_decision(self, mock_prn):
        """ decision for game Matches """
        for _ in self.sims:
            with self.subTest(nbSim=_):
                o = self.K('x', self.jeu, nbSim=_)
                o.who_am_i = self.jeu.turn # 1st player
                for nbm in range(2, 5):
                    _choice = o.decision( (nbm, 2) )
                    self.assertTrue(_choice == nbm-1,
                                    "with {} expecting {} found {}"
                                    "".format(nbm, nbm-1, _choice))

    @patch('builtins.print')
    def test_bad_decision(self, mock_prn):
        """ decision for game Matches should fail when no sims allowed """
        o = self.K('x', self.jeu, nbSim=0)
        o.who_am_i = self.jeu.turn # 1st player
        for nbm in range(2, 5):
            _choice = o.decision( (nbm, 2) )
            self.assertTrue(_choice is None,
                            "with {} expecting {} found {}"
                            "".format(nbm, None, _choice))
                
class TestAnswersDice(unittest.TestCase):
    """ check that 'THAT' can find good answers in some cases """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.sims = (10, 50, 100)
        self.jeu = Dice(8,6)
        
    @patch('builtins.print')
    def test_decision(self, mock_prn):
        """ decision for game Dice """
        for _ in self.sims:
            o = self.K('x', self.jeu, nbSim=_)
            o.who_am_i = self.jeu.turn # 1st player
            with self.subTest(nbSim=_):
                for nbm in range(2, 6):
                    with self.subTest(cpt=nbm):
                        _choice = o.decision( ((nbm,6),2) )
                        self.assertTrue(_choice == nbm,
                                        "expecting {} found {}"
                                        "".format(nbm, _choice))
    @patch('builtins.print')
    def test_bad_decision(self, mock_prn):
        """ decision for game Dice with no Sim allowed """
        o = self.K('x', self.jeu, nbSim=0)
        o.who_am_i = self.jeu.turn # 1st player
        for nbm in range(2, 6):
            with self.subTest(cpt=nbm):
                _choice = o.decision( ((nbm,6),2) )
                self.assertTrue(_choice is None,
                                "expecting {} found {}"
                                "".format(None, _choice))

class TestAnswersBoxes(unittest.TestCase):
    """ find the best action for boxes """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.sims = (10, 50, 100)

    @patch('builtins.print')    
    def test_split(self, mock_prn):
        """ force next move to a win Divide """
        jeu = Divide(7,17)
        _s = (3,4), 4
        for _ in self.sims:
            with self.subTest(nbSim=_):
                o = self.K('x', jeu, nbSim=_)
                o.who_am_i = jeu.turn
                _0 = o.decision(_s)
                self.assertEqual(_0, o.game.actions[0],
                                 "wrong choice {}".format(_0))
    @patch('builtins.print')    
    def test_cant_split(self, mock_prn):
        """ force None if nbSim==0 """
        jeu = Divide(7,17)
        _s = (3,4), 4
        o = self.K('x', jeu, nbSim=0)
        o.who_am_i = jeu.turn
        _0 = o.decision(_s)
        self.assertIsNone(_0, "wrong choice {}, expect None".format(_0))
                        
class TestAnswersTTT(unittest.TestCase):
    """ check that 'THAT' can find good answers in some cases """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.jeu = Morpion()
        self.sims = (10, 50, 100)

    @patch('builtins.print')
    def test_defence(self, mock_prn):
        """ decision for game TicTacToe """
        for _ in self.sims:
            with self.subTest(nbSim=_):
                o = self.K('x', self.jeu, nbSim=_)
                o.who_am_i = self.jeu.turn # 1st player
                _state = "XOX.OX..O",6
                _choice = o.decision( _state )
                _1 = o.game.actions[-1]
                self.assertTrue(_choice == _1,
                                "expecting {} found {}"
                                "".format(_1, _choice))

class TestMorpion(unittest.TestCase):
    """ do we find the best move for Morpion """
    def setUp(self):
        klass = THAT
        chk.check_class(tp, klass)
        self.jeu = Morpion(5) # à définir
        self.K = getattr(tp, klass)
        self.sims = (10, 50, 100)
        
    @patch('builtins.print')    
    def test_attak(self, mock_prn):
        """ find the winning play """
        _0 = '.'*5+"..XO."*3+'.'*5, 6
        for _ in self.sims:
            random.seed(42)
            _rep = []
            with self.subTest(nbSim=_):
                o = self.K('x', self.jeu, nbSim=_)
                o.who_am_i = self.jeu.turn
                jeu = o.game
                _rep.append(o.decision(_0))
                _val = [_rep[0] == x for x in _rep ]
                self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
                _1 = jeu.actions[2][1]
                self.assertEqual(_rep[0][1], _1,
                         "expected col {}, found {}".format(_1, _rep[0][1]))

    @patch('builtins.print')    
    def test_defence(self, mock_prn):
        """ find the key play """
        _0 = "X..O."+"."*5+"..XO."*2+'.'*5, 6
        for _ in self.sims:
            random.seed(42)
            _rep = []
            with self.subTest(nbSim=_):
                o = self.K('x', self.jeu, nbSim=_)

                o.who_am_i = self.jeu.turn
                jeu = o.game
                _rep.append(o.decision(_0))
                _val = [_rep[0] == x for x in _rep ]
                self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
                _1 = jeu.actions[6]
                self.assertEqual(_rep[0], _1,
                         "expected {}, found {}".format(_1, _rep[0]))

    
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass, TestDefault, TestAnswersMatches,
               TestAnswersBoxes, TestAnswersDice, TestAnswersTTT, TestMorpion)
    
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
    



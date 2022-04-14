#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "01.04.21"
__usage__ = "Project 2022: tests jalon 03: UCT"
__update__ = "13.04.22"

import os
import unittest
from unittest.mock import patch
from  tools import checkTools as chk
from allumettes import Matches # TestAnswersMatches
from divide_left import Divide # TestAnswersBoxes
from dice import Dice # TestAnswersDice
from morpion import Morpion # TestAnswersTTT
import random
import math # subtest_policy

"""
The tests are similar to UCB/Randy_MC, since we use pf=1
TestPrivacy contains a test_memory similar to NegAlphaBeta_Memory
TestMemory is UCT specific
"""

THAT="UCT"

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

    def test_memory(self):
        """ one expects to find memory """
        klass = THAT
        player = "Player"
        chk.check_class(tp, player)
        chk.check_class(tp, klass)
        _d = getattr(tp, klass).decision
        self.assertTrue(hasattr(_d, 'memory'), "memory is missing")
        self.assertIsInstance(getattr(_d, 'memory'), dict,
                              "expect a dictionnary")

class TestDefault(unittest.TestCase):
    """ check the correct default behavior of 'THAT' """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.jeu = Matches(13)
        self.K = getattr(tp, THAT)
        self.o = self.K('x', self.jeu, pf=1, nbSim=1)

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
                o = self.K('x', self.jeu, pf=1, nbSim=_)
                o.who_am_i = self.jeu.turn # 1st player
                for nbm in range(2, 5):
                    _choice = o.decision( (nbm, 2) )
                    self.assertTrue(_choice == nbm-1,
                                    "with {} expecting {} found {}"
                                    "".format(nbm, nbm-1, _choice))

    @patch('builtins.print')
    def test_bad_decision(self, mock_prn):
        """ decision for game Matches should fail when no sims allowed """
        o = self.K('x', self.jeu, pf=1, nbSim=0)
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
            o = self.K('x', self.jeu, pf=1, nbSim=_)
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
        o = self.K('x', self.jeu, pf=1, nbSim=0)
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
                o = self.K('x', jeu, pf=1, nbSim=_)
                o.who_am_i = jeu.turn
                _0 = o.decision(_s)
                self.assertEqual(_0, o.game.actions[0],
                                 "wrong choice {}".format(_0))
    @patch('builtins.print')    
    def test_cant_split(self, mock_prn):
        """ force None if nbSim==0 """
        jeu = Divide(7,17)
        _s = (3,4), 4
        o = self.K('x', jeu, pf=1, nbSim=0)
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
                o = self.K('x', self.jeu, pf=1, nbSim=_)
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
                o = self.K('x', self.jeu, pf=1, nbSim=_)
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
            random.seed(1)
            _rep = []
            with self.subTest(nbSim=_):
                o = self.K('x', self.jeu, pf=1, nbSim=_)

                o.who_am_i = self.jeu.turn
                jeu = o.game
                _rep.append(o.decision(_0))
                _val = [_rep[0] == x for x in _rep ]
                self.assertTrue(all(_val),
                        "expected the same answer {}".format(_rep[0]))
                _1 = jeu.actions[6]
                self.assertEqual(_rep[0], _1,
                         "expected {}, found {}".format(_1, _rep[0]))

class TestMemory(unittest.TestCase):
    """ Check Content of Memory """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        random.seed(42)

    def subtest_policy(self, memory:dict, action:any):
        """ given some memory, check that result is as expected """
        def utility(win, loss, draw):
            """ compute the utility value """
            _sum = win + loss + draw
            _upper = win + .5 * draw - loss
            return _upper / _sum
        _mother = sum([sum(memory[k]) for k in memory])
        _daughters = {k: (utility(*memory[k]) +
                          0.3 * math.sqrt(math.log(_mother) / sum(memory[k])))
                      for k in memory}
        _max_daughter = max(_daughters.values())
        self.assertEqual(_daughters[action], _max_daughter,
                         "action {} counters {} chosen {:.3f} < expected {:.3f}"
                         "".format(action, memory[action],
                                   _daughters[action], _max_daughter))
                         
    @patch('builtins.print')
    def test_getdecision_pf_deux(self, mock_prn):
        """ pf=2 """
        _jeu = Matches(7, False)
        self.K.decision.memory = {}
        _nbS = 100
        _matches = _jeu.state[0]
        _target = 2
        self.o = self.K('x', _jeu, pf=2, nbSim=_nbS)
        self.o.who_am_i = _jeu.turn
        _choice = self.o.decision( _jeu.state )
        _1 = self.o.decision.memory[_matches]
        self.subtest_policy(_1, _choice)
        _sum = sum([sum(_1[k]) for k in _1])
        self.assertTrue(_sum==3*2*_nbS,
                        "expecting {} found {}".format(6*_nbS, _sum))
        # this might be problematic and not very important
        self.assertTrue(_choice == _target,
                        "expecting {} found {}".format(_target, _choice))

    @patch('builtins.print')
    def test_getdecision_pf_quatre(self, mock_prn):
        """ pf=4 """

        _jeu = Matches(10, False)
        self.K.decision.memory = {}
        _nbS = 100
        _target = 2
        _matches = _jeu.state[0]
        self.o = self.K('x', _jeu, pf=4, nbSim=_nbS)
        self.o.who_am_i = _jeu.turn
        _choice = self.o.decision( _jeu.state )
        _1 = self.o.decision.memory[_matches]
        self.subtest_policy(_1, _choice)
        _sum = sum([sum(_1[k]) for k in _1])
        self.assertTrue(_sum==3*4*_nbS,
                        "expecting {} found {}\n{}".format(12*_nbS, _sum,_1))
        # this might be problematic and not very important
        self.assertTrue(_choice == _target,
                        "expecting {} found {}".format(_target, _choice))

        
    @patch('builtins.print')
    def test_getdecision_pf_twice(self, mock_prn):
        """ pf=2, cumulative effect """
        _jeu = Matches(7, False)
        self.K.decision.memory = {}
        _nbS = 500
        _target = 3
        _matches = 4
        self.o = self.K('x', _jeu, pf=2, nbSim=_nbS)
        self.o.who_am_i = _jeu.turn
        _choice = self.o.decision( (4,2) )
        _1 = self.o.decision.memory[_matches]
        self.subtest_policy(_1, _choice)
        self.assertTrue(_choice == _target,
                        "expecting {} found {}".format(_target, _choice))
        _sum = sum([sum(_1[k]) for k in _1])
        # 4: 3 choix 1: 1 choix 0: 0:choix
        self.assertTrue(_sum==4*_nbS,
                        "expecting {} found {}\n{}".format(4*_nbS, _sum,_1))
        _matches = 7
        _target = 2
        _choice = self.o.decision( (_matches, 0) )
        _1 = self.o.decision.memory[_matches]
        self.subtest_policy(_1, _choice)
        # This might be problematic
        self.assertTrue(_choice == _target,
                        "expecting {} found {}\n {}"
                        "".format(_target, _choice, _1))
        _sum = sum([sum(_1[k]) for k in _1])
        self.assertEqual(_sum, 3*2*_nbS,
                         "sum = {}, dic = {}".format(_sum, _1))

    @patch('builtins.print')
    def test_memory_preset_part1(self, mock_prn):
        """ only new simulations are propagated part I"""
        _jeu = Matches(7, False)
        # forced choice in state 7: action 2
        self.K.decision.memory = {
            6: {3:[0,0,13]},
            5: {1:[0,11,0]},
            7: {2:[100,0,0]}
            }
        _target = 2
        _nbSim = 10
        self.o = self.K('test', _jeu, pf=3, nbSim=_nbSim)
        self.o.who_am_i = _jeu.turn
        _choice = self.o.decision( _jeu.state )
        _1 = self.o.decision.memory
        self.subtest_policy(_1[7], _choice)
        self.assertEqual(_choice, _target,
                        "expecting {} found {}".format(_target, _choice))
        _sim_1 = sum(_1[7][1])
        self.assertEqual(_sim_1, sum(_1[7][3]),
                         "expect same number of simulations for actions 1 & 3")
        self.assertEqual(_sim_1, _nbSim,
                         "expect {} found {}".format(_nbSim, _sim_1))
        self.assertEqual(_1[6], {3:[0,0,13]},
                         "state 6 has been changed")
        self.assertEqual(_1[5][1], [0,11,0],
                         "state 5, action 1 has been changed")

    @patch('builtins.print')
    def test_memory_preset_part2(self, mock_prn):
        """ only new simulations are propagated part II"""
        _jeu = Matches(7, False)
        self.K.decision.memory = {
            6: {3:[0,0,13]},
            5: {1:[0,11,0]},
            7: {2:[100,0,0]}
            }
        _target = 2
        _nbSim = 10
        self.o = self.K('test', _jeu, pf=3, nbSim=_nbSim)
        self.o.who_am_i = _jeu.turn
        _choice = self.o.decision( _jeu.state )
        _1 = self.o.decision.memory
        self.assertEqual(sum([sum(_1[5][k]) for k in (2,3)]), 50,
                         "state 5, expect 50 more sims")
        _sim_2 = sum(_1[7][2]) -100 # 100 preset
        self.assertEqual(_sim_2, 50,
                         "wrong number of simulations for state 7, action 2\n"
                         "expecting 50 more, found {}".format(_sim_2))
    
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestPrivacy, TestKlass, TestDefault, TestAnswersMatches,
               TestAnswersBoxes, TestAnswersDice, TestAnswersTTT,
               TestMorpion, TestMemory)
    
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
    



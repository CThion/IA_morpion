#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "09.01.21"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__="""
valid_state for HexaPawn
"""


import os
import unittest
from unittest.mock import patch
from classes.abstract_game import Game
from  tools import checkTools as chk

THAT = 'Hexapawn'

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

class TestDefault(unittest.TestCase):
    """ control the initial state """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '.AB'
        self.o = self.K()

    def test_default(self):
        """ test default values """
        self.assertTrue(issubclass(self.K, Game),
                        "'{}' is not well defined".format(self.K))
        _latt = "nbl nbc cylindre priorite".split()
        _0 = [self.o.get_parameter(att) for att in _latt ]
        _1 = [3,3,False, False]
        for i,a in enumerate(_latt):
            with self.subTest(args=a):
                self.assertEqual(_0[i], _1[i], "wrong '{}'".format(a))

        _2 = self.K.PAWN[1]*3+self.K.PAWN[0]*3+self.K.PAWN[-1]*3
        self.assertEqual(self.o.hash_code, _2,
                         "wrong state expect '{}', found '{}'"
                         "".format(_2, self.o.hash_code))

class TestBasicSetup(unittest.TestCase):
    """ whatever size """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        self.o = self.K(4,7)
        self.state = self.K.PAWN[1]*7+self.K.PAWN[0]*14+self.K.PAWN[-1]*7

    @patch('builtins.print')
    def test_init_state(self, mock_prn):
        """ initial state is valid """
        self.assertEqual(self.o.hash_code, self.state,
                         "wrong state expect '{}', found '{}'"
                         "".format(self.state, self.o.hash_code))
        self.assertTrue( self.o.valid_state( (self.state, 0) ),
                         "Initial state is supposed to be valid")

class TestCommon(unittest.TestCase):
    """ tuple size 2 : str, int
        str good length with good data
    """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        self.o = self.K(4,7)


    def test_wrong_size(self):
        """ wrong size get False """
        self.assertTrue(hasattr(self.o, 'valid_state'),
                        "missing 'valid_state'")
        self.assertFalse(self.o.valid_state((1,)),
                         "len is 1: expect False")
        self.assertFalse(self.o.valid_state((1,2,3)),
                         "len is 3: expect False")

    def test_wrong_types(self):
        """ wrong types get False """
        self.assertTrue(hasattr(self.o, 'valid_state'),
                        "missing 'valid_state'")
        self.assertFalse(self.o.valid_state((1,"0"*28)),
                         "wrong types: expect False")
        
    def test_wrong_str(self):
        """ wrong str content """
        self.assertTrue(hasattr(self.o, 'valid_state'),
                        "missing 'valid_state'")
        _1 = "X"*7
        _0 = "."*14
        _2 = "O"*7
        self.assertFalse(self.o.valid_state((_1+_0+_2,0)),
                         "wrong content: expect False")
    def test_good_str(self):
        """ good str content """
        self.assertTrue(hasattr(self.o, 'valid_state'),
                        "missing 'valid_state'")
        _1 = "1"*7
        _0 = "0"*14
        _2 = "2"*7
        self.assertTrue(self.o.valid_state((_1+_0+_2,0)),
                         "good content: expect True")

class TestSpecific(unittest.TestCase):
    """ 
       pas plus de pions que nbc
       pas plus d'un pion dans le camp adverse
       pas à la fois un pion adverse dans chaque camp
       nombre de déplacements visibles <= compteur
    """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        self.o = self.K(5,5)

    @patch('builtins.print')
    def test_wrong_pawn(self, mock_prn):
        """ wrong number of pawns """
        _1 = "0"*5
        _2 = "22011"
        _3 = "1"*5
        _4 = '2'*5
        self.assertFalse(self.o.valid_state( (_1+_2+_1+_2+_2, 16) ),
                         "expect False 6 pawns / player")
        self.assertFalse(self.o.valid_state( (_1+_3+_1+_3+_1, 16) ),
                         "expect False 10/0")
        self.assertFalse(self.o.valid_state( (_1+_4+_1+_4+_1, 16) ),
                         "expect False 0/10")
        
    @patch('builtins.print')
    def test_good_pawn(self, mock_prn):
        """ good number of pawns """
        _1 = "0"*5
        _2 = "22011"
        _3 = "1"*5
        _4 = '2'*5
        self.assertTrue(self.o.valid_state( (_1+_2+_1+_2+_1, 16) ),
                         "expect True 4 pawns / player")

    @patch('builtins.print')
    def test_wrong_promotion1(self, mock_prn):
        """ 2 promotions for the same player """
        _1 = "0"*5
        _up = "12121"
        self.assertFalse( self.o.valid_state( (_up+_1*4, 10) ),
                          "wrong number on the first raw")
        self.assertFalse( self.o.valid_state( (_1*4+_up, 10) ),
                          "wrong number on the last raw")

    @patch('builtins.print')
    def test_wrong_promotion1(self, mock_prn):
        """ 1 promotion for both players """
        _1 = "0"*5
        _up = "12000"
        self.assertFalse( self.o.valid_state( (_up+_1*3+_up, 10) ),
                          "wrong number on the first & last raws")

    @patch('builtins.print')
    def test_good_promotion(self, mock_prn):
        """ one promotion for one player """
        _1 = "0"*5
        _up = "12000"
        self.assertTrue( self.o.valid_state( (_up+_1*4, 10) ),
                          "one promotion on the first raw")
        self.assertTrue( self.o.valid_state( (_1*4+_up, 10) ),
                          "one promotion on the last raw")
        
        
    @patch('builtins.print')
    def test_good_steps(self, mock_prn):
        """ steps' guess are well defined """
        _0 = "0"*5
        _1 = "10000"
        _2 = "00002"
        _3 = "10002"
        self.assertTrue( self.o.valid_state( (_2+_0*4, 8) ),
                         "guess 8 steps")
        self.assertTrue( self.o.valid_state( (_0*4+_1, 8) ),
                         "guess 8 steps")
        self.assertTrue( self.o.valid_state( (_3+_0*4, 8) ),
                         "guess 8 steps")
        self.assertTrue( self.o.valid_state( (_0*4+_3, 8) ),
                         "guess 8 steps")

    @patch('builtins.print')
    def test_bad_steps_one_pawn(self, mock_prn):
        """ bad steps' guess for one visible pawn """
        _0 = "0"*5
        _1 = "10000"
        _2 = "00002"
        self.assertTrue( self.o.valid_state( (_1+_0*4, 2) ),
                         "minimal guess: 2 steps")
        self.assertTrue( self.o.valid_state( (_0*4+_2, 2) ),
                         "minimal guess: 2 steps")
        self.assertTrue( self.o.valid_state( (_1+_0*3+_2, 2) ),
                         "minimal guess: 2 steps")

    @patch('builtins.print')
    def test_bad_steps_pawn(self, mock_prn):
        """ this case is not detected """
        _up = "11010"
        _down = "00222"
        _1 = "00101"
        _2 = "00022"
        _0 = "0"*5
        _ = _up + _1 + _0 + _2 + _down, 2+2
        self.assertTrue(self.o.valid_state( _ ),
                        "bad moves are not detected")
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestDefault, TestBasicSetup, TestCommon, TestSpecific)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

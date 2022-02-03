#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__date__ = "09.01.21"
__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__usage__="""
valid_state for Morpion
"""


import os
import unittest
import random
from unittest.mock import patch
from classes.abstract_game import Game
from  tools import checkTools as chk

THAT = 'Morpion'

def mock_prn(*args, **kargs):
    """ no output allowed """
    pass

class TestDefault(unittest.TestCase):
    """ control the initial state """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = ' AB'
        self.o = self.K()

    def test_default(self):
        """ test default values """
        self.assertTrue(issubclass(self.K, Game),
                        "'{}' is not well defined".format(self.K))
        _latt = "nbl nbc tore phase pierres".split()
        _0 = [self.o.get_parameter(att) for att in _latt ]
        _1 = [3,3,False,0,8]
        for i,a in enumerate(_latt):
            with self.subTest(args=a):
                self.assertEqual(_0[i], _1[i], "wrong '{}'".format(a))

        _2 = self.K.PAWN[0]*9
        self.assertEqual(self.o.hash_code, _2,
                         "wrong state expect '{}', found '{}'"
                         "".format(_2, self.o.hash_code))
        
class TestBasicSetup(unittest.TestCase):
    """ whatever size """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        self.o = self.K(7)
        self.state = self.K.PAWN[0]*49
        
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
        self.o = self.K(7)


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
        _0 = "."*49

        self.assertFalse(self.o.valid_state((_0,0)),
                         "wrong content: expect False")
        _0 = "."+"0"*48
        self.assertFalse(self.o.valid_state((_0,0)),
                         "partially wrong content: expect False")
        
    def test_good_str(self):
        """ good str content """
        self.assertTrue(hasattr(self.o, 'valid_state'),
                        "missing 'valid_state'")

        _0 = "0"*49

        self.assertTrue(self.o.valid_state((_0,0)),
                         "good content: expect True")

class TestSpecific(unittest.TestCase):
    """ 
       Le nombre de pions présents est compatible avec l'entier
       Le joueur 1 a exactement 0 ou 1 pion de plus que le joueur 2
       En phase 0, on ne dépasse pas les pierres
       En phase non 0, on ne dépasse pas pierres +2*nbl
    """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        random.seed(42)

    @patch('builtins.print')
    def test_pawns_vs_int(self, mock_prn):
        """ check that int is correct """
        _s = "012012"
        for k in (3, 5, 7):
            self.o = self.K(k)
            with self.subTest(size=k):
                _s = "0"*2+_s+"0"*(k*k - 2 - len(_s))
                self.assertTrue(self.o.valid_state( (_s, 4) ),
                        "expect True")
                for _ in range(k):
                    if _ == 4: continue
                    self.assertFalse(self.o.valid_state((_s, _)),
                                     "expect False")

    def make_state(self, ch:str, x:int, y:int, sz:int) -> tuple:
        """ build a random state """
        _p = random.sample( range(sz), x+y )
        _s = [ ch[0] for _ in range(sz) ]
        for _ in range(x): _s[_p[_]] = ch[1]
        for _ in range(y): _s[_p[x+_]] = ch[-1]
        return ''.join(_s), x+y

    def make_nowin(self, alphabet:str, nl:int) -> tuple:
        """ build neutral full board of nl rows """
        _ = {3:  [1, 2, 1,
                  2, 1, 0,
                  2, 1, 2,],
             5:  [1, 2, 1, 2, 1,
                  2, 1, 2, 1, 2,
                  2, 1, 2, 1, 2,
                  1, 2, 1, 2, 1,
                  1, 1, 2, 2, 0,],
             7: [1,2,1,2,1,2,1,
                 1,2,1,2,1,2,1,
                 2,1,2,1,2,1,2,
                 2,1,2,1,2,1,2,
                 2,1,2,1,2,1,2,
                 1,2,1,2,1,2,1,
                 0,1,2,1,2,1,2],}
        return ''.join([alphabet[x] for x in _[nl]]), (nl*nl -1)
    
    @patch('builtins.print')
    def test_bad_pawns(self, mock_prn):
        """ check that J1 and J2 played when needed """
        for k in (3, 5, 7):
            self.o = self.K(k)
            _0 = self.o.get_parameter('pierres') // 2
            i = random.choices(range(_0+1), k=5)
            j = random.choices(range(_0+1), k=5)
            for a,b in zip(i,j):
                _s = self.make_state(self.K.PAWN, a, b, k*k)
                with self.subTest(size=k, X=a, O=b):
                    if a in (b, b+1):
                        self.assertTrue(self.o.valid_state( _s ),
                                        "expect True {}".format(_s))
                    else:
                        self.assertFalse(self.o.valid_state( _s ),
                                          "expect False {}".format(_s))

    
    @patch('builtins.print')
    def test_phase_zero(self, mock_prn):
        """ check that upper value is rejected """
        for k in (3, 5, 7):
            self.o = self.K(k)
            _0 = self.o.get_parameter('pierres') // 2
            _s, v = self.make_state(self.K.PAWN, _0, _0, k*k)
            for i in range(1, k):
                with self.subTest(size=k, count=v+i):
                    self.assertFalse(self.o.valid_state( (_s, v+i) ),
                                     "expect False {}".format(_s))
    @patch('builtins.print')
    def test_phase_bad_non_zero(self, mock_prn):
        """ check that upper value is rejected for non zero """
        for k in (3, 5, 7):
            _p = random.choice( (1,2) )
            self.o = self.K(k, phase=_p)
            _0 = self.o.get_parameter('pierres') // 2
            _s, v = self.make_nowin(self.K.PAWN, k)
            for i in range(1, k):
                with self.subTest(size=k, count=v+i):
                    self.assertFalse(self.o.valid_state( (_s, v+2*k+i) ),
                                     "expect False {}".format(_s))
                    
    @patch('builtins.print')
    def test_phase_good_non_zero(self, mock_prn):
        """ check that below max value is accepted for non zero """
        for k in (3, 5, 7):
            _p = random.choice( (1,2) )
            self.o = self.K(k, phase=_p)
            _0 = self.o.get_parameter('pierres') // 2
            _s, v = self.make_nowin(self.K.PAWN, k)
            for i in range(k):
                with self.subTest(size=k, count=v+i):
                    self.assertTrue(self.o.valid_state( (_s, v+2*k-i) ),
                                     "expect True {}".format(_s))
                    
class TestBonus33(unittest.TestCase):
    """
       detection des cas multi-gains en 3x3
       chaque joueur n'a que 4 pierres, ne peut pas faire 2 alignements
    """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '012'
        self.o = self.K(3)

    @patch('builtins.print')
    def test_bad_row(self, mock_prn):
        """ 2 different winners in rows """
        _s = "111000222", 6
        self.assertFalse(self.o.valid_state(_s),
                         "2 winners in row: cant be")
        
    @patch('builtins.print')
    def test_bad_col(self, mock_prn):
        """ 2 different winners in columns """
        _s = "102"*3, 6
        self.assertFalse(self.o.valid_state(_s),
                         "2 winners in col: cant be")

class TestBonus55(unittest.TestCase):
    """
       detection des cas multi-gains en 5x5
    """
    def setUp(self):
        chk.check_class(tp, THAT)
        self.K = getattr(tp, THAT)
        self.K.PAWN = '.XO'
        self.o = self.K(5)

    @patch('builtins.print')
    def test_bad_row_classic(self, mock_prn):
        """ 2 different winners in rows """
        _s = "OOOO."+"."*15+".XXXX", 8
        self.assertFalse(self.o.valid_state(_s),
                         "2 winners in row: cant be")

    #@patch('builtins.print')
    def test_bad_same_win(self):#, mock_prn):
        """ same winner 2 rows or cols tore or not """
        _s = "XXOXX"+"O.O.O"+"XXXX."+"."*5+"O.O.O", 15

        self.assertTrue(self.o.valid_state(_s),
                         "1 winner in row: ok")
        _1 = self.K(5, True)
        self.assertFalse(_1.valid_state(_s),
                         "2 wins in row: cant be")
        
        _s = "XO..O"+"X.X.."+"OOX.O"+"X.X.."+"XOX.O", 15

        self.assertTrue(self.o.valid_state(_s),
                         "1 winner in col: ok")
        self.assertFalse(_1.valid_state(_s),
                         "2 wins in col: cant be")
        
    @patch('builtins.print')
    def test_bad_row_tore(self, mock_prn):
        """ 2 different winners in rows """
        _s = "OOXOO" + "..X.." + "."*10 + "XXXOX", 11
        _1 = self.K(5, tore=True)
        self.assertFalse(_1.valid_state(_s),
                         "2 winners in row: cant be")
    @patch('builtins.print')
    def test_bad_col_classic(self, mock_prn):
        """ 2 different winners in columns """
        _s = "OX..."*4+"."*5, 8

        self.assertFalse(self.o.valid_state(_s),
                         "2 winners in col: cant be")
        
    @patch('builtins.print')
    def test_bad_col_tore(self, mock_prn):
        """ 2 different winners in columns """
        _s = "O.X.."*2+"X"+"."*4+"O.X.."*2, 9
        _1 = self.K(5, tore=True)
        self.assertFalse(_1.valid_state(_s),
                         "2 winners in col: cant be")
        
    @patch('builtins.print')
    def test_bad_win(self, mock_prn):
        """ 2 different winners in columns and diag """
        _s = "XOXXO.OX...X...OOX...O..X", 13
        _1 = self.K(5, tore=True)
        self.assertFalse(_1.valid_state(_s),
                         "2 winners O in col, X in diag: cant be")
        
def suite(fname):
    """ permet de récupérer les tests à passer avec l'import dynamique """
    global tp
    klasses = (TestDefault, TestBasicSetup, TestCommon, TestSpecific,
               TestBonus33, TestBonus55)
    
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    sweet = unittest.TestSuite()
    for klass_t in klasses:
        sweet.addTest(unittest.makeSuite(klass_t))
    return sweet

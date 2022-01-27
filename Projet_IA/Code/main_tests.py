#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

__author__ = "mmc <marc-michel dot corsini at u-bordeaux dot fr>"
__date__ = "10.01.20"
__usage__ = "Test loader pour le projet 2021/2022"
__update__ = "20.01.22 11h"

import os
import sys
import unittest
from tools.checkTools import *


#===== tests import, will grow ==========#
try:
    from tests import test_state_hexapawn
except Exception as _e:
    print(_e, "failed test_state_hexapawn")
    pass
try:
    from tests import test_state_morpion
except Exception as _e:
    print(_e, "failed test_state_morpion")
    pass
try:
    from tests import test_randy
except Exception as _e:
    print("failed test_randy")
    pass
try:
    from tests import test_human
except Exception as _e:
    print("failed test_human")
    pass
try:
    from tests import test_minmax
except Exception as _e:
    print("failed test_minmax")
    pass
try:
    from tests import test_negamax
except Exception as _e:
    print("failed test_negamax")
    pass
try:
    from tests import test_alphabeta
except Exception as _e:
    print("failed test_alphabeta")
    pass
try:
    from tests import test_negalpha
except Exception as _e:
    print("failed test_negalpha")
    pass
try:
    from tests import test_negalpha_mem
except Exception as _e:
    print("failed test_negalpha_mem")
    pass
try:
    from tests import test_iterative
except Exception as _e:
    print("failed test_iterative")
    pass
try:
    from tests import test_randy_mc
except Exception as _e:
    print("failed test_randy_mc")
    pass
try:
    from tests import test_ucb
except Exception as _e:
    print("failed test_ucb")
    pass
try:
    from tests import test_uct
except Exception as _e:
    print("failed test_uct")
    pass
try:
    from tests import test_negalpha_mc
except Exception as _e:
    print("failed test_negalpha_mc")
    pass
#================================ unittest area ========================#
def suite_me(fname, toTest):
    if not hasattr(toTest, '__iter__'): raise TypeError("go to Hell !")
    print("Vous avez {} série(s) à passer".format(len(toTest)))
    try:
        tp = __import__(fname)
    except Exception as _e:
        print(_e)
    suite = unittest.TestSuite()
    for test_me in toTest:
        try:
            suite.addTest(test_me.suite(fname))
        except Exception as _e:
            print(_e)
            
    return suite

if __name__ == '__main__':

    if len(sys.argv) == 1:
        param = input("quel est le fichier à traiter ? ")
        if not os.path.isfile(param): ValueError("need a python file")
    else: param = sys.argv[1]

    target = param.split('.')[0]

    _out = check_property(target != '','acces au fichier')
    print("tentative de lecture de {}".format(target))
    try:
        tp = __import__(target) # revient à faire import XXX as tp
    except Exception as _e:
        print(_e)
        sys.exit(-1)

        
    _yes = "oO0Yy"
    _todo = []
    _submenu = { '1': ("hexapawn morpion",
                       [test_state_hexapawn, test_state_morpion]),
                 '2': ("randy human minmax negamax alphabeta alphabeta_negamax",
                       []),
                       #[test_randy, test_human, test_minmax,
                       # test_negamax, test_alphabeta, test_negalpha]),
                 '3':("alphabeta_memory iterative_deepening randy_mc ucb uct"
                      " negamax_mc",
                      [])
                      #[test_negalpha_mem, test_iterative, test_randy_mc,
                      # test_ucb, test_uct, test_negalpha_mc])
                      }
    _all = None
    print("select wich subtests you want")
    print("Pour répondre par oui, utiliser l'un des symboles '{}'"
          "".format(_yes))
    _choices = ['all']
    _choices.extend(sorted(_submenu.keys()))
    for key in _choices:
        _msg = ("Passer tous les tests ? " if key == "all"
                else "Tests du jalon 0{} ? ".format(key))
        if key == "all":
                _ = input(_msg)
                if len(_) >=1 and _[0] in _yes:
                    for k in _submenu: _todo.extend(_submenu[k][1])
                    break # sortie
        else:
            _ = input(_msg)
            if len(_) >=1 and _[0] in _yes:
                _names, _modules = _submenu[key]
                for n,x in zip(_names.split(), _modules):
                    _ = input(">>> Jalon 0{}: Test de {} ? ".format(key, n))
                    if len(_)==1 and _ in _yes:
                        _todo.append(x) ; print("{} added".format(n))
                
    unittest.TextTestRunner(verbosity=2).run(suite_me(target, _todo))

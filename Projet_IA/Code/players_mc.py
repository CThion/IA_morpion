#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players of players_mc
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random
import math
from tools.outils import count
import time

def scoring(win:int, loss:int, draw:int) -> float:
    """ 
        from counters win/loss/draw makes some metrics
        return a value in [-1, 1] 
    """
    _sum = win + loss + draw
    if _sum == 0: return 0
    _upper = win + .5 * draw - loss
    _ratio = _upper / _sum
    return _ratio 
#===========INFORMATIONS================================================#
#self.game.hash_code : donne les clés du dictionnaire
#=========== les classes à mettre en oeuvre pour le jalon 03 ===========#
class NegAlphaBeta_Memory(Player): #optionnel 2
  """
  Implémentation similaires à celle de Negamax avec MinMax ;
  Regrouper coupe_alpha et coupe_beta en 1 seul coupe_alpha qui appelle -coupe_alpha
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    pf = self.get_value('pf')
    alpha = -101 
    beta = 101  
    liste_vi=[]
    #--
    for a_i in self.game.actions:   
      #--changement d'état
      self.game.move(a_i)
      #--Etape 4
      key = self.game.hash_code #Etape 4 - 1)
      if key not in self.decision.memory : pass #Etape 4 - 2)
      else: #Etape 4 _ 3)
          if self.decision.memory[key]['exact']==True:
              return self.game.actions[a_i]
          elif pf <= self.decision.memory[key]['pf']:
              return self.decision.memory[key]
              
      #--récupération informations
      v_i = self.__coupe_alpha(pf-1, alpha, beta)   
      liste_vi.append(v_i)
      #--retour à l'état précédent
      self.game.undo()
      #--traitement de l'information (sortie possible)
    #--Cas de la nouvelle partie
    maximum = liste_vi.index(max(liste_vi))
    self.decision.memory.update({self.game.hash_code : {'pf':pf, "exact":True, "score":maximum, "best_action":self.game.actions[maximum]}}) #dico
    return self.game.actions[maximum]
  # -----------------Partie Dictionnaire-----------
  decision.memory = {}
  # -----------------------------------------------
  def __coupe_alpha(self, pf, alpha, beta):
    """MIN cherche a diminuer beta"""
    if pf == 0:
      
      if self.game.over() == True:  #dans ce if, exact vaut True car on a fini la partie
        if self.who_am_i == self.game.turn :
          self.decision.memory.update({self.game.hash_code : {'pf':pf, "exact":True, "score":-self.estimation(), "best_action":None}}) #dico
          return -self.estimation()
        else:
          self.decision.memory.update({self.game.hash_code : {'pf':pf, "exact":True, "score":self.estimation(), "best_action":None}}) #dico
          return self.estimation()

      else: #dans ce else, la partie n'est pas finie, on n'a qu'une approximation donc exact vaut False
        if self.who_am_i == self.game.turn :
          self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":False, "score":-self.estimation(), "best_action":None}}) #dico
          return -self.estimation()
        else:
          self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":False, "score":self.estimation(), "best_action":None}}) #dico
          return self.estimation()

    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])
      key = self.game.hash_code #Etape 4 - 1)
      if key not in self.decision.memory : pass #Etape 4 - 2)
      else: #Etape 4 _ 3)
          if self.decision.memory[key]['exact']==True:
              return self.decision.memory[key]['score']
      v_i = -self.__coupe_alpha(pf-1, -beta,-alpha) 
      
      if v_i <= alpha:
        if self.decision.memory[self.game.hash_code]["exact"]==True:
          self.game.undo()
          self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":True, "score":alpha, "best_action":None}}) #dico
          return alpha
        else:
          self.game.undo()
          self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":False, "score":alpha, "best_action":None}}) #dico
        return alpha
      beta = min(beta, v_i)
      i = i+1
      if self.decision.memory[self.game.hash_code]["exact"]==True:
        self.game.undo()
        self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":True, "score":beta, "best_action":None}}) #dico
      else:
        self.game.undo()
        self.decision.memory.update({self.game.hash_code:{'pf':pf, "exact":False, "score":beta, "best_action":None}}) #dico
    return beta
    
#====================== exemples de code test ==========================#
def usage():
    print("""
> test_clever(cls)
  prend en paramètre une classe n'ayant besoin que de pf
> test_morpion(cls)
  prend en paramètre une classe ayant besoin de pf ou nbSim
  prend en paramètre une classe ayant besoin de pf et secondes
> test_hexapawn(cls)
  prend en paramètre une classe ayant besoin de pf ou nbSim
  prend en paramètre une classe ayant besoin de pf et secondes
""")
    
def test_clever(joueur):
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
jeu.state == (13, 0) # on attend True au test

moi = joueur('toto', jeu, pf=3)
moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 3 # on attend True au test
jeu.state == (3, 4) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
jeu.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 2 # on attend True au test
jeu.state == (6, 4) # on attend True au test

jeu2 = Matches(13, False) # le but ne pas prendre la dernière allumette
moi = joueur('toto', jeu2, pf=3)
moi.who_am_i = jeu2.turn # moi est le premier joueur
moi.decision( (3, 4) ) == 2# on attend True au test
jeu2.state == (3, 4)  # on attend True au test

moi.decision( (4, 4) ) == 3 # on attend True au test
jeu2.state == (4, 4) # on attend True au test

moi.decision( (5, 4) ) == 1 # on attend True au test
jeu2.state == (5, 4) # on attend True au test

moi.decision( (6, 4) ) == 1 # on attend True au test
jeu2.state == (6, 4) # on attend True au test

from divide_left import Divide
jeu3 = Divide(7, 17)
moi = joueur('malin', jeu3, pf=3)
moi.who_am_i = jeu3.turn # moi est le premier joueur
moi.decision( ((3,4), 4) ) == ('A', 1)
jeu3.state == ((3,4), 4)
''' ; testcode(code)
    
def  test_morpion(joueur):
    code = '''
from morpion import Morpion
klass = IterativeDeepening
kargs = {'pf':43, 'secondes':2.} if joueur==klass else {'pf':3, 'nbSim': 100}
jeu = Morpion(phase=2) 
_state = "X...O..OX", 4
jeu.state = _state
print(jeu)

a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.time()
print(a.decision(_state))
_end = time.time() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)

jeu = Morpion(5)
_attack = '.'*5+"..XO."*3+'.'*5, 6
_defence = "X..O."+"."*5+"..XO."*2+'.'*5, 6

jeu.state = _attack
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.time()
print(a.decision(_attack))
_end = time.time() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_attack[0], None)

jeu.state = _defence
print(jeu)

joueur.decision.memory = {}
_start = time.time()
print(a.decision(_defence))
_end = time.time() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_defence[0], None)
''' ; testcode(code)

def  test_hexapawn(joueur):
    code = '''
from hexapawn import Hexapawn
klass = IterativeDeepening
kargs = {'pf':43, 'secondes':2} if joueur==klass else {'pf':3, 'nbSim': 100}
jeu = Hexapawn()
_state = "X.."+"O.X"+".O.",4

jeu.state = _state
print(jeu)

a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.time()
print(a.decision(_state))
_end = time.time() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)

jeu = Hexapawn(4,3)
_state = "X.X.X.O...OO", 2
jeu.state = _state
print(jeu)

joueur.decision.memory = {}
a = joueur('a', jeu, **kargs)
a.who_am_i = jeu.turn
_start = time.time()
print(a.decision(_state))
_end = time.time() - _start
print("decision was taken in {:.03f}s".format(_end))
a.decision.memory.get(_state[0], None)
''' ; testcode(code)

if __name__ == "__main__":
    usage()

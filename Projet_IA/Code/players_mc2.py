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
        -1 = situtation défavorable
        1 = situation favorable
    """
    _sum = win + loss + draw
    if _sum == 0: return 0
    _upper = win + .5 * draw - loss
    _ratio = _upper / _sum
    return _ratio 
#===========INFORMATIONS================================================#
#self.game.hash_code : donne les clés du dictionnaire
# D = {}
# D.keys() : clefs du dictionnaire
# D.values() : toutes les valeurs du dictionnaire
# D.items() : (clef, valeur), (clef, valeur)
# 'hashable' : transformable en 1 nbre entier
#=========== les classes à mettre en oeuvre pour le jalon 03 ===========#
class NegAlphaBeta_Memory(Player): #optionnel 2
  """
  Implémentation similaires à celle de Negamax avec MinMax ;
  Regrouper coupe_alpha et coupe_beta en 1 seul coupe_alpha qui appelle -coupe_alpha
  Paramètres rattaché à chaque config de memory : 
    -- pf : la profondeur à laquelle l'état est rencontrée, c'est un entier,
    -- exact : un booléen qui indique si l'évaluation est exacte ce qui est le cas lorsque la partie
    est terminée, c'est-à-dire soit parce que on est sur une feuille avec self.game.over() est
    True, soit parce que l'information a été remontée depuis un état où l'évaluation était exacte.
    -- score : la valeur de l'évaluation
    -- best_action : l'action ayant produit le score, lorsqu'il n'y a pas d'action, parce que la
    partie est terminée, l'action sera None
  """


  def decision(self, state):
    """ the main method """
    self.game.state = state
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    #--
    beta = self.WIN+1 #-101 et 101
    alpha = -beta
    _v, _a = alpha, None
    pf = self.get_value('pf')

    #--------TEST MEMORY
    clef = self.game.hash_code
    if clef in self.decision.memory:
      memoire = self.decision.memory[clef] # clef en mémoire, récupération
      #----traitement avec éventuel arrêt
      if memoire['pf'] >= pf or memoire['exact'] == True:
        # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
        return memoire['best_action']
      else:
          pass
          #si on est ici, c'est qu'il y a un truc en memoire MAIS
          #pas suffisant pour s'arreter, on peut utiliser le score
          #on peut utiliser best_action (heuristique)
    
    #--------MEMOIRE VIDE ==> GO LES CALCULS 
    #si on est ici c'est qu'on va poursuivre la méthode normale
    
    #----sauvegarde tampon des meilleurs valeurs pour le renvoi final
    score = alpha 
    exact=False 
    best_action=None
    
    for a in self.game.actions:
      self.game.move(a)
      clef_fils = self.game.hash_code
      #ICI
      _ = - self.__cut(pf-1, alpha, beta)
      self.game.undo()
      if _ > _v:
        score = _
        exact=self.decision.memory[clef_fils]['exact']
        best_action=a
        self.decision.memory[self.game.hash_code]={'pf':pf,
                                               'exact':exact,
                                               'score':score,
                                               'best_action':best_action}          
        _v, _a = _, a
    # ICI
    self.decision.memory[self.game.hash_code]={'pf':pf,
                                           'exact':exact,
                                           'score':score,
                                           'best_action':best_action}            
    return _a
  decision.memory = {}


  def __cut(self, pf:int, alpha:float, beta:float) -> float:
    """ we use, max thus cut_beta """
    
    clef = self.game.hash_code
    
    #--------CHECK MEMORY
    if clef in self.decision.memory:
        memoire = self.decision.memory[clef] # clef en mémoire, récupération
        #--traitement avec éventuel arrêt
        if memoire['pf'] >= pf or memoire['exact'] == True: 
            return memoire['score']# arret
        #si on est ici, c’est qu’il y a un truc en memoire MAIS
        #pas suffisant pour s’arreter, on peut utiliser le score
        #on peut utiliser best_action (heuristique)
    # si on est ici c’est qu’on va poursuivre la méthode normale
    
    #--------FEUILLE
    if pf == 0 or self.game.over():
      _c = 1 if self.who_am_i == self.game.turn else -1 #coef du résultat (+1 ou -1)
      # ICI - maj
      score = _c * self.estimation() #(+100 ou -100)
      self.decision.memory[self.game.hash_code]={'pf':pf,
                                                 'exact':self.game.over,
                                                 'score':score,
                                                 'best_action':None}
      return score

    #--------PAS FEUILLE
    #----sauvegarde tampon des meilleurs valeurs
    score = alpha 
    exact=False 
    best_action=None
    
    for a in self.game.actions:
      #----CONFLIT
      if alpha >= beta:
        # ICI - on enregistre le fait qu'il ne sert à rien de jouer ce coup 
        self.decision.memory[self.game.hash_code]={'pf':pf,
                                                 'exact':self.game.over,
                                                 'score':None, #aucun score renvoyé car conflit 
                                                 'best_action':None}  
        return beta #retour niveau précédent
    
      #----PAS CONFLIT => OK
      self.game.move(a)
      clef_fils = self.game.hash_code # ICI - sauvegarde locale info fils
      _M = - self.__cut(pf-1, -beta, -alpha) # SCORE (_Mesure)
      self.game.undo()
      # ICI - maj SI meilleure valeur <=> si alpha est modifié => on retien quel fils est responsable de cette modification
      #il n'y a pas de sauvegarde dans le cas contraire !
      #Dans tous les cas, à une profondeur donnée, alpha sera forcément mis à jour au moins une fois 
      if _M > alpha:
          #--valeur tampon pour renvoi final du noeud
          score = _M
          exact=self.decision.memory[clef_fils]['exact']
          best_action=a
          #--
          self.decision.memory[self.game.hash_code]={'pf':pf,
                                                 'exact':exact,
                                                 'score':score,
                                                 'best_action':best_action}        
      alpha = max(_M, alpha)
    # ICI - mise a jour du neud : valeur finale renvoyée une fois toutes les branches fils parcourues
    self.decision.memory[self.game.hash_code]={'pf':pf,
                                                 'exact':exact,
                                                 'score':score,
                                                 'best_action':best_action}  
    return alpha
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
#klass = IterativeDeepening
kargs = {'pf':3, 'nbSim': 100}
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

    
if __name__ == "__main__":
    #testcodeCM()
    
    joueur = NegAlphaBeta_Memory
    test_morpion(joueur)
    """
    from morpion import Morpion
    #klass = IterativeDeepening
    jeu = Morpion(phase=2) 
    _state = "X...O..OX", 4
    jeu.state = _state
    #print(jeu)

    kargs = {'pf':3, 'nbSim': 100} #paramètre joueur
    a = joueur('a', jeu, **kargs)
    a.who_am_i = jeu.turn #mon tour de jouer
    a.decision(_state)
    a.decision.memory.get(_state[0], None)
    
    
    # jeu = Morpion(5)
    # _attack = '.'*5+"..XO."*3+'.'*5, 6
    # _defence = "X..O."+"."*5+"..XO."*2+'.'*5, 6
    
    # jeu.state = _attack
    # print(jeu)
    
    # joueur.decision.memory = {}
    # a = joueur('a', jeu, **kargs)
    # a.who_am_i = jeu.turn
    # _start = time.time()
    # print(a.decision(_attack))
    # _end = time.time() - _start
    # print("decision was taken in {:.03f}s".format(_end))
    # a.decision.memory.get(_attack[0], None)
    
    # jeu.state = _defence
    # print(jeu)
    
    # joueur.decision.memory = {}
    # _start = time.time()
    # print(a.decision(_defence))
    # _end = time.time() - _start
    # print("decision was taken in {:.03f}s".format(_end))
    # a.decision.memory.get(_defence[0], None)
    # ''' ; testcode(code)
"""
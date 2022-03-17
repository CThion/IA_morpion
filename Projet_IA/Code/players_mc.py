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
#=========== les classes à mettre en oeuvre pour le jalon 03 ===========#
class NegAlphaBeta_Memory(Player): #optionnel 2
  """
  Implémentation similaires à celle de Negamax avec MinMax ;
  Regrouper coupe_alpha et coupe_beta en 1 seul coupe_alpha qui appelle -coupe_alpha
  Paramètres rattaché à chaque config de memory : 
    -- pf : la profondeur à laquelle l’état est rencontrée, c’est un entier,
    -- exact : un booléen qui indique si l’évaluation est exacte ce qui est le cas lorsque la partie
    est terminée, c’est-à-dire soit parce que on est sur une feuille avec self.game.over() est
    True, soit parce que l’information a été remontée depuis un état où l’évaluation était exacte.
    -- score : la valeur de l’évaluation
    -- best_action : l’action ayant produit le score, lorsqu’il n’y a pas d’action, parce que la
    partie est terminée, l’action sera None
  """


  def decision(self, state):
    """Récupère l'état du jeu, et renvoit la meilleur décision possible
    étant donnée la profondeur de calcul et les informations en mémoire
    a_i = actions i dans self.game.actions
    v_i = valeurs attribuée à  a_i"""
    
    #--vérificaiton légitimité du joueur
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None  
  
    print(f"""
      NIVEAU DECISION = avant remember
      self.game.actions {self.game.actions}
      """)
    
    #--vérification mémoire
    alpha = -101; beta = 101
    pf = self.get_value('pf') #profondeur de calcul
    action = self.__remember(pf, alpha, beta, 'best_action') #vérification mémoire
    if action[2] !=None : 
        return action[2] #action[2] correspond à self.memory[key]['best_action']
    
    #--état totalement nouveau => calculs
    liste_vi=[] #liste des valeurs estimées des actions les plus proches
    #--parcours de toutes les actions les plus proches de la racines 
    for a_i in self.game.actions:   
      self.game.move(a_i) #changement d'état
      v_i = self.__coupe_alpha(pf-1, alpha, beta)   
      liste_vi.append(v_i)
      #--retour à l'état précédent
      self.game.undo()
    #--
    maximum = liste_vi.index(max(liste_vi)) #indice de la meilleur action
    print(f"""
          ==========================
          self.game.actions {self.game.actions}
          liste_vi {liste_vi}
          maximum {maximum}
          """)
    best_action = self.game.actions[maximum] #meilleur action
    self.__learn(pf, True, maximum, best_action)#enregistrement de ce nouvel état
    return best_action
  # -----------------Partie Dictionnaire-----------
  decision.memory = {}
  # ----------------------------
  def __remember(self, pf, alpha, beta, wishinfo):
    """Vérifie si l'état du jeu a déjà été traité dans self.memory, 
    et si oui envoi le résultat correspondant en mémoire, 
    ainsi que alpha et beta potentiellement mis à jour
    wishinfo = 'best_action' ou 'score', change selon qu'on appelle __remember
    depuis decision ou depuis cut"""

    #--Etape 4 : utilisation de la mémoire 
    res=None #résultat = None a priori
    key = self.game.hash_code #état actuel du jeu
    #--
    if key in self.decision.memory : #si état déjà rencontré
        #--si solution exacte (on sait comment gagner)
        etat = self.decision.memory[key]
        if etat['exact'] or \
        (not etat['exact'] and pf<=etat['pf']) : 
            res=etat[wishinfo]
        #--si la profondeur restante à explorer est supérieure à la profondeur de découverte de key
        else:
            print("UPDATE ALPHA BETA memory")
            alpha = max(alpha, etat['score'])
            if alpha >= beta: return beta # coupe  
        print(f"""
      AVEC remember = cas où mémoire mobilisée
      self.game.actions {self.game.actions}
      """)
    else:
        print(f"""
      SANS remember = cas où mémoire NON mobilisé
      self.game.actions {self.game.actions}
      """)
    return alpha, beta, res
  # ----------------------------
  def __learn(self, pf, exact, score, best_action):
      """Met a jour decision.memory"""
      self.decision.memory.update(
          {self.game.hash_code : {
              'pf':pf, 
              "exact":True, 
              "score":score, 
              "best_action":best_action}})
  # -----------------------------------------------
  def __coupe_alpha0(self, pf, alpha, beta):
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
      v_i = -self.__coupe_alpha0(pf-1, -beta,-alpha) 
      
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

  def __coupe_alpha(self, pf, alpha, beta):
    """MIN cherche a diminuer beta"""
    
    #--verif si état en mémoire
    alpha, beta, score = self.__remember(pf, alpha, beta, 'score') #vérification mémoire
    if score !=None : return score #si on est dans un état qu'on avait déjà trouvé avant
    
    #--bout de branche ou victoire : solution complète
    if pf == 0 or self.game.over() == True :
      if self.who_am_i == self.game.turn : 
          self.__learn(pf, True, -self.estimation(), None) #enregistrement 
          return -self.estimation()
      else : 
          self.__learn(pf, True, self.estimation(), None) #enregistrement
          return self.estimation()
    
    #--milieur de branche : solution incomplète
    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])#déplacement => changement d'état
      #--verif si nouvel état dans mémoire
      alpha, beta, score = self.__remember(pf, alpha, beta, 'score') #vérification mémoire
      if score !=None : 
          self.game.undo()
          return score #si on est dans un état qu'on avait déjà trouvé avant
      #--
      v_i = -self.__coupe_alpha(pf-1, -beta,-alpha) #chaîne récursive
      if v_i <= alpha: 
          self.__learn(pf, False, alpha, None); 
          self.game.undo()
          return alpha
      beta = min(beta, v_i)
      i = i+1
    self.__learn(pf, False, beta, None)
    self.game.undo()
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
    #test_morpion(joueur)
    
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
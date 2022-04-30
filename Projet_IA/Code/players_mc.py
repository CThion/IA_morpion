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
# D.keys() : parents du dictionnaire
# D.values() : toutes les valeurs du dictionnaire
# D.items() : (parent, valeur), (parent, valeur)
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
    beta = self.WIN+1
    alpha = -beta
    score, b_a = alpha, None
    pf = self.get_value('pf')
    #--------TEST MEMORY
    parent = self.game.hash_code
    L_a = self.game.actions
    if parent in self.decision.memory:
      memoire = self.decision.memory[parent] # parent en mémoire, récupération
      #----traitement avec éventuel arrêt
      if memoire['exact']: return memoire['best_action']
      if memoire['pf'] >= pf:
        # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
        return memoire['best_action']
      alpha=max(alpha, memoire["score"])
      if alpha>=beta: memoire['pf']=pf; return memoire['best_action']
      else:
          L_a = list(self.game.actions) #liste des actions
          id_a = L_a.index(memoire['best_action'])
          L_a.pop(id_a) #mets le b_a en première position
          L_a.insert(0,memoire['best_action'])
          L_a = tuple(L_a)
    #--------MEMOIRE VIDE ou PAS INTERESSANTE ==> GO LES CALCULS 
    #si on est ici c'est qu'on va poursuivre la méthode normale    
    for a in L_a:
      self.game.move(a)
      parent_fils = self.game.hash_code
      #ICI
      _v_new = - self.__cut(pf-1, alpha, beta)
      self.game.undo()
      if _v_new > score:
        score, b_a = _v_new, a
        score = _v_new
        exact=self.decision.memory[parent_fils]['exact']
    # ICI
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':b_a}            
    return b_a
  decision.memory = {}
  # ----
  def __cut(self, pf:int, alpha:float, beta:float) -> float:
    """ we use, max thus cut_beta """
    parent = self.game.hash_code
    #--------CHECK MEMORY
    if parent in self.decision.memory:
        memoire = self.decision.memory[parent] # parent en mémoire, récupération
        #----traitement avec éventuel arrêt
        if memoire['exact']: return memoire['score']
        if memoire['pf'] >= pf:
          # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
          return memoire['score']
        alpha=max(alpha, memoire["score"])
        if alpha>=beta: self.decision.memory[parent]['pf']=pf; return memoire['score']
    #--------FEUILLE
    if pf == 0 or self.game.over():
      _c = 1 if self.who_am_i == self.game.turn else -1 #coef du résultat (+1 ou -1)
      # ICI - maj
      score = _c * self.estimation() #(+100 ou -100)
      self.decision.memory[parent]={'pf':pf,
                                  'exact':self.game.over(),
                                  'score':score,
                                  'best_action':None}
      return score
    #--------PAS FEUILLE
    score=-(self.WIN+1)
    exact=False
    best_action=None
    for a in self.game.actions:
      #----CONFLIT
      if alpha >= beta:
        # ICI - on enregistre le fait qu'il ne sert à rien de jouer ce coup 
        self.decision.memory[parent]={'pf':pf,
                                    'exact':exact,
                                    'score':score, #aucun score renvoyé car conflit 
                                    'best_action':best_action} 
        return beta #retour niveau précédent
      #----PAS CONFLIT => OK
      self.game.move(a)
      parent_fils = self.game.hash_code # ICI - sauvegarde locale info fils
      _M = - self.__cut(pf-1, -beta, -alpha) # SCORE (_Mesure)
      self.game.undo()
      # ICI - maj SI meilleure valeur <=> si alpha est modifié => on retien quel fils est responsable de cette modification
      #il n'y a pas de sauvegarde dans le cas contraire !
      #Dans tous les cas, à une profondeur donnée, alpha sera forcément mis à jour au moins une fois 
      if _M > score: #Il faut intialiser par une variable différente de alpha qui sera égale à -1000 (sinon au niveau de la boucle la comparaison sera tjr avec alpha)
          #--valeur tampon pour renvoi final du noeud 
          score=_M
          exact=self.decision.memory[parent_fils]['exact']
          best_action=a
      alpha = max(_M, score)            
    # ICI - mise a jour du neud : valeur finale renvoyée une fois toutes les branches fils parcourues
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':best_action}  
    return score
#===============================================================================#

class IterativeDeepening(Player): #optionnel 2
  """L'objectif de cette classe est de 'muscler' notre base de donnée (memory)
  Concrêtement, iterativeDeepening :
      - renvoit exactement le même résultat que NegAlphaBeta_Memory
      - est moins rapide que NegAlphaBeta_Memory
      - modifie davantage la mémoire car ne se permet pas d'avoir des résultats
      inexacts => va parcourir quand même toutes les possibilités !
  L'idée ici est donc de décomposer notre IA en deux phases : une première phase
  d'apprentissage ou elle utilisera IterativeDeepening pour construire une mémoire
  conséquente, puis une phase d'exploitation ou on va passer par NegAlphaBeta_Memory 
  qui est plus rapide et aura juste à utiliser la mémoire déjà pré-construite"""
  
  def decision(self, state):
      self.game.state = state
      if self.game.turn != self.who_am_i:
          print("not my turn to play")
          return None
      # the parameters to retrieve
      pf = self.get_value('pf')
      second = self.get_value('secondes')
      depth = 1
      # alpha , beta
      _bound = self.WIN +1
      _start = time.time()
      #_a=0
      while depth <= pf and time.time() - _start < second:
          _a = self.__old_decision(depth , -_bound , +_bound)
          # print("elapsed {:.2f} depth = {}"
          # "".format(time.time() - _start , depth))
          depth += 1
      return _a
  

  def __old_decision(self,pf:int,alpha:float,beta:float):
    """ the main method 
    """     
    score = alpha
    parent = self.game.hash_code
    for a in self.game.actions:
      self.game.move(a)
      parent_fils = self.game.hash_code
      _v_new = - self.__cut(pf-1, alpha, beta)
      self.game.undo()
      if _v_new > score:
        score, b_a = _v_new, a
        score = _v_new
        exact=self.decision.memory[parent_fils]['exact']
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':b_a}            
    return b_a
  decision.memory = {}
  #--

  def __cut(self, pf:int, alpha:float, beta:float) -> float:
    """ we use, max thus cut_beta """
    parent = self.game.hash_code
    #--------CHECK MEMORY
    if parent in self.decision.memory:
        memoire = self.decision.memory[parent] # parent en mémoire, récupération
        #----traitement avec éventuel arrêt
        if memoire['exact']: return memoire['score']
        if memoire['pf'] >= pf:
          # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
          return memoire['score']
        alpha=max(alpha, memoire["score"])
        if alpha>=beta: self.decision.memory[parent]['pf']=pf; return memoire['score']
    #--------FEUILLE
    if pf == 0 or self.game.over():
      _c = 1 if self.who_am_i == self.game.turn else -1 #coef du résultat (+1 ou -1)
      score = _c * self.estimation() #(+100 ou -100)
      self.decision.memory[parent]={'pf':pf,
                                  'exact':self.game.over(),
                                  'score':score,
                                  'best_action':None}
      return score
    #--------PAS FEUILLE
    score=-(self.WIN+1)
    exact=False
    best_action=None
    
    for a in self.game.actions:
      #----CONFLIT
      if alpha >= beta:
        # ICI - on enregistre le fait qu'il ne sert à rien de jouer ce coup 
        self.decision.memory[parent]={'pf':pf,
                                    'exact':exact,
                                    'score':score, #aucun score renvoyé car conflit 
                                    'best_action':best_action} 
        return beta #retour niveau précédent
    
      #----PAS CONFLIT => OK
      self.game.move(a)
      parent_fils = self.game.hash_code # ICI - sauvegarde locale info fils
      _M = - self.__cut(pf-1, -beta, -alpha) # SCORE (_Mesure)
      self.game.undo()
      # ICI - maj SI meilleure valeur <=> si alpha est modifié => on retien quel fils est responsable de cette modification
      #il n'y a pas de sauvegarde dans le cas contraire !
      #Dans tous les cas, à une profondeur donnée, alpha sera forcément mis à jour au moins une fois 
      if _M > score: #Il faut intialiser par une variable différente de alpha qui sera égale à -1000 (sinon au niveau de la boucle la comparaison sera tjr avec alpha)
          #--valeur tampon pour renvoi final du noeud 
          score=_M
          exact=self.decision.memory[parent_fils]['exact']
          best_action=a
      alpha = max(_M, score)            
    # ICI - mise a jour du neud : valeur finale renvoyée une fois toutes les branches fils parcourues
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':best_action}  
    return score    
#=======================================================================
class Randy_MC(Player):
    """
    Randy avec approche Monte-Carlo
    """
    def decision(self, state):
        """ get the state """
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None

        nbSim = self.get_value('nbSim')
        print("nbsim : ", nbSim)
        if nbSim < 1 : return None
        best_score = -10
        best_action = None
        # description algorithmique
        for a in self.game.actions :
            self.game.move(a)
            win, loss , draw = self.simulation(nbSim)
            self.game.undo()
            score = (win-loss + 0.5*draw)/(win+loss+draw)
            if best_action == None or score > best_score:
                best_score = score
                best_action = a
        return best_action
#=======================================================================
class NegAlphaBeta_MC(Player): 
  """
  NegAlphaBeta avec Approche Monte-Carlo
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    pf = self.get_value('pf') #on récupère la profondeur
    alpha = -101 #alpha et beta ne sont pas choisies par l'utilisateur
    beta = 101  #  +- self.WIN +-1 (aide_jalon_02 p11)
    liste_vi=[]
    #--
    for a_i in self.game.actions:   #pour chaque action
      #--changement d'état
      self.game.move(a_i)           #j'avance sur l'une des actions disponible
      #--récupération informations
      v_i = self.__coupe_alpha(pf-1, alpha, beta)   
      liste_vi.append(v_i)
      #--retour à l'état précédent
      self.game.undo()
      #--traitement de l'information (sortie possible)
    #--
    maximum = liste_vi.index(max(liste_vi))
    return self.game.actions[maximum]
  # -----------------------------------------------
  def __coupe_alpha(self, pf, alpha, beta):
    """MIN cherche a diminuer beta"""
    nbSim = self.get_value('nbSim')
    if self.game.over() == True :
      if self.who_am_i == self.game.turn : return -self.estimation()
      else : return self.estimation()
    if pf == 0:
        if self.who_am_i == self.game.turn :
            win, loss, draw = self.simulation(nbSim,False)
            return self.WIN * scoring(win,loss,draw)
        else :
            win, loss, draw = self.simulation(nbSim)
            return self.WIN * scoring(win,loss,draw)
        
    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])
      v_i = -self.__coupe_alpha(pf-1, -beta,-alpha) #chaîne récursive
      self.game.undo()
      if v_i <= alpha: return alpha
      beta = min(beta, v_i)
      i = i+1
    return beta
#=======================================================================
class NegAlphaBeta_Memory_MC(Player): #1 FAIL A CORRIGER
  """
  Ajout d'une mémoire à NegAlphaBeta_MC
  """


  def decision(self, state):
    """ the main method """
    self.game.state = state
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    beta = self.WIN+1
    alpha = -beta
    score, b_a = alpha, None
    pf = self.get_value('pf')
    #--------TEST MEMORY
    parent = self.game.hash_code
    if parent in self.decision.memory:
      memoire = self.decision.memory[parent] # parent en mémoire, récupération
      #----traitement avec éventuel arrêt
      if memoire['exact']: return memoire['best_action']
      if memoire['pf'] >= pf:
        # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
        return memoire['best_action']
      alpha=max(alpha, memoire["score"])
      if alpha>=beta: memoire['pf']=pf; return memoire['best_action']
      else:
          b_a = memoire["best_action"] #best_cation que l'on avait déjà trouvé par le passé (en mémoire)
          L_a = list(self.game.actions) #liste des actions
          id_a = L_a.index(b_a)
          L_a.insert(0, L_a.pop(id_a)) #mets le b_a en première position

    
    #--------MEMOIRE VIDE ou PAS INTERESSANTE ==> GO LES CALCULS 
    #si on est ici c'est qu'on va poursuivre la méthode normale    
    for a in self.game.actions:
      self.game.move(a)
      parent_fils = self.game.hash_code
      #ICI
      _v_new = - self.__cut(pf-1, alpha, beta)
      print(_v_new)
      self.game.undo()
      if _v_new > score:
        score, b_a = _v_new, a
        score = _v_new
        exact=self.decision.memory[parent_fils]['exact']
    # ICI
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':b_a}            
    return b_a
  decision.memory = {}


  def __cut(self, pf:int, alpha:float, beta:float) -> float:
    """ we use, max thus cut_beta """
    print("---------")
    
    parent = self.game.hash_code
    nbSim = self.get_value('nbSim')
    #--------CHECK MEMORY
    if parent in self.decision.memory:
        memoire = self.decision.memory[parent] # parent en mémoire, récupération
        #----traitement avec éventuel arrêt
        if memoire['exact']: return memoire['score']
        if memoire['pf'] >= pf:
          # arret car on a un résultat en mémoire plus précis (plus grande profondeur) que ce qu'on pourrait calculer là
          return memoire['score']
        alpha=max(alpha, memoire["score"])
        if alpha>=beta: self.decision.memory[parent]['pf']=pf; return memoire['score']
        
    #--------FEUILLE       
    if self.game.over():
      _c = 1 if self.who_am_i == self.game.turn else -1 #coef du résultat (+1 ou -1)
      # ICI - maj
      score = _c * self.estimation() #(+100 ou -100)
      self.decision.memory[parent]={'pf':pf,
                                  'exact':self.game.over(),
                                  'score':score,
                                  'best_action':None}
      print('feuille', score)
      return score
    if pf == 0:
        if self.who_am_i == self.game.turn :
            win, loss, draw = self.simulation(nbSim)
            score = self.WIN * scoring(win,loss,draw)
            self.decision.memory[parent]={'pf':pf,
                                  'exact':self.game.over(),
                                  'score':score,
                                  'best_action':None}
            return score
        else :
            win, loss, draw = self.simulation(nbSim,False)
            score = self.WIN * scoring(win,loss,draw)
            self.decision.memory[parent]={'pf':pf,
                                  'exact':self.game.over(),
                                  'score':score,
                                  'best_action':None}
            return score
    #--------PAS FEUILLE
    score=-(self.WIN+1)
    exact=False
    best_action=None
    
    for a in self.game.actions:
      #----CONFLIT
      if alpha >= beta:
        # ICI - on enregistre le fait qu'il ne sert à rien de jouer ce coup 
        self.decision.memory[parent]={'pf':pf,
                                    'exact':exact,
                                    'score':score, #aucun score renvoyé car conflit 
                                    'best_action':best_action} 
        return beta #retour niveau précédent
    
      #----PAS CONFLIT => OK
      self.game.move(a)
      parent_fils = self.game.hash_code # ICI - sauvegarde locale info fils
      _M = - self.__cut(pf-1, -beta, -alpha) # SCORE (_Mesure)
      self.game.undo()
      # ICI - maj SI meilleure valeur <=> si alpha est modifié => on retien quel fils est responsable de cette modification
      #il n'y a pas de sauvegarde dans le cas contraire !
      #Dans tous les cas, à une profondeur donnée, alpha sera forcément mis à jour au moins une fois 
      if _M > score: #Il faut intialiser par une variable différente de alpha qui sera égale à -1000 (sinon au niveau de la boucle la comparaison sera tjr avec alpha)
          #--valeur tampon pour renvoi final du noeud 
          score=_M
          exact=self.decision.memory[parent_fils]['exact']
          best_action=a
      alpha = max(_M, score)            
    # ICI - mise a jour du neud : valeur finale renvoyée une fois toutes les branches fils parcourues
    self.decision.memory[parent]={'pf':pf,
                                'exact':exact,
                                'score':score,
                                'best_action':best_action}  
    return score
#=======================================================================
import numpy as np
class UCB(Player):
    
    def decision(self, state):
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print (" not my turn to play ")
            return None
        
        _scores = []
        _nbSims = self.get_value('nbSim')
        if _nbSims < 1: return None
        
        for a in self.game.actions :
            self.game.move(a)
            _scores.append(self.simulation(1)) # stockage
            self.game.undo()
      
        for i in range((_nbSims -1)*len(self.game.actions)):
            # déterminer idx qui maximise formule UCB
            best_ucb = -1000
            best_action = None
            for a in _scores:
                utilite_a = scoring(a[0],a[1],a[2])
                #ucb_a = utilité  +  C  * sqrt(log(nombre de simu totales)/n-ième essai sur la machine i)
                ucb_a = utilite_a + 0.3 * np.sqrt(np.log(i+1)/(a[0]+a[1]+a[2]))#win + loss + draw
                if ucb_a > best_ucb:
                    best_action, best_ucb = a, ucb_a
            idx = _scores.index(best_action)
            b = self.game.actions[idx]
            self.game.move(b)
            _resultat = self.simulation(1)
            self.game.undo()
            
            # mettre à jour _scores [idx] avec _resultat
            _scores[idx][0] += _resultat[0]
            _scores[idx][1] += _resultat[1]
            _scores[idx][2] += _resultat[2]
            
        # déterminer a qui maximise formule UCB
        return self.game.actions[idx]
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
    #code = '''
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
    
    #testcode(code)

    
if __name__ == "__main__":
    from allumettes import Matches
                     
    jeu = Matches(13, True)
                     
    joueur=Randy_MC('tot', jeu, pf=3)
    
    joueur.who_am_i=jeu.turn
                     
   
                     
    Randy_MC.decision.memory={}
                     
    joueur.decision((4,4))
    joueur.decision((4,4))
    joueur.decision((4,4))
    joueur.decision((3,2))
                     
    # for k in joueur.decision.memory:
        
    #     print(k, joueur.decision.memory[k])

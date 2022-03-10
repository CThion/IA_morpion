#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random
#=========== les classes à mettre en oeuvre pour le jalon 02 ===========#
class Human(Player):
  """
  * On affiche le jeu 
  * On demande à l’utilisateur de choisir une action parmi les actions autorisées 
  * On return cette action.
  """
  # -----------------------------------------------
  def decision(self, state):
    """reçoit en entrée un état du jeu, dépendant du jeu auxquel on joue
    Renvoit l'action choisie par l'utilisateur
    """
    #--mise à jour de l’état du jeu / vérification validité du joueur
    self.game.state = state 
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    #--Affichage de la partie avec les règles
    print(f"""
          Règle et état du jeu : {self.game} \n
          Plateau de jeu : {self.game.board} \n
          Actions possibles : {self.game.actions}
          action {self.game.actions[2]}
          """)
    #--choix d'un coup par le joueur
    choice = input("Où voulez-vous jouer ? ")
    while choice.isdecimal()==False or int(choice) not in range(0,len(self.game.actions)):  
      #--Tant que l'input n'est pas valide
      choice = input('Mauvais choix, réessayez. Où voulez-vous jouer ? : ') 
    return self.game.actions[int(choice)]
# -----------------------------------------------------------------------
class Randy(Player):
  """
  * La méthode de décision renvoie au hasard, grâce à la commande random.choice 
  une des actions possibles du jeu
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i: #verif joueur valide
      print("not my turn to play")
      return None
    #--
    return random.choice(self.game.actions)
# -----------------------------------------------------------------------
class MinMax(Player): #récursif
  """
  * Méthode récursive sur deux autres méthodes : __eval_min et __eval_max
  * Le but est de parcourir l’arbre des coups possibles jusqu’à une certaine profondeur. 
  * La profondeur est donnée au constructeur au moment de la création
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i: #verif joueur valide
      print("not my turn to play")
      return None
    #-- récupération paramètres
    pf = self.get_value('pf') #on récupère la profondeur
    a_best = None #meilleur action trouvée
    v_best = -1000 #valeur (poid) de a_best
    #-- parcours arbre
    for a_i in self.game.actions:   #pour chaque action à partir de la racine
      self.game.move(a_i)           #on essaie les actions possibles une par une
      v_i = self.__eval_min(pf-1)   #lancement chaîne min max (processus récurcif) 
      if v_i > v_best: #mise à jour si une meilleur valeure est trouvée
          v_best = v_i 
          a_best = a_i
      self.game.undo()              #je reviens à l'état précédent
    return a_best 

  # -----------------------------------------------
  def __eval_min(self, pf):
    """Cherche à minimiser les gains adverses. Utilisé sur les noeuds gérés par
    l'adversaire. Appelle __eval_max()"""
    v_min=[]
    #si on est au max de pf, ou sur une feuille : on s'arrête
    if pf == 0 or self.game.over() == True : return self.estimation() #p8 fiche aide
    else:                                       
      for action in self.game.actions:
        self.game.move(action)
        v_i = self.__eval_max(pf-1)
        v_min.append(v_i)
        self.game.undo()
      return min(v_min)

  # -----------------------------------------------
  def __eval_max(self,pf):
    """Cherche à maximiser les gains du joueur. Utilisé sur les noeuds gérés par
    le joueur. Appelle __eval_min()"""
    v_max=[]
    if pf == 0 or self.game.over() == True : return self.estimation()
    else:
      for action in self.game.actions:
        self.game.move(action)
        v_i = self.__eval_min(pf-1)
        v_max.append(v_i)
        self.game.undo()
      return max(v_max)
# -----------------------------------------------------------------------
class AlphaBeta(Player):
  """
  Algorithme du MinMax optimisé en donnant des bornes alpha et beta, 
  qui réduisent le champ des possibles (Branch&Brant).
  Alpha = borne max(inf)
  Beta = borne min(sup)
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    #--
    pf = self.get_value('pf') #on récupère la profondeur
    alpha = -101 #alpha et beta ne sont pas choisies par l'utilisateur
    beta = 101  #  +- self.WIN +-1 (aide_jalon_02 p11)
    liste_vi=[]
    #--
    for a_i in self.game.actions:   #pour chaque action
      #--changement d'état
      self.game.move(a_i)           #j'avance sur l'une des actions disponible
      #--récupération informations
      v_i = self.__coupe_alpha(pf-1, alpha, beta)   #on diminue d'abord la borne beta 
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
    if pf == 0 or self.game.over() == True : return self.estimation()
    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])
      v_i = self.__coupe_beta(pf-1, alpha, beta) #chaîne récursive
      self.game.undo()
      if v_i <= alpha: return alpha
      beta = min(beta, v_i)
      i = i+1
    return beta
  # -----------------------------------------------
  def __coupe_beta(self, pf, alpha, beta):
    """MAX cherche a augmenter alpha"""
    if pf == 0 or self.game.over() == True : return self.estimation()
    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])
      v_i = self.__coupe_alpha(pf-1, alpha, beta) #chaîne récursive
      self.game.undo()
      if v_i >= beta: return beta
      alpha = max(alpha, v_i)
      i = i+1
    return alpha
# -----------------------------------------------------------------------
class Negamax(Player):  #optionnel 1
  """
  Version améliorée de l'algorithme MinMax
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    pf = self.get_value('pf') #on récupère la profondeur
    a_best = None #meilleur action trouvée
    v_best = -1000 #valeur (poids) de a_best
    #-- parcours arbre
    for a_i in self.game.actions:   #pour chaque action à partir de la racine
      self.game.move(a_i)           #on essaie les actions possibles une par une
      v_i = -self.__eval_negamax(pf-1)   #lancement chaîne min max (processus récurcif) 
      if v_i > v_best: #mise à jour si une meilleur valeure est trouvée
          v_best = v_i 
          a_best = a_i
      self.game.undo()              #je reviens à l'état précédent
    return a_best 
  # -----------------------------------------------
  def __eval_negamax(self,pf):  
    """Objectif : regrouper eval_min et eval_max en 1 methode"""  #Pas d'utilisation de la propriété
    if pf == 0 or self.game.over() == True:
      if self.who_am_i == self.game.turn : return self.estimation()
      else : return -self.estimation()
    else:
      liste =[]
      for actions in self.game.actions:
        self.game.move(actions)
        v_i = -self.__eval_negamax(pf-1)
        liste.append(v_i)
        self.game.undo()
      return max(liste)
  # -----------------------------------------------------------------------
class NegAlphaBeta(Player): #optionnel 2
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
    if pf == 0 or self.game.over() == True :
      if self.who_am_i == self.game.turn : return -self.estimation()
      else : return self.estimation()
    i = 0
    while i<len(self.game.actions) and alpha<beta:
      self.game.move(self.game.actions[i])
      v_i = -self.__coupe_alpha(pf-1, -beta,-alpha) #chaîne récursive
      self.game.undo()
      if v_i <= alpha: return alpha
      beta = min(beta, v_i)
      i = i+1
    return beta

#====================== exemples de code test ==========================#
if __name__ == "__main__":
    #--tous les jeux disponibles pour les tests (pour les paramètres cf fichiers)
    from allumettes import Matches
    from dice import Dice
    from marienbad import Marienbad
    from divide import Divide
    from divide_left import Divide as Divide_left
    jeu_allumettes = Matches(13, True) # le but prendre la dernière allumette
    jeu_dice = Dice(50)
    jeu_marienbad = Marienbad(7, 0)
    jeu_divide = Divide(10, 8)
    jeu_divide_left = Divide_left(10, 8)
    #--jeu courrant pour les tests :
    jeu = jeu_allumettes
    #--initialisation du context de jeu
    moi = MinMax('toto', jeu, pf=5)
    moi.who_am_i = jeu.turn # moi est le premier joueur
    #-- TESTS
    moi.decision( (7, 6) ) # on attend 1, 2 ou 3 pour Human et Randy
    #print(jeu) # on attend 7 allumettes

def test_decision(joueur):
    """ joueur est une classe telle que Human, Randy, MinMax """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
print(jeu) # on attend 13 allumettes

moi = Human('toto', jeu, pf=3)
moi.decision( (3, 4) ) # on attend None
print(jeu) # on attend 3 allumettes

moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (7, 3) ) # on attend None
print(jeu) # on attend 7 allumettes

moi.decision( (7, 4) ) # on attend 1, 2 ou 3 pour Human et Randy
print(jeu) # on attend 7 allumettes
''' ; testcode(code)

def test_clever(joueur):
    """ on attend que joueur soit MinMax Negamax AlphaBeta Neg_AlphaBeta """
    code = '''
from allumettes import Matches
jeu = Matches(13, False) # le but prendre la dernière allumette
print(jeu) # on attend 13 allumettes

moi = joueur('toto', jeu, pf=3)
moi.who_am_i = jeu.turn # moi est le premier joueur
moi.decision( (3, 4) ) # on attend 3
print(jeu) # on doit voir 3 allumettes

moi.decision( (5, 4) ) # on attend 1
print(jeu) # on doit voir 5 allumettes

jeu2 = Matches(13, True) # le but ne pas prendre la dernière allumette
moi = joueur('toto', jeu2, pf=3)
moi.who_am_i = jeu2.turn # moi est le premier joueur
moi.decision( (3, 4) ) # on attend 2
print(jeu2) # on doit voir 3 allumettes

moi.decision( (4, 4) ) # on attend 3
print(jeu2) # on doit voir 4 allumettes

moi.decision( (5, 4) ) # on attend 1
print(jeu2) # on doit voir 5 allumettes
''' ; testcode(code)
    

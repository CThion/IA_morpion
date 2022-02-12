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
    while choice.isdecimal()==False or int(choice) not in range(1,len(self.game.actions)+1):  
      #--Tant que l'input n'est pas valide
      choice = input('Mauvais choix, réessayez. Où voulez-vous jouer ? : ') 
    return int(choice)
    #en utilisant input, spécifier isdecimal pour s'assurer que la chaine de caractère 
    #ne contient que des nombres
    
    
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
    c = random.choice(self.game.actions)
    return c

# -----------------------------------------------------------------------
class MinMax(Player): #récursif
  """
  * Elle va nécessiter, en plus de la méthode decision de deux méthodes privées 
  c’est-à-dire dont le nom sera préfixé par 2 soulignés « __ »
  * Le but est de parcourir l’arbre des coups possibles jusqu’à une certaine 
  profondeur. 
  * La profondeur sera donnée au constructeur au moment de la création
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    self.pf = self.get_value('pf')
    for a_i in self.game.actions:
      #calculer s_i le nouvel etat construit par (s,a_i)

      v_i = self.__eval_min(pf-1)
    #return a_j tel que v_j = max(v_1, .. v_k) et j minimum 
  
    
  # -----------------------------------------------
  def __eval_min(self,pf):
    """Cherche à minimiser les gains adverses"""
    s = self.game.state
    if pf == 0 or self.game.over() == True : return s
    else:
      for k in range(liste):  #Manque à définir liste, cad les s_k construits par (s, a_j)
        k = self.eval_max(s,pf-1)
        liste.append(k)
      return min(liste)
  # -----------------------------------------------
  def __eval_max(self,pf):
    s = self.game.state
    if pf == 0 or self.game.over() == True : return s
    else:
      for k in range(liste):  #Manque à définir liste, cad les s_k construits par (s, a_j)
        k = self.eval_min(s,pf-1)
        liste.append(k)
      return max(liste)
# -----------------------------------------------------------------------
class AlphaBeta(Player):
  """
  Docstring à rajouter
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
  # -----------------------------------------------
# -----------------------------------------------------------------------
class NegaMax(Player):  #optionnel 1
  """
  Docstring à rajouter
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
  # -----------------------------------------------
  # -----------------------------------------------------------------------
class AlphaBetaNegaMax(Player): #optionnel 2
  """
  Docstring à rajouter
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
  # -----------------------------------------------


#====================== exemples de code test ==========================#
if __name__ == "__main__":
    from allumettes import Matches
    jeu = Matches(13, True) # le but prendre la dernière allumette
    moi = Human('toto', jeu, pf=3)
    moi.who_am_i = jeu.turn # moi est le premier joueur
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
    

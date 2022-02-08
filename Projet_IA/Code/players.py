#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# this file is supposed to define all the players
from classes.abstract_player import Player
from tools.ezCLI import testcode
import random
#########################################################################
#---------CLEMENT LIT CE MESSAGE------------------
#ON PEUT FAIRE DES TESTS VIA MAIN_TEST.PY
#########################################################################
#=========== les classes à mettre en oeuvre pour le jalon 02 ===========#
class Human(Player):
  """
  * On affiche le jeu 
  * On demande à l’utilisateur de choisir une action parmi les actions autorisées 
  * On return cette action.
  """
  # -----------------------------------------------
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    print(self.game) #Affichage de la partie avec les règles
    print("Plateau de jeu: ",self.game.board)
    print("Actions possibles: ", self.game.actions)
    choice = input("Où voulez-vous jouer ? Choisissez '1','2' ou '3'")
    if choice == 1 or choice =='1': choice = self.game.actions[0]
    if choice == 2 or choice =='2': choice = self.game.actions[1]
    if choice == 3 or choice =='3': choice = self.game.actions[2]

    while choice not in self.game.actions:  #Tant que l'input n'est pas valide
      choice = input('Mauvais choix, réessayez. Où voulez-vous jouer ?') 
    return choice


# -----------------------------------------------------------------------
class Randy(Player):
  """
  * La méthode de décision renvoie au hasard, grâce à la commande random.choice une des actions possibles du jeu
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    c = randrange(len(self.game.actions))
    return self.game.actions[c]

# -----------------------------------------------------------------------
class MinMax(Player): #récursif
  """
  * Elle va nécessiter, en plus de la méthode decision de deux méthodes privées c’est-à-dire dont le nom sera préfixé par 2 soulignés « __ »
  * Le but est de parcourir l’arbre des coups possibles jusqu’à une certaine profondeur. 
  * La profondeur sera donnée au constructeur au moment de la création
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
    self.state = state  #etat de la partie : à regarder pour savoir où jouer
    self.force = 0
    #super().__init__(nom=nom,jeu=jeu,profondeur)
    #self.profondeur = profondeur
  # -----------------------------------------------
  def __min():
    for i in range(self.profondeur):
      pass
    pass
  # -----------------------------------------------
  def __max():
    pass
# -----------------------------------------------------------------------
class AlphaBeta(Player):
  """
  
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
  
  """
  def decision(self, state):
    self.game.state = state # on met à jour l’état du jeu
    if self.game.turn != self.who_am_i:
      print("not my turn to play")
      return None
    # maintenant on peut travailler
  # -----------------------------------------------


#====================== exemples de code test ==========================#
from random import randrange

def test_decision(joueur):
    """ joueur est une classe telle que Human, Randy, MinMax """
    code = '''
from allumettes import Matches
jeu = Matches(13, True) # le but prendre la dernière allumette
print(jeu) # on attend 13 allumettes

moi = joueur('toto', jeu, pf=3)
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
    

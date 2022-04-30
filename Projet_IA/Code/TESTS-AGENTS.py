# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:33:29 2022

@author: cleme
"""

from players_mc import * #les agents avec mémoire
from players import * #les agents sans mémoire

from main_parties import Statistics #class pour simuler des parties entre agents

#--tous les jeux disponibles pour les tests (pour les paramètres cf fichiers)
from morpion import Morpion
from allumettes import Matches
from dice import Dice
from marienbad import Marienbad
from divide import Divide
from divide_left import Divide as Divide_left

#--------
 
class testagent():
    """class regroupant plusieurs batterie de test pour les agents de player_mc
    """
    def __init__(self):
        pass
    
    def rapidite(self):
        """teste la rapidité de l'agent
        """
        pass
    
    def efficacite(self):
        """teste l'efficacité de l'agent
        """
        pass
    
    def flexibilite(self):
        """teste la flexibilité de l'agent
        """
        pass
    
    def memorisation(self):
        """teste la capacité à utiliser la mémoire d'un agent
        """
        pass



def letsplay(jeu, j1, j2, tmax):
    """simulation d'une partie à deux agents
    tmax = durée maximal de la partie
    leur joueur 1 joue les "O" ; le joueur 2 les "X"
    """
    J = [j1, j2]
    i=1
    while (not jeu.win() or not jeu.over()) and i<=3: #tant qu'il n'y a pas de gagnant + reste des coups
        j = J[jeu.turn]
        print("j", j)
        a = j1.decision(jeu.state)
        jeu.move(a)
        print(jeu)
        i+=1

if __name__=="__main__":
    
    #----le jeu
    jeu =Morpion()
    
    #----les joueurs
    j1 = NegAlphaBeta_Memory('toto', jeu, pf=5)
    j2 = NegAlphaBeta_Memory('toto', jeu, pf=5)
    
    
    j1.who_am_i = jeu.turn # c'est à j1 de commencer

    letsplay(jeu, j1, j2, 6*10**4)
    
    
    
    
    
    
    
    
    
    
    
    
    
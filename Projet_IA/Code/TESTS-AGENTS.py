# -*- coding: utf-8 -*-
"""
Created on Wed Apr 27 14:33:29 2022

@author: cleme
"""

from players_mc import * #les agents avec mémoire
from players import * #les agents sans mémoire
from time import time #fonction pour mesurer les temps d'exécution

from main_parties import Statistics, manche, partie #class pour simuler des parties entre agents

#--tous les jeux disponibles pour les tests (pour les paramètres cf fichiers)
from morpion import Morpion


#--------
 
def rapidite(Agents, Advers, jeu, nbPartie):
    
    """teste le paramètre de rapidité entre deux agents
    """
    Stats = {}
    for agent in Agents:
        for advers in Advers:
            stat=partie(advers, agent, jeu, nbPartie)            
            Stat[f"{agent}-VS-{advers}"]=tuple(stat[1], stat[2])
            print(f"statistique : ", stat)
    return Stat

def efficacite(agent, jeu):
    """teste l'efficacité de l'agent
    """
    pass


if __name__=="__main__":
    """
    tests de l'intelligence d'agents sur le jeu Morpion
    """
    jeu = Morpion(3, tore=False) #morpion de taille 3*3 forme non torique
    Agents=[NegAlphaBeta_Memory('toto', jeu, pf=2), UCB('toto', jeu, nbSim=500), NegAlphaBeta_Memory_MC('toto', jeu, pf=2, nbSim=500)] #agents testés
    Advers=[Randy('randy', jeu), MinMax('minmax', jeu, pf=2)]
    
    print(rapidite(Agents, Advers, jeu, 10))
    
    
    
    
    
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
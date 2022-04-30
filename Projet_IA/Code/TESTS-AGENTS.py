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
 
def rapidite(agent, j, jeu):
    
    """teste la rapidité de l'agent
    Co
    """
    j=j
    s = manche(j, agent, jeu)
    print(s)
    return

def efficacite(agent, jeu):
    """teste l'efficacité de l'agent
    """
    pass


if __name__=="__main__":
    """
    tests de l'intelligence d'agents sur le jeu Morpion
    """
    jeu = Morpion()
    Agents=[Randy('randy', jeu), MinMax('minmax', jeu, pf=3), 
            NegAlphaBeta_Memory('toto', jeu, pf=3), UCB('toto', jeu, nbSim=1000), NegAlphaBeta_Memory_MC('toto', jeu, pf=3, nbSim=1000)] #agents testés
    
    rapidite(Agents[2], Agents[1], jeu)
    
    
    
    
    #----evaluation des trois agents
    # for agent in Agents:
    #     print(f"""
    #           Evaluation de {agent} :
    #           """)
    #     rapidite(agent, jeu)
    #     efficacite(agent, jeu)
        
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
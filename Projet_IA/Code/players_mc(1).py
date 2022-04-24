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

#=========== les classes à mettre en oeuvre pour le jalon 03 ===========#
class NegAlphaBeta_Memory(Player):

        
    def decision(self, state):
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None

        beta = self.WIN+1 #Initialisation de beta plus elevé que self.WIN
        alpha = -beta #alpha doit être inférieur à self.WIN (-inf en théorie)

        v = alpha #Meilleure action initialisée à un point bas
        b_a = None #Pas de meilleure action au début

        pf = self.get_value('pf') #Récupération de la profondeur max de recherche 

        key = self.game.hash_code #Récupération de la clé

        if key in self.decision.memory:
            m = self.decision.memory[key]
            if m['pf'] >= pf or m['exact'] == True:
                return m['best_action']
            else:
                alpha = max(alpha, self.decision.memory[key]['score']) #Maj éventuel d'alpha 


                
        for a in self.game.actions:
            print(self.decision.memory)
            self.game.move(a) #Maj de l'état de jeu
            clef_fils = self.game.hash_code
            v_b = - self.__cut(pf-1, alpha, beta)
            self.game.undo() #Retour à l'état précédent
            if v_b > v: #Mis à jour si résultat obtenu meilleur que celui d'avant 
                v = v_b
                b_a = a #Maj de l'action
                exact = self.decision.memory[clef_fils]['exact'] #La valeur exacte de la branche dépend de celle de son "fils"   
                
             
        self.decision.memory[key] = {'pf' : pf , 'exact': exact , 'score': v, 'best_action' : b_a} #On sauvegarde la meilleure action
        return b_a
            
        

    decision.memory = {} #Création du dictionnaire

    
    def __cut(self, pf:int, alpha:float, beta:float) -> float:
        """ we use, max thus cut_beta """
        key = self.game.hash_code

        if key in self.decision.memory : #Cas ou la clé est en mémoire
            
            m = self.decision.memory[key] 
            if m['pf'] >= pf or m['exact'] == True:
                return m['score'] #On renvoie le score deja calculé
            else:
                alpha = max(alpha, self.decision.memory[key]['score']) #Maj éventuel d'alpha 
                if alpha >= beta: return beta # coupe
                
        if pf == 0 or self.game.over(): #Cas ou c'est une feuille 
            _c = 1 if self.who_am_i == self.game.turn else -1
            self.decision.memory[key] = {'pf' : pf , 'exact': self.game.over() , 'score': _c*self.estimation() , 'best_action' : None}
            return _c * self.estimation() #Modification en fonction du joueur racine concerné

        
        
        
    #partie Heuristique 
        
        print(self.decision.memory)
        e_min=-1000
        #Cas ou rien n'est en mémoire donc algo normal
        for a in self.game.actions: #On teste tout les états 
            if alpha >= beta:
                self.decision.memory[key] = {'pf' : pf , 'exact': False  , 'score': beta , 'best_action' : None}   #Sauvegarde mémoire
                return beta #Arret si conflit
            self.game.move(a) #Mis à jour de l'état de jeu
            clef_fils = self.game.hash_code #On récupére la clé du fils
            v = - self.__cut(pf-1, -beta, -alpha) #Appel récursif
            self.game.undo() #On retourne à l'état précédent
            if v > e_min: #Mémoriser la meilleure action
                alpha = v
                e_min = v
                b_a = a
                exact = self.decision.memory[clef_fils]['exact'] #La valeur exacte de la branche dépend de celle de son "fils"
                
        self.decision.memory[key] = {'pf' : pf , 'exact': exact , 'score': alpha , 'best_action' : b_a} #Sauvegarde mémoire
        return alpha

#===========================================================================================================================================
#===========================================================================================================================================
#===========================================================================================================================================


class IterativeDeepening(Player):

    def decision(self, state):
        self.game.state = state
        if self.game.turn != self.who_am_i :
            print(" not my turn to play ")
            return None
        # the parameters to retrieve
        pf = self.get_value('pf')
        second = self.get_value('secondes')
        depth = 0
        # alpha , beta
        _bound = self.WIN +1
        _start = time.time()
        
        while depth <= pf and (time.time() - _start) < second:
            depth +=1
            _a = self.__old_decision(depth , -_bound , +_bound)
            # print (" elapsed {:.2f} depth = {}"
            # "". format(time.time () - _start , depth ))
            print("Ceci est depth",depth)
            print("Ceci est la profondeur",pf)
        print(self.decision.memory)
        return _a


    
    def __old_decision(self, pf:int , alpha:float,beta:float):

        key = self.game.hash_code #Récupération de la clé

        if key in self.decision.memory:
            m = self.decision.memory[key]
            if m['pf'] >= pf or m['exact'] == True:
                return m['best_action']
            else:
                alpha = max(alpha, self.decision.memory[key]['score']) #Maj éventuel d'alpha
                if alpha >= beta :
                    self.decision.memory[key]['pf'] = pf
                    return m['best_action']
        v = -1000        
        for a in self.game.actions:
            self.game.move(a) #Maj de l'état de jeu
            clef_fils = self.game.hash_code
            v_b = - self.__cut(pf-1, alpha, beta)
            self.game.undo() #Retour à l'état précédent
            if v_b > v: #Mis à jour si résultat obtenu meilleur que celui d'avant 
                v = v_b
                b_a = a #Maj de l'action
                exact = self.decision.memory[clef_fils]['exact'] #La valeur exacte de la branche dépend de celle de son "fils"   
                
             
        self.decision.memory[key] = {'pf' : pf , 'exact': exact , 'score': v, 'best_action' : b_a} #On sauvegarde la meilleure action
        return b_a
            
        

    decision.memory = {} #Création du dictionnaire

    
    def __cut(self, pf:int, alpha:float, beta:float) -> float:
        """ we use, max thus cut_beta """
        key = self.game.hash_code

        if key in self.decision.memory : #Cas ou la clé est en mémoire
            
            m = self.decision.memory[key] 
            if m['pf'] >= pf or m['exact'] == True:
                return m['score'] #On renvoie le score deja calculé
            else:
                alpha = max(alpha, self.decision.memory[key]['score']) #Maj éventuel d'alpha 
                if alpha >= beta:
                    self.decision.memory[key]['pf'] = pf #Maj de la profondeur
                    return m['score'] # coupe
                
        if pf == 0 or self.game.over(): #Cas ou c'est une feuille 
            _c = 1 if self.who_am_i == self.game.turn else -1
            self.decision.memory[key] = {'pf' : pf , 'exact': self.game.over() , 'score': _c*self.estimation() , 'best_action' : None}
            return _c * self.estimation() #Modification en fonction du joueur racine concerné

        
        
        
    #partie Heuristique 
        
        e_min=-1000
        #Cas ou rien n'est en mémoire donc algo normal
        for a in self.game.actions: #On teste tout les états 
            if alpha >= beta:
                self.decision.memory[key] = {'pf' : pf , 'exact': exact  , 'score': e_min , 'best_action' : None}   #Sauvegarde mémoire
                return beta #Arret si conflit
            self.game.move(a) #Mis à jour de l'état de jeu
            clef_fils = self.game.hash_code #On récupére la clé du fils
            v = - self.__cut(pf-1, -beta, -alpha) #Appel récursif
            self.game.undo() #On retourne à l'état précédent
            if v > e_min: #Mémoriser la meilleure action
                
                e_min = v
                b_a = a
                exact = self.decision.memory[clef_fils]['exact'] #La valeur exacte de la branche dépend de celle de son "fils"
            alpha = max(alpha,v)
        self.decision.memory[key] = {'pf' : pf , 'exact': exact , 'score': e_min , 'best_action' : b_a} #Sauvegarde mémoire

        return e_min
#========================================================================
class Randy_MC(Player):
    def decision(self, state):
        """ get the state """
        self.game.state = state
        if self.game.turn != self.who_am_i:
            print("not my turn to play")
            return None
        nbSim = self.get_value('nbSim')
        if nbSim < 1 : return None #On a besoin d'au minimum 1 simulation
        best_score = -1.5 #On sélectionne un nombre qui n'est pas entre -1 et 1
        best_action = None #Initialisation de b_a
        for a in self.game.actions:
            self.game.move(a) #On effectue un mouvement
            score = self.simulation(nbSim) #Retourne une liste de triplets [Victoire , défaite , nul]
            self.game.undo()
            w = score[0]
            l = score[1]
            d = score[2]
            
            e = (w-l + 0.5*d)/(w+l+d) #Calcul du scoring 
            if best_action == None or e > best_score:
                best_score = e
                best_action = a
        return best_action 
        
#====================== exemples de code test ==========================#
def usage():
    print("""
> test_clever(cls)
  prend en paramètre une classe n'ayant besoin que de pf
> test_morpion(cls)
  prend en paramètre une classe ayant besoin de pf ou nbSim
  prend en paramètre une classe ayant besoin de pf et secondes
> test_hexapawn(cls)=
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

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 17 14:16:22 2022

@author: geeka
"""

def testcodeCM():
    from allumettes import Matches
    jeu = Matches(13, True)
    print(jeu)
    
    from sol_j02 import Human
    moi = Human('mc', jeu)
    moi.decision((3,4))
    
    moi.simulation(100)
    x = moi.simulation(300)
    x
    
    from synopsis_03 import scoring
    #on donne l'information x à cette fonction. Mais attention cette fonction prend 3 paramètres, et nous ces 3 paramètres on les a dans un liste => utitliser une technique python
    #scoring(x[0], x[1], x[2])
    scoring(*x) #permet d'utiliser une liste en paramètre directement
    #=> résultat : en faisant 300 simulations, il y a un chouilla plus de chance de perdre que de gagner ([146, 154, 0])
    moi.estimation() #--> on a 0 parce que quand il n'y a aucune allumette sur le terrain tu as ni gagné ni perdu
    
    memoire={}
    for a in moi.game.action:
        moi.game.move(a)
        memoire[a] = moi.simulation(100)
        moi.game.undo() #on défait ce qu'on a fait car pour l'instant on ne fait que tester
    print(memoire.keys())
    memoire[3] #je prends 3 alumettes et il n'y en avait que 3 ==> je gagner dans 100% des cas
    memoire[1] #je prends 1 => j'ai une chance sur 2 de gagner (jeu aléatoire)
    memoire[2] #je prends 2 => j'ai perdu dans 100% des cas 
    for a in memoire: print(f"action prend {a} allumettes(s)", scoring(*memoire[a]))
    
    print(moi.game)
    moi.estimation()
    moi.simulation(300)
    for a in moi.game.actions:
        moi.game.move(a)
        memoire[a] = moi.simulation(100)
        moi.game.undo()
    
    for a in memoire: print("action prenre {a} allumettes", scoring(*memoire[a]))
    
    moi.who_am_i = jeu.turn
    moi.estimation()
    
    moi.simulation(300)
    help(jeu)
    
    jeu=Hexapawn(priorite=True)
    print(jeu)
    
    moi=Randy("mmc", jeu)
    moi.who_am_i = jeu.turn
    moi.estimation()
    
    moi.simulation(300)
    moi.simulation(3000)
    #on tend de plus en plus vers l'espérance réelle
    
    import time
    x = time.perf_counter(); moi.simulation(100); print(time.perf_counter -x)
    return

def UCB():
    from math import log, sqrt
    form synopsis_03 import scoring
    
    def choix_ucb(L:list) -> int:
        _ni = [sum(cpt) for cpt in L] #cpt=compteur
        _n=sum(_ni)
        _best=-1
        for i,cpt in enumerate(L):
            _ev = scoring(*cpt)+0.3*sqrt(log)#MANQUE UN TRUC
        
    L=[]
    for a in moi.game.actions:
        moi.game.move(a)
        L.append(moi.simulation(10))
        moi.game.undo()
    L
    _l = [sum(x) for x in L]
    sum(_l)
    len(L)
    
    from synopsis_03 import scoring
    _3 = [scoring(*x) for x in L]
    len(_3)
    _3.index(-0.14)
    _3
    from math import log, sqrt
    _4 = [x+sqrt(log(2500)/100) for x in _3]
    _4.index(max(_4))
    moi.game.actions[18]
    moi.game.move(moi.game.action[18])
    _nouveau=moi.simulation(100)
    moi.game.undo()
    print(moi.game)
    _nouveau
    L
    L[18]
    _n18=[x+y for x,y in zip(_nouveau, L[18])]
    
    #quand on fait une simulation il n'y a qu'une série de compteur qui change, donc seulement une série d'utilité ==> ne pas tout remettre à jour à chaque fois
    scoring(*L[18])
    _3[18]
    _3
    
    _n=sum(_l)
    _n
    
    _4
    
    _3 #scoring
    _1

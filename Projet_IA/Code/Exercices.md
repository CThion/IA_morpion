# Exercices 

## Exercice 1

### 1)

Décision à la racine : Sommet B, car il a le plus grand poids des trois.

### 2)

- $S_1$ : 1
- $S_2$ : 5
- $S_3$ : 1

### 3)

$$ S_1 \rightarrow S_4 \rightarrow S_{10} \rightarrow S_{19} \rightarrow S_{20} \rightarrow S_{11} \rightarrow S_{21} \rightarrow S_5 \rightarrow S_{12} \rightarrow S_{22} \rightarrow S_{23} \rightarrow S_{13} \rightarrow S_6 \\ \rightarrow S_2 \rightarrow S_7 \rightarrow S_{14} \rightarrow S_{24} \rightarrow S_{25} \rightarrow S_{15} \rightarrow S_{26} \\ \rightarrow S_3 \rightarrow S_{32} \rightarrow S_8 \rightarrow S_{16} \rightarrow S_{27} \rightarrow S_{28} \rightarrow S_{29} \rightarrow S_9 \rightarrow S_{17} \rightarrow S_{30} \rightarrow S_{31} \rightarrow S_{18}$$

### 4)

Tous les sommets pouvant être atteint, en partant de la racine par un chemin de longueur inférieur ou égale à 4 (l’arbre visible sur le sujet), sont visités. Tous les sommets nécessitant un chemin de longueur strictement supérieure à 4 (la profondeur) ne sont pas visités.

### 5)

![image-20220223201803376](C:\Users\geeka\AppData\Roaming\Typora\typora-user-images\image-20220223201803376.png)

Pour évaluer la valeur de $S_1$ : je pars du principe que mon adversaire n’est pas con, et donc qu’il va forcément choisir le truc qui va l’arranger le plus lui au prochain tour, c’est à dire le truc qui va le plus me faire suer, c’est à dire le coup qui minimise mes gains. Donc je sais qu’il va forcément choisir $S_6$ puisque, entre $S_4,\ S_5,\ S_6$ c’est $S_6$ qui lui rapportera le plus (ici $S_6$ vaut $20-1 = 19$ pour l’adversaire)

## Exercice 2

1. Quelle est la décision à la racine?

   AlphaBeta renvoie la même chose que MinMax ==> décision à la racine est $S_2$

2. Donnez l’ordre de visite des sommets de l’arbre, l’ordre est obtenu par le premier accès au
    cours du parcours en profondeur d’abord.

    | Sommet | $\alpha$ | $\beta$                  |
    | ------ | -------- | ------------------------ |
    | S1     | -00      | +00                      |
    | S4     | -00      | +00                      |
    | S10    | -00      | +00                      |
    | S19    | -00      | +00                      |
    | S10    | -00      | 19                       |
    | S20    | -00      | 19                       |
    | S10    | -00      | 8                        |
    | S4     | 8        | +00                      |
    | S11    | 8        | 8                        |
    | S21    | 8        | 8                        |
    | S11    | 8        | -10 => erreur => garde 8 |
    | S4     | 8        | 8                        |
    | S1     | 8        | 8                        |
    | S5     | 8        | 8                        |
    | S12    | 8        | 8                        |
    | S22    | 8        | 2 => erreur => garde 2   |
    |        |          |                          |
    |        |          |                          |
    |        |          |                          |
    
    
    
3. **Quels sont les sommets qui peuvent modiﬁer la valeur de α ?**

    Tous les sommets de profondeur paire

4. **Quels sont les sommets qui peuvent modiﬁer la valeur de β ?**

    Tous les sommets de profondeur impaire

5. **Y-a-t-il des sommets non visités par l’algorithme de l’alpha-beta?**

6. **Donnez la valeur ﬁnale renvoyée par les sommets visités de l’arbre sauf celles des feuilles,**
  **ainsi que les valeurs de α et β lorsqu’on accède pour la première fois au sommet et lorsqu’on**
  **quitte le sommet.**

  


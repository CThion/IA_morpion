# Exercices 

## Exercice 1

### 1)  Quelle est la décision à la racine

Décision à la racine : Sommet B, car il a le plus grand poids des trois.

### 2) Donnez les valeurs des 3 sommets successeurs de la racine qui justiﬁent cette décision.

- $S_1$ : 1
- $S_2$ : 5
- $S_3$ : 1

### 3) Donnez l’ordre de visite des sommets de l’arbre, l’ordre est obtenu par le premier accès au cours du parcours en profondeur d’abord.

$$ S_1 \rightarrow S_4 \rightarrow S_{10} \rightarrow S_{19} \rightarrow S_{20} \rightarrow S_{11} \rightarrow S_{21} \rightarrow S_5 \rightarrow S_{12} \rightarrow S_{22} \rightarrow S_{23} \rightarrow S_{13} \rightarrow S_6 \\ \rightarrow S_2 \rightarrow S_7 \rightarrow S_{14} \rightarrow S_{24} \rightarrow S_{25} \rightarrow S_{15} \rightarrow S_{26} \\ \rightarrow S_3 \rightarrow S_{32} \rightarrow S_8 \rightarrow S_{16} \rightarrow S_{27} \rightarrow S_{28} \rightarrow S_{29} \rightarrow S_9 \rightarrow S_{17} \rightarrow S_{30} \rightarrow S_{31} \rightarrow S_{18}$$

### 4)  Y-a-t-il des sommets non visités par l’algorithme du MinMax?

Tous les sommets pouvant être atteint, en partant de la racine par un chemin de longueur inférieur ou égale à 4 (l’arbre visible sur le sujet), sont visités. Tous les sommets nécessitant un chemin de longueur strictement supérieure à 4 (la profondeur) ne sont pas visités.

### 5) Donnez la valeur ﬁnale renvoyée par les sommets de l’arbre sauf celles des feuilles et celle des 4 premiers sommets de l’arbre S 0 , S 1 , S 2 , S 3 .
![image-20220223201803376](C:\Users\geeka\AppData\Roaming\Typora\typora-user-images\image-20220223201803376.png)

---

## Exercice 2

### 1) Quelle est la décision à la racine?

AlphaBeta renvoie la même chose que MinMax, la décision à la racine est $S_2$.

### 2) Donnez l’ordre de visite des sommets de l’arbre, l’ordre est obtenu par le premier accès au cours du parcours en profondeur d’abord.

Voici l’évolution d’AlphaBeta dans l’arbre:

$$ S_1 \rightarrow S_4 \rightarrow S_{10} \rightarrow S_{19} \rightarrow S_{20} \rightarrow S_{11} \rightarrow S_{21} \rightarrow S_5 \rightarrow S_{12} \rightarrow S_{22} \rightarrow S_{23} \rightarrow S_{13} \rightarrow S_6 \\ \rightarrow S_2 \rightarrow S_7 \rightarrow S_{14} \rightarrow S_{24} \rightarrow S_{25} \rightarrow S_{15} \rightarrow S_{26} \\ \rightarrow S_3 \rightarrow S_{32}$$

### 3) **Quels sont les sommets qui peuvent modiﬁer la valeur de α ?**

Tous les sommets de profondeur paire qui ne sont pas ignorés

### 4) **Quels sont les sommets qui peuvent modiﬁer la valeur de β ?**

Tous les sommets de profondeur impaire qui ne sont pas ignorés

### 5) **Y-a-t-il des sommets non visités par l’algorithme de l’alpha-beta?**

On s’attend a avoir $2\sqrt{n}-1=2\sqrt{32}-1=10$ sommets non visités. En l'occurrence on a tous les sommets en dessous des nœuds $S_8$  et $S_9$ (exclus eux aussi) qui ne sont pas visités, c’est à dire précisément les sommets 

$$S_8 \rightarrow S_{16} \rightarrow S_{27} \rightarrow S_{28} \rightarrow S_{29} \rightarrow S_9 \rightarrow S_{17} \rightarrow S_{30} \rightarrow S_{31} \rightarrow S_{18}$$, c’est à dire 10 sommets en tout, ce qui correspond bien à ce qui est attendu.

### 6)  Donnez la valeur ﬁnale renvoyée par les sommets visités de l’arbre sauf celles des feuilles, ainsi que les valeurs de α et β lorsqu’on accède pour la première fois au sommet et lorsqu’on  quitte le sommet.

![alphaBeta](C:\Users\geeka\Downloads\alphaBeta.jpg)

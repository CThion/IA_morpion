# Exercices 

## Exercice 1

### 1)  Quel est la décision à la racine

Décision à la racine : Sommet B, car il a le plus grand poids des trois.

### 2) Donnez les valeurs des 3 sommets successeurs de la racine qui justiﬁe cette décision.

- $S_1$ : 1
- $S_2$ : 5
- $S_3$ : 1

### 3) Donnez l’ordre de visite des sommets de l’arbre, l’ordre est obtenu par le premier accès au cours du parcours en profondeur d’abord.

$$ S_1 \rightarrow S_4 \rightarrow S_{10} \rightarrow S_{19} \rightarrow S_{20} \rightarrow S_{11} \rightarrow S_{21} \rightarrow S_5 \rightarrow S_{12} \rightarrow S_{22} \rightarrow S_{23} \rightarrow S_{13} \rightarrow S_6 \\ \rightarrow S_2 \rightarrow S_7 \rightarrow S_{14} \rightarrow S_{24} \rightarrow S_{25} \rightarrow S_{15} \rightarrow S_{26} \\ \rightarrow S_3 \rightarrow S_{32} \rightarrow S_8 \rightarrow S_{16} \rightarrow S_{27} \rightarrow S_{28} \rightarrow S_{29} \rightarrow S_9 \rightarrow S_{17} \rightarrow S_{30} \rightarrow S_{31} \rightarrow S_{18}$$

### 4)  Y-a-t-il des sommets non visités par l’algorithme du MinMax?

Tous les sommets pouvant être atteint, en partant de la racine par un chemin de longueur inférieur ou égale à 4 (l’arbre visible sur le sujet), sont visités. Tous les sommets nécessitant un chemin de longueur strictement supérieure à 4 (la profondeur) ne sont pas visités.

### 5) Donnez la valeur ﬁnale renvoyée par les sommets de l’arbre sauf celles des feuilles et celle
des 4 premiers sommets de l’arbre S 0 , S 1 , S 2 , S 3 .

![image-20220223201803376](C:\Users\geeka\AppData\Roaming\Typora\typora-user-images\image-20220223201803376.png)

## Exercice 2

### 1) Quelle est la décision à la racine?

AlphaBeta renvoie la même chose que MinMax ==> décision à la racine est $S_2$

### 2) Donnez l’ordre de visite des sommets de l’arbre, l’ordre est obtenu par le premier accès au cours du parcours en profondeur d’abord.

On s’attend a avoir $2\sqrt{n}-1=2\sqrt{32}-1=10$ sommets non visités. Voici l’évolution de AlphaBeta :

```mermaid

```



$$ S_1 \rightarrow S_4 \rightarrow S_{10} \rightarrow S_{19} \rightarrow S_{20} \rightarrow S_{11} \rightarrow S_{21} \rightarrow S_5 \rightarrow S_{12} \rightarrow S_{22} \rightarrow S_{23} \rightarrow S_{13} \rightarrow S_6 \\ \rightarrow S_2 \rightarrow S_7 \rightarrow S_{14} \rightarrow S_{24} \rightarrow S_{25} \rightarrow S_{15} \rightarrow S_{26} \\ \rightarrow S_3 \rightarrow S_{32}$$

VERIFICAITON RATÉE ==>  DEMANDER PROF POUR FORMULE

### 3) **Quels sont les sommets qui peuvent modiﬁer la valeur de α ?**

Tous les sommets de profondeur paire qui ne sont pas ignorés

### 4) **Quels sont les sommets qui peuvent modiﬁer la valeur de β ?**

Tous les sommets de profondeur impaire qui ne sont pas ignorés

### 5) **Y-a-t-il des sommets non visités par l’algorithme de l’alpha-beta?**

Tous les sommets en dessous du nœud $S_8$ 

### 6)  Donnez la valeur ﬁnale renvoyée par les sommets visités de l’arbre sauf celles des feuilles, ainsi que les valeurs de α et β lorsqu’on accède pour la première fois au sommet et lorsqu’on  quitte le sommet.

```mermaid
flowchart

%% Colors %%
classDef blue fill:#66deff,stroke:#000,color:#000
classDef green fill:#6ad98b,stroke:#000,color:#000
classDef red fill:#d00b,stroke:#000,color:#000

%% arbre %%
%%neuds
S0(S0\n-oo/+oo\n-oo/+oo):::green 
S1(S1\n-oo/+oo\n-oo/+oo) ; S2(S2) ; S3(S3)
S4(S4\n-oo/+oo\n-oo/+oo); S5(S5\n-oo/8\n-oo/8);  S7(S7); S8(S8); S9(S9)
S10(S10\n-oo/+oo\n-oo/+oo); S11(S11\n8/+oo\n8/+oo); S12(S12\n-oo/8\n-oo/8); S14(S14); S15(S15); S16(S16); S17(S17); S18(S18)
%%feuilles (bleu)
S6(S6):::blue; S13(S13\n-oo/+oo\n-oo/+oo):::blue
S19(S19\n-oo/+oo\n-oo/19):::blue; S20(S20\n-oo/19\n-oo/8):::blue; S21(S21):::red; S22(S22\n-oo/8\n-oo/5):::blue; S23(S23\n-oo/5\n-oo/2):::blue; S24(S24):::blue; S25(S25):::blue; S26(S26):::blue; S27(S27):::blue; S28(S28):::blue; S29(S29):::blue; S30(S30):::blue; S31(S31):::blue; S32(S32):::blue
%%pf1
S0---S1; S0---S2; S0---S3
%%pf2
S1---S4; S1---S5; S1---S6
S2---S7
S3---S32; S3---S8; S3---S9
%%pf3
S4---S10; S4---S11
S5---S12; S5---S13
S7---S14; S7---S15
S8---S16
S9---S17; S9---S18
%%pf4
S10---S19; S10---S20
S11---S21
S12---S22; S12---S23
S14---S24; S14---S25
S15---S26
S16---S27; S16---S28; S16---S29
S17---S30; S17---S31

```

- jalon_02 entièrement terminé (codes optionnels et exercices)
- début jalon_03
  - ?????

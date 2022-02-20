# IA_morpion

## point clef code python
### \*arg \**Kwargs
arg c'est pour valeur simple (dans un tuple), Kwarg c'est pour les affectations et les mots clefs en général (dans un dico)

### property
pour masquer les valeurs, permet d'utiliser les fonctions comme des variables.

len([index for index, element in enumerate(move) if element == 'O'])

# Jalon\_02

## Questions jalon\_02
- Où met-t-on exactement les import . (zone tests ou bien où c'est vraiment nécessaire ?)
- Les classes doivent vraiment être indépendantes du jeu ? (exemple MinMax compliqué)

## Arborescence des import
- abstract_game ==> morpion, hexapawn, allumettes, divide_left
- abstract_game + abstract_player ==> main_parties

## Algorithme MinMax

- eval_min : s’appliques aux sommets gérés par l’adversaires
- eval_max : s’appliques aux sommets gérés par le joueur
- pf : self.get_value(‘pf’)
- self.game.move(a) : modifie état du jeu en faisant l’action a (choisie parmi self.game.actions)
- self.game.undo() : revient au s précédent
  - :warning: move et undo ne renvoient rien mais modifie s 


# IA_morpion

## point clef code python
### \*arg \**Kwargs
arg c'est pour valeur simple (dans un tuple), Kwarg c'est pour les affectations et les mots clefs en général (dans un dico)

### property
pour masquer les valeurs, permet d'utiliser les fonctions comme des variables.

len([index for index, element in enumerate(move) if element == 'O'])

## Questions jalon02
- Où met-t-on exactement les import . (zone tests ou bien où c'est vraiment nécessaire ?)
- Les classes doivent vraiment être indépendantes du jeu ? (exemple MinMax compliqué)

## Arboresence des import
- abstract_game ==> morpion, hexapawn, allumettes, divide_left
- abstract_game + abstract_player ==> main_parties


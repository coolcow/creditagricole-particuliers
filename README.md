# Client Python pour la banque Crédit agricole - Particuliers

Ce fork a été créé pour permettre l'installation directe depuis Git avec pip. Cela offre deux avantages principaux :

1. **Transparence** : Vous pouvez voir exactement quel code installé est, car il est directement depuis le dépôt Git.
2. **Flexibilité** : Vous pouvez facilement basculer entre différentes versions selon vos besoins.

Ce fork est automatiquement synchronisé avec le dépôt original et inclut une `setup.py` pour faciliter l'installation.

## Changements et Améliorations

Une documentation technique complète de la bibliothèque est maintenant disponible dans le fichier `docs/LIBRARY_REFERENCE.md`. Cette documentation détaille l'ensemble des composants, méthodes et structures de données disponibles dans la bibliothèque.

Des exemples d'utilisation ont été ajoutés dans le dossier `examples/` et sont documentés dans `docs/EXAMPLES.md`. Ces exemples illustrent les cas d'utilisation les plus courants de la bibliothèque.

## Installation

### Installation de la dernière version
```bash
# Dernière version avec modifications (par défaut)
pip install git+https://github.com/coolcow/creditagricole-particuliers.git

# Dernière version sans modifications (sauf setup.py)
pip install git+https://github.com/coolcow/creditagricole-particuliers.git@dmachard
```

### Installation d'une version spécifique
```bash
# Version 0.14.3 avec modifications
pip install git+https://github.com/coolcow/creditagricole-particuliers.git@v0.14.3

# Version 0.14.3 sans modifications (sauf setup.py)
pip install git+https://github.com/coolcow/creditagricole-particuliers.git@v0.14.3-dmachard
```

## Exemples

Des exemples d'utilisation sont disponibles dans le dossier `examples/` du dépôt. Ces exemples couvrent les cas d'utilisation les plus courants et vous aideront à démarrer rapidement avec la bibliothèque.

Pour plus de détails sur les exemples disponibles, consultez le fichier `docs/EXAMPLES.md`.

## Gestion des branches

Ce dépôt utilise une structure de branches claire :

- `main` : Branche principale contenant les modifications et améliorations du code
- `dmachard` : Branche contenant uniquement les modifications de setup.py pour l'installation via pip

## Gestion des versions

Les versions sont gérées par des tags Git suivant le format :
- `vX.Y.Z` : Version X.Y.Z avec modifications et améliorations (version par défaut)
- `vX.Y.Z-dmachard` : Version X.Y.Z sans modifications (sauf setup.py)

### Exemples
- `v0.14.3` : Version 0.14.3 avec modifications et améliorations
- `v0.14.3-dmachard` : Version 0.14.3 sans modifications (sauf setup.py)

## Script create-setup.py

Ce script est un outil de maintenance qui automatise la création du fichier `setup.py` pour ce fork. Voici ses principales fonctionnalités :

1. **Récupération automatique de la version** : Le script interroge l'API GitHub pour obtenir la dernière version disponible dans le dépôt original.
2. **Génération du setup.py** : Il crée automatiquement un fichier `setup.py` avec :
   - La dernière version détectée
   - Les dépendances nécessaires
   - Les métadonnées du projet
   - Les informations de classification Python

### Utilisation

Pour mettre à jour le `setup.py` avec la dernière version :

```bash
python create-setup.py
```

Pour créer le `setup.py` avec une version spécifique :

```bash
python create-setup.py 0.14.3
```

Le script vérifiera automatiquement si la version spécifiée existe dans le dépôt original. Si la version n'est pas fournie, il utilisera la dernière version disponible.

Pour plus d'informations sur l'utilisation de ce client, veuillez consulter la [documentation originale](https://github.com/dmachard/creditagricole-particuliers).
# Utilisation des Exemples de Données du Crédit Agricole

## Table des matières
- [Introduction](#introduction)
- [Fichiers de Données d'Exemple](#fichiers-de-données-dexemple)
  - [Mode JSON](#mode-json)
  - [Mode String](#mode-string)
  - [Mode Types](#mode-types)
- [Script de Création d'Exemples](#script-de-création-dexemples)
  - [Prérequis](#prérequis)
  - [Utilisation](#utilisation)
  - [Arguments de Ligne de Commande](#arguments-de-ligne-de-commande)
  - [Exemples](#exemples)
  - [Fonctionnement](#fonctionnement)
  - [Considérations de Sécurité](#considérations-de-sécurité)
- [Utilisation des Données d'Exemple pour le Développement](#utilisation-des-données-dexemple-pour-le-développement)
- [Mise à Jour des Exemples](#mise-à-jour-des-exemples)

## Introduction

Cette documentation explique comment utiliser les fichiers de données d'exemple et les outils fournis avec la bibliothèque `creditagricole-particuliers` pour faciliter le développement et les tests.

## Fichiers de Données d'Exemple

Le script peut générer des fichiers dans trois formats différents, selon le mode choisi. Si aucun mode n'est spécifié, tous les modes seront exécutés.

### Mode JSON
Ce mode extrait vos données réelles et les sauvegarde au format JSON. Ces fichiers contiennent toutes vos informations financières.

**Fichiers générés :**
- `accounts.json` : Liste complète des comptes
- `account_{numeroCompte}_operations.json` : Historique des opérations pour chaque compte
- `account_{numeroCompte}_iban.json` : Coordonnées IBAN pour chaque compte
- `cards.json` : Liste complète des cartes
- `card_{last4}_operations.json` : Historique des opérations pour chaque carte
- `regionalBank_{code_département}.json` : Informations sur la banque régionale

### Mode String
Ce mode extrait la structure des données en utilisant la représentation textuelle (`__str__`) des objets. Les fichiers sont sauvegardés avec l'extension `.txt`.

**Fichiers générés :**
- `accounts.txt` : Liste complète des comptes (un compte par ligne)
- `account_{numeroCompte}_operations.txt` : Historique des opérations pour chaque compte (une opération par ligne)
- `account_{numeroCompte}_iban.txt` : Fichier vide (l'IBAN n'est pas disponible en mode texte)
- `cards.txt` : Liste complète des cartes (une carte par ligne)
- `card_{last4}_operations.txt` : Historique des opérations pour chaque carte (une opération par ligne)
- `regionalBank_{code_département}.txt` : Informations sur la banque régionale

### Mode Types
Ce mode extrait uniquement la structure des données avec des valeurs fictives. Les valeurs sont remplacées par :
- Chaînes : "" (chaîne vide)
- Nombres entiers : 0
- Nombres décimaux : 0.0
- Booléens : false
- Listes : un seul élément exemple

**Fichiers générés :**
- `account_types.json` : Structure générique d'un compte
- `card_types.json` : Structure générique d'une carte
- `operation_types.json` : Structure générique d'une opération de compte
- `operation_card_types.json` : Structure générique d'une opération de carte
- `regionalBank_types.json` : Structure générique des informations bancaires

## Script de Création d'Exemples

Le script `create_samples.py` se connecte à votre espace Crédit Agricole et récupère les données via la bibliothèque.

### Prérequis

- Vos identifiants Crédit Agricole (identifiant, mot de passe et code département)
- Python 3.6 ou version plus récente
- La bibliothèque `creditagricole-particuliers` installée

### Utilisation

Vous pouvez exécuter le script de plusieurs manières :

1. Sans spécifier de mode (exécute tous les modes) :
```bash
./create_samples.py --username VOTRE_IDENTIFIANT --department VOTRE_CODE_DEPARTEMENT
```

2. Avec un mode spécifique :
```bash
./create_samples.py --username VOTRE_IDENTIFIANT --department VOTRE_CODE_DEPARTEMENT --mode json
```

3. Avec plusieurs modes (séparés par des virgules) :
```bash
./create_samples.py --username VOTRE_IDENTIFIANT --department VOTRE_CODE_DEPARTEMENT --mode json,types
```

### Arguments de Ligne de Commande

- `--username` : Votre identifiant Crédit Agricole (obligatoire)
- `--password` : Votre mot de passe Crédit Agricole (composé de chiffres). Si non fourni, il sera demandé de façon sécurisée
- `--department` : Votre code département (nombre entier, obligatoire)
- `--output-dir` : Dossier de destination pour les fichiers générés (par défaut : ./output)
- `--mode` : Modes de génération (séparés par des virgules) : 'json', 'types', 'str'. Si non spécifié, tous les modes seront exécutés.

### Utilisation des Mocks

Le script supporte l'utilisation de mocks pour le développement et les tests.

Arguments spécifiques aux mocks :
- `--use-mocks-dir` : Dossier contenant les fichiers mock à utiliser
- `--write-mocks-dir` : Dossier où sauvegarder les réponses API en tant que fichiers mock
- `--use-mock-suffix` : Suffixe des fichiers mock à utiliser (par défaut : 'mock')
- `--write-mock-suffix` : Suffixe pour les nouveaux fichiers mock (par défaut : 'mock')

### Exemples

Exécution de tous les modes :
```bash
./create_samples.py --username johndoe --department 75
```

Exécution d'un mode spécifique :
```bash
./create_samples.py --username johndoe --department 75 --mode json
```

Exécution de plusieurs modes :
```bash
./create_samples.py --username johndoe --department 75 --mode json,str
```

Avec un dossier de sortie personnalisé :
```bash
./create_samples.py --username johndoe --department 75 --output-dir ./mes_exemples
```

### Fonctionnement

1. Le script s'authentifie auprès du Crédit Agricole
2. Pour chaque mode sélectionné :
   - Mode 'json' : Extrait et sauvegarde les données réelles au format JSON
   - Mode 'types' : Extrait la structure avec des valeurs fictives au format JSON
   - Mode 'str' : Extrait les représentations textuelles des données au format TXT

3. Structure des dossiers :
   - Si un seul mode est spécifié : les fichiers sont écrits directement dans le dossier de sortie
   - Si plusieurs modes sont spécifiés : un sous-dossier est créé pour chaque mode

### Considérations de Sécurité

- Le script ne conserve pas vos identifiants
- Exécutez-le uniquement sur un système sécurisé
- Pour éviter d'exposer vos données financières, utilisez les modes 'types' ou 'str' pour le développement

## Utilisation des Données d'Exemple pour le Développement

Les fichiers d'exemple peuvent servir pendant le développement à :

1. **Analyser la Structure des Données** : Explorer les champs disponibles
2. **Créer des Interfaces** : Concevoir des écrans d'affichage
3. **Développer Sans Connexion** : Travailler sans connexion à l'API
4. **Automatiser les Tests** : Créer des tests avec des données prévisibles

Les modes 'types' et 'str' sont particulièrement utiles pour :
- Comprendre la structure des API sans exposer des données sensibles
- Partager des exemples dans un dépôt de code
- Créer une documentation technique
- Générer des schémas de validation de données

## Mise à Jour des Exemples

Pour mettre à jour les fichiers d'exemple :

1. Exécutez le script avec vos identifiants et le(s) mode(s) souhaité(s)
2. Vérifiez les fichiers générés dans le dossier de destination
3. Pour les fichiers en mode 'types' ou 'str', vous pouvez les ajouter directement à votre dépôt de code
4. Pour les fichiers en mode 'json', assurez-vous d'anonymiser toute information personnelle avant de les partager 
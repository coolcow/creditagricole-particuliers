# Workflows GitHub Actions

## Synchronisation automatique avec le dépôt upstream

Ce workflow est déclenché lorsqu'une nouvelle version est publiée dans le dépôt original (upstream). Il effectue les opérations suivantes dans l'ordre :

1. **Mise à jour de la branche `upstream`**
   - Synchronise la branche `upstream` avec le dépôt original
   - Cette branche est une copie exacte du dépôt original
   - Crée un nouveau tag au format `vX.Y.Z-upstream`

2. **Mise à jour de la branche `dmachard`**
   - Bascule sur la branche `dmachard`
   - Génère un nouveau `setup.py` avec la dernière version détectée
   - Crée un nouveau tag au format `vX.Y.Z-dmachard`
   - Cette branche contient uniquement les modifications de `setup.py`

3. **Mise à jour de la branche `main`**
   - Bascule sur la branche `main`
   - Intègre les modifications de la branche `dmachard`
   - Crée un nouveau tag au format `vX.Y.Z`
   - Cette branche contient toutes les modifications et améliorations

### Format des tags

- `vX.Y.Z` : Version X.Y.Z avec modifications et améliorations (branche `main`)
- `vX.Y.Z-dmachard` : Version X.Y.Z sans modifications (sauf setup.py) (branche `dmachard`)
- `vX.Y.Z-upstream` : Version X.Y.Z exactement comme dans le dépôt original (branche `upstream`)

### Déclencheurs

Le workflow est déclenché automatiquement par :
- La publication d'une nouvelle version dans le dépôt original
- Une exécution manuelle via l'interface GitHub Actions

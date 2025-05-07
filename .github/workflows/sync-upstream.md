# Workflows GitHub Actions

## Synchronisation automatique avec le dépôt original

Ce workflow est déclenché lorsqu'une nouvelle version est publiée dans le dépôt original (upstream). Il effectue les opérations suivantes dans l'ordre :

1. **Mise à jour de la branche `dmachard`**
   - Synchronise la branche `dmachard` avec le dépôt original via un merge
   - Conserve toutes les modifications du dépôt original
   - Génère un nouveau `setup.py` avec la dernière version détectée
   - Crée un nouveau tag au format `vX.Y.Z-dmachard`
   - Cette branche contient toutes les modifications du dépôt original plus les modifications de `setup.py`

2. **Mise à jour de la branche `main`**
   - Bascule sur la branche `main`
   - Intègre les modifications de la branche `dmachard`
   - Crée un nouveau tag au format `vX.Y.Z`
   - Cette branche contient toutes les modifications et améliorations

### Format des tags

- `vX.Y.Z` : Version X.Y.Z avec modifications et améliorations (branche `main`)
- `vX.Y.Z-dmachard` : Version X.Y.Z du dépôt original avec mise à jour de setup.py (branche `dmachard`)

### Déclencheurs

Le workflow est déclenché automatiquement par :
- La publication d'une nouvelle version dans le dépôt original
- Une exécution manuelle via l'interface GitHub Actions

# 🔍 Scanner Module

Module orchestration du scan pour Horus-RPi5.

## 📂 Structure

```
scanner/
├── __init__.py                  # Exports du module
└── README.md                    # Cette documentation
```

## 🎯 Responsabilités

Ce module contiendra les classes et fonctions pour :

- **Orchestration du pipeline**
  - Gestion du flux de capture
  - Coordination entre engine et calibration
  - Gestion des états

- **Modes de scan**
  - Fast (100 étapes)
  - High Quality (400 étapes)
  - Customs

- **Gestion des fichiers**
  - Export PLY
  - Sauvegarde des métadonnées
  - Historique des scans

## 📝 Note

La logique de scan se trouve actuellement dans `ScanEngine` (engine/scan.py).
Cette structure permet d'abstraire plus tard les responsabilités.

---

**Créé pour Horus-RPi5 Edition** 🔍

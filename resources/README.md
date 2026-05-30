# 📚 Resources

Ressources supplémentaires pour Horus-RPi5.

## 📂 Structure

```
resources/
├── README.md                    # Cette documentation
├── models/                      # Modèles ML pré-entraînés
│   └── .gitkeep
├── calibration/                 # Fichiers de calibration
│   └── .gitkeep
└── test_data/                   # Données de test
    └── .gitkeep
```

## 🎯 Contenu

### models/
- **Modèles pré-entraînés**
  - Détecteurs laser
  - Classificateurs
  - Régresseurs

### calibration/
- **Fichiers de calibration**
  - Matrice caméra (intrinsèques)
  - Distorsion optique
  - Calibrage laser
  - Points de référence

### test_data/
- **Données de test**
  - Images d'exemple
  - Nuages de points PLY
  - Configurations de test

## 🚀 Utilisation

```python
# Charger une ressource
import os
model_path = os.path.join("resources", "models", "laser.tflite")

# Charger une donnée de calibration
calib_path = os.path.join("resources", "calibration", "camera.yaml")
```

---

**Créé pour Horus-RPi5 Edition** 📚

# Horus-RPi5

Version modernisée et compatible Raspberry Pi 5 du logiciel Horus pour scanner 3D Ciclop.

## Installation

```bash
sudo apt update
sudo apt install python3 python3-pip python3-opencv python3-numpy python3-scipy python3-matplotlib python3-pil
pip install -r requirements.txt
```

## Configuration (config.json)

Les réglages caméra, laser et GRBL sont centralisés dans `config.json` :

- `camera.exposure` / `camera.gain` / `camera.white_balance` : réglages manuels
  optionnels pour améliorer le contraste du laser (mettre à `null` pour laisser
  l'auto-réglage de la caméra).
- `camera.warmup_frames` : nombre d'images ignorées à l'ouverture de la caméra
  pour la laisser se stabiliser.
- `laser.threshold` / `laser.hsv_ranges` : utilisés respectivement par
  `ProfileExtractor` et le mode de secours HSV de `LaserAI`.
- `laser.model_path` : chemin vers un modèle TFLite optionnel pour la
  détection laser par IA (nécessite le paquet `tflite-runtime`). En son
  absence, `LaserAI` bascule automatiquement sur la détection HSV.
- `laser.gpio` : contrôle laser direct via GPIO (Raspberry Pi, `gpiozero`),
  en complément des commandes GRBL M3/M5.

## Tests

```bash
pip install pytest opencv-python-headless numpy scipy pyserial gpiozero
pytest tests/
```

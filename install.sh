#!/bin/bash

echo "=== Installation de Horus-RPi5 ==="

sudo apt update
sudo apt install -y python3 python3-pip python3-opencv python3-numpy python3-scipy python3-matplotlib python3-pil

pip install -r requirements.txt

echo "Installation terminée."

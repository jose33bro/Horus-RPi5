#!/bin/bash

# Script de lancement de l'application Horus RPi5

set -e

echo "=== Lancement de Horus-RPi5 ==="

# Vérifier que Python3 est installé
if ! command -v python3 &> /dev/null; then
    echo "Erreur : Python3 n'est pas installé"
    exit 1
fi

# Aller dans le répertoire de l'application
cd "$(dirname "$0")"

# Lancer l'application
python3 -m horus

echo "=== Horus-RPi5 fermé ==="
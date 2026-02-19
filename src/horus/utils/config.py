import json
import os
from horus.utils.logger import logger

class Config:
    def __init__(self, filename="config.json"):
        """
        Charge config.json depuis :
        - le chemin absolu si fourni
        - sinon depuis le dossier du projet
        - sinon depuis le dossier courant
        """

        # 1. Chemin absolu
        if os.path.isabs(filename) and os.path.exists(filename):
            path = filename

        else:
            # 2. Chemin relatif au projet
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            candidate = os.path.join(base_dir, filename)

            if os.path.exists(candidate):
                path = candidate
            elif os.path.exists(filename):
                # 3. Dossier courant
                path = filename
            else:
                raise FileNotFoundError(f"Fichier de configuration introuvable : {filename}")

        logger.info(f"Chargement configuration : {path}")

        with open(path, "r") as f:
            self.data = json.load(f)

    def get(self, path, default=None):
        """
        Exemple : get("camera.width")
        """
        keys = path.split(".")
        value = self.data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                logger.warning(f"Config: clé manquante '{path}', valeur par défaut = {default}")
                return default

        return value

import json
import os
from horus.utils.logger import logger

class CalibrationStore:
    def __init__(self, filename="calibration.json"):
        """
        Stocke la calibration dans le dossier du projet.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        self.path = os.path.join(base_dir, filename)

        # Créer le fichier si nécessaire
        if not os.path.exists(self.path):
            logger.warning(f"Fichier calibration absent, création : {self.path}")
            self.save(None, None)

    def save(self, left_plane, right_plane):
        """
        Sauvegarde les plans laser dans un fichier JSON.
        """
        data = {
            "left_plane": list(left_plane) if left_plane else None,
            "right_plane": list(right_plane) if right_plane else None
        }

        try:
            with open(self.path, "w") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Calibration sauvegardée : {self.path}")
        except Exception as e:
            logger.error(f"Erreur sauvegarde calibration : {e}")

    def load(self):
        """
        Charge les plans laser depuis le fichier JSON.
        """
        if not os.path.exists(self.path):
            logger.warning("Aucune calibration trouvée.")
            return None, None

        try:
            with open(self.path, "r") as f:
                data = json.load(f)

            left = data.get("left_plane")
            right = data.get("right_plane")

            logger.info("Calibration chargée avec succès.")
            return left, right

        except Exception as e:
            logger.error(f"Erreur lecture calibration : {e}")
            return None, None

import threading
import time

import cv2
import numpy as np

from horus.engine.camera import Camera
from horus.engine.profile_extractor import ProfileExtractor
from horus.engine.reconstruction import Reconstruction3D
from horus.engine.grbl_controller import GRBLController
from horus.engine.ai_laser import LaserAI
from horus.engine.ai_pointcloud import PointCloudAI
from horus.engine.ai_calibration import CalibrationAI
from horus.utils.config import Config
from horus.utils.logger import logger


class ScanEngine:
    def __init__(self):
        self.camera = Camera()
        self.extractor = ProfileExtractor()
        self.reconstruction = Reconstruction3D()
        self.grbl = GRBLController()

        # IA modules
        self.laser_ai = LaserAI()
        self.pc_ai = PointCloudAI()
        self.calib_ai = CalibrationAI()

        # Configuration
        cfg = Config()
        self.steps = cfg.get("scan.steps", 200)
        self.step_angle = cfg.get("grbl.step_angle", 1.8)
        self.output_file = cfg.get("scan.output_file", "scan.ply")

        self._stop_event = threading.Event()

    def stop(self):
        """Demande l'arrêt du scan en cours (pris en compte à la prochaine étape)."""
        self._stop_event.set()

    def run_scan_yield(self):
        """
        Exécute le scan pas à pas et rend la main (yield) après chaque étape
        avec (angle_courant, message_statut), pour permettre à l'appelant
        (GUI) de suivre la progression sans bloquer.
        """
        self._stop_event.clear()
        angle = 0
        background = None

        logger.info("Initialisation du scan")

        try:
            # Connexion matériel
            self.grbl.connect()
            self.camera.open()

            # Allumer laser gauche
            self.grbl.set_laser(left=True)

            # Calibration IA (optionnel)
            frame = self.camera.read()
            calib = self.calib_ai.auto_calibrate(frame)
            logger.info(f"Calibration IA : {calib}")

            if self.camera.background_subtraction:
                self.grbl.set_laser(False)
                background = self.camera.capture_background()
                self.grbl.set_laser(left=True)

            for step in range(self.steps):
                if self._stop_event.is_set():
                    logger.info("Scan interrompu par l'utilisateur")
                    break

                status = f"Étape {step + 1}/{self.steps}"
                logger.info(status)

                try:
                    frame = self.camera.read()
                except Exception as e:
                    logger.error(f"Frame caméra invalide : {e}")
                    yield angle, f"{status} : capture échouée, étape ignorée"
                    continue

                if background is not None:
                    frame = cv2.absdiff(frame, background)

                # IA Laser → masque binaire
                mask = self.laser_ai.detect(frame)

                # Extraction profil
                profile = self.extractor.extract_profile(mask)

                # Reconstruction 3D
                self.reconstruction.add_profile(profile, angle)

                # Rotation plateau
                angle += self.step_angle
                self.grbl.rotate_relative(self.step_angle)

                yield angle, status

                time.sleep(0.15)  # stabilisation

        finally:
            # Toujours couper le laser et libérer le matériel, même en cas d'erreur.
            try:
                self.grbl.set_laser(False)
            except Exception as e:
                logger.error(f"Erreur lors de l'extinction du laser : {e}")

            self.camera.close()
            self.grbl.disconnect()

        # Nettoyage IA du nuage de points
        points = np.array(self.reconstruction.points)
        points = self.pc_ai.clean(points)
        points = self.pc_ai.interpolate(points)

        # Remplacer les points par ceux nettoyés
        self.reconstruction.points = points.tolist()

        # Export
        self.reconstruction.export_ply(self.output_file)

        logger.info(f"Scan terminé, fichier exporté : {self.output_file}")
        yield angle, f"Scan terminé, fichier exporté : {self.output_file}"

    def run_scan(self):
        """Exécute le scan intégralement (sans progression incrémentale)."""
        for _angle, _status in self.run_scan_yield():
            pass

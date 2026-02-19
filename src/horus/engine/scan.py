import time
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
        self.laser_ai = LaserAI(tflite_path="models/laser.tflite")
        self.pc_ai = PointCloudAI()
        self.calib_ai = CalibrationAI()

        # Configuration
        cfg = Config()
        self.steps = cfg.get("scan.steps")
        self.step_angle = cfg.get("grbl.step_angle")

    def run_scan(self):
        logger.info("Initialisation du scan")

        # Connexion matériel
        self.grbl.connect()
        self.camera.open()

        angle = 0

        # Calibration IA (optionnel)
        frame = self.camera.read()
        calib = self.calib_ai.auto_calibrate(frame)
        logger.info(f"Calibration IA : {calib}")

        for step in range(self.steps):
            logger.info(f"Étape {step+1}/{self.steps}")

            frame = self.camera.read()
            if frame is None:
                logger.error("Frame caméra invalide")
                continue

            # IA Laser
            mask = self.laser_ai.detect(frame)

            # Extraction profil
            profile = self.extractor.extract_profile(mask)

            # Reconstruction 3D
            self.reconstruction.add_profile(profile, angle)

            # Rotation plateau
            angle += self.step_angle
            self.grbl.rotate_step()

            time.sleep(0.1)

        # Fin du scan
        self.camera.close()
        self.grbl.disconnect()

        # Nettoyage IA du nuage de points
        points = np.array(self.reconstruction.points)
        points = self.pc_ai.clean(points)
        points = self.pc_ai.interpolate(points)

        # Export
        self.reconstruction.export_ply("scan.ply", points)

        logger.info("Scan terminé, fichier exporté : scan.ply")

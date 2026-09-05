import os
import numpy as np
import cv2

from horus.utils.config import Config
from horus.utils.logger import logger

# Plage HSV par défaut (laser rouge), utilisée si config.json ne fournit rien.
DEFAULT_HSV_RANGES = [
    ((0, 120, 120), (10, 255, 255)),
    ((170, 120, 120), (180, 255, 255)),
]


class LaserAI:
    def __init__(self, tflite_path=None, hsv_ranges=None):
        cfg = Config()

        if tflite_path is None:
            tflite_path = cfg.get("laser.model_path")

        if hsv_ranges is None:
            hsv_ranges = cfg.get("laser.hsv_ranges")

        self.hsv_ranges = self._parse_hsv_ranges(hsv_ranges)
        self.model = None
        self.model_loaded = False

        if tflite_path:
            if not os.path.exists(tflite_path):
                logger.warning(
                    f"Modèle TFLite introuvable ({tflite_path}), "
                    "utilisation du mode de secours HSV."
                )
            else:
                try:
                    import tflite_runtime.interpreter as tflite
                    self.model = tflite.Interpreter(model_path=tflite_path)
                    self.model.allocate_tensors()
                    self.model_loaded = True
                    logger.info(f"Modèle TFLite chargé : {tflite_path}")
                except Exception as e:
                    logger.error(
                        f"Échec du chargement du modèle TFLite '{tflite_path}' : {e}. "
                        "Utilisation du mode de secours HSV."
                    )
                    self.model = None

    @staticmethod
    def _parse_hsv_ranges(hsv_ranges):
        if not hsv_ranges:
            return DEFAULT_HSV_RANGES
        try:
            return [(tuple(low), tuple(high)) for low, high in hsv_ranges]
        except (TypeError, ValueError):
            logger.warning("Config laser.hsv_ranges invalide, valeurs par défaut utilisées.")
            return DEFAULT_HSV_RANGES

    def detect(self, frame):
        if frame is None:
            return None

        # IA TFLite
        if self.model:
            try:
                input_details = self.model.get_input_details()
                output_details = self.model.get_output_details()

                img = cv2.resize(frame, (128, 128))
                img = img.astype(np.float32) / 255.0
                img = np.expand_dims(img, axis=0)

                self.model.set_tensor(input_details[0]['index'], img)
                self.model.invoke()
                mask = self.model.get_tensor(output_details[0]['index'])[0]

                # Normalisation + resize
                mask = np.clip(mask, 0, 1)
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))

                mask = (mask > 0.5).astype(np.uint8) * 255
                mask = cv2.medianBlur(mask, 5)
                return mask

            except Exception as e:
                # fallback automatique
                logger.error(f"Erreur d'inférence TFLite : {e}. Passage en mode HSV.")
                self.model = None
                self.model_loaded = False

        # Fallback OpenCV HSV (laser rouge par défaut, configurable via config.json)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask = None
        for lower, upper in self.hsv_ranges:
            partial = cv2.inRange(hsv, np.array(lower), np.array(upper))
            mask = partial if mask is None else cv2.bitwise_or(mask, partial)

        mask = cv2.medianBlur(mask, 5)

        return mask

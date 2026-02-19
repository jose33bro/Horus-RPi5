"""
Module IA pour Horus-RPi5
Toutes les fonctions IA sont centralisées ici.
Tu pourras ensuite brancher TensorFlow Lite, ONNX, OpenVINO ou Ollama.
"""

import numpy as np
import cv2

# ----------------------------------------------------------------------
# IA 1 — Assistant IA (diagnostic, conseils)
# ----------------------------------------------------------------------

def ai_assistant_analyze(status):
    """
    Analyse l'état du scanner et renvoie un diagnostic IA.
    """
    return {
        "status": "OK",
        "message": "Analyse IA : tout semble fonctionner correctement.",
        "details": status
    }

# ----------------------------------------------------------------------
# IA 2 — Analyse caméra en temps réel
# ----------------------------------------------------------------------

def ai_camera_analyze(frame):
    """
    Analyse la qualité de l'image caméra.
    Retourne un score simple pour l'instant.
    """
    if frame is None:
        return {"brightness": 0, "sharpness": 0}

    brightness = np.mean(frame)
    sharpness = cv2.Laplacian(frame, cv2.CV_64F).var()

    return {
        "brightness": float(brightness),
        "sharpness": float(sharpness)
    }

# ----------------------------------------------------------------------
# IA 3 — Détection laser (segmentation IA)
# ----------------------------------------------------------------------

def ai_detect_laser(frame):
    """
    Détection simple du laser (version IA minimale).
    Tu pourras remplacer par un modèle TFLite.
    """
    if frame is None:
        return None

    # Détection naïve du laser rouge
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 120])
    upper_red = np.array([10, 255, 255])
    mask = cv2.inRange(hsv, lower_red, upper_red)

    return mask

# ----------------------------------------------------------------------
# IA 4 — Calibration intelligente
# ----------------------------------------------------------------------

def ai_auto_calibration(frame):
    """
    Détection automatique des paramètres caméra/laser.
    Version simple pour l'instant.
    """
    if frame is None:
        return None

    h, w = frame.shape[:2]
    return {
        "cx": w / 2,
        "cy": h / 2,
        "focal": max(w, h)
    }

# ----------------------------------------------------------------------
# IA 5 — Nettoyage du nuage de points
# ----------------------------------------------------------------------

def ai_clean_point_cloud(points):
    """
    Nettoyage simple du nuage de points.
    Tu pourras remplacer par un modèle IA plus tard.
    """
    if points is None or len(points) == 0:
        return points

    # Suppression des points aberrants
    mean = np.mean(points, axis=0)
    dist = np.linalg.norm(points - mean, axis=1)
    threshold = np.mean(dist) + 2 * np.std(dist)

    return points[dist < threshold]

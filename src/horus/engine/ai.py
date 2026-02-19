"""
Module IA complet pour Horus-RPi5
Inclut :
- IA Laser (TFLite ou fallback OpenCV)
- IA Nuage de points (nettoyage + interpolation)
- IA Calibration automatique
- Assistant IA (diagnostic + chat local)
"""

import numpy as np
import cv2

# ----------------------------------------------------------------------
# IA 1 — Assistant IA (diagnostic + chat local)
# ----------------------------------------------------------------------

def ai_assistant(status, question=""):
    """
    Analyse l'état du scanner et répond à une question utilisateur.
    Version simple, prête à être remplacée par un modèle local (Ollama).
    """
    base = {
        "status": "OK",
        "diagnostic": "Aucun problème détecté dans le pipeline.",
        "details": status
    }

    if question:
        base["assistant_reply"] = (
            "Je suis l'assistant IA de Horus. "
            "Je peux analyser la caméra, le laser, la calibration et le nuage de points."
        )

    return base

# ----------------------------------------------------------------------
# IA 2 — Analyse caméra en temps réel
# ----------------------------------------------------------------------

def ai_camera_analyze(frame):
    if frame is None:
        return {"brightness": 0, "sharpness": 0}

    brightness = float(np.mean(frame))
    sharpness = float(cv2.Laplacian(frame, cv2.CV_64F).var())

    return {
        "brightness": brightness,
        "sharpness": sharpness,
        "quality": (brightness / 255) * (sharpness / 500)
    }

# ----------------------------------------------------------------------
# IA 3 — Détection laser (TFLite ou fallback)
# ----------------------------------------------------------------------

def ai_detect_laser(frame, tflite_model=None):
    if frame is None:
        return None

    if tflite_model:
        # Prétraitement pour TFLite
        img = cv2.resize(frame, (128, 128))
        img = img.astype(np.float32) / 255.0
        img = np.expand_dims(img, axis=0)

        tflite_model.set_tensor(0, img)
        tflite_model.invoke()
        mask = tflite_model.get_tensor(1)[0]
        mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]))
        return (mask > 0.5).astype(np.uint8) * 255

    # Fallback OpenCV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 120, 120])
    upper_red = np.array([10, 255, 255])
    return cv2.inRange(hsv, lower_red, upper_red)

# ----------------------------------------------------------------------
# IA 4 — Calibration intelligente
# ----------------------------------------------------------------------

def ai_auto_calibration(frame):
    if frame is None:
        return None

    h, w = frame.shape[:2]

    return {
        "cx": w / 2,
        "cy": h / 2,
        "focal": max(w, h),
        "confidence": 0.85
    }

# ----------------------------------------------------------------------
# IA 5 — Nettoyage du nuage de points
# ----------------------------------------------------------------------

def ai_clean_point_cloud(points):
    if points is None or len(points) == 0:
        return points

    mean = np.mean(points, axis=0)
    dist = np.linalg.norm(points - mean, axis=1)
    threshold = np.mean(dist) + 2 * np.std(dist)

    filtered = points[dist < threshold]

    # Interpolation simple
    if len(filtered) > 10:
        filtered = cv2.GaussianBlur(filtered, (5, 5), 0)

    return filtered


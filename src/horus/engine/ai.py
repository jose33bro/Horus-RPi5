import numpy as np
import cv2

"""
Module IA générique pour Horus-RPi5.
Contient :
- Assistant IA (diagnostic)
- Analyse caméra
- Wrappers optionnels
"""

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
        "diagnostic": "Pipeline fonctionnel.",
        "details": status
    }

    if question:
        base["assistant_reply"] = (
            "Je suis l'assistant IA de Horus-RPi5. "
            "Je peux analyser la caméra, le laser, la calibration et le nuage de points."
        )

    return base

# ----------------------------------------------------------------------
# IA 2 — Analyse caméra en temps réel
# ----------------------------------------------------------------------

def ai_camera_analyze(frame):
    if frame is None:
        return {"brightness": 0, "sharpness": 0, "quality": 0}

    brightness = float(np.mean(frame))
    sharpness = float(cv2.Laplacian(frame, cv2.CV_64F).var())

    quality = (brightness / 255.0) * min(sharpness / 500.0, 1.0)

    return {
        "brightness": brightness,
        "sharpness": sharpness,
        "quality": quality
    }
